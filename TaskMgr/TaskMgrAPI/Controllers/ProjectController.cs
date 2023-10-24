using System.Reflection;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TaskMgrAPI.Context;
using TaskMgrAPI.Dtos.User;
using TaskMgrAPI.Models;

using TaskMgrAPI.Dtos.Role;
using TaskMgrAPI.Dtos.Project;
using TaskMgrAPI.Dtos.Section;
using TaskMgrAPI.Attributes;

namespace TaskMgrAPI.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class ProjectController : ControllerBase
    {
        private readonly TaskmgrContext _context;
        private LinkGenerator _linkGenerator;
        
        public ProjectController(TaskmgrContext context, LinkGenerator linkGenerator)
        {
            _context = context;
            _linkGenerator = linkGenerator;
        }

        private async Task<long> AuthUser(string telegramId)
        {
            var userId = await _context.Users.Where(u => u.TelegramId == telegramId).Select(u => u.UserId).FirstAsync();
            return userId;
        }

        private IEnumerable<Link> CreateProjectLink(long project_id, List<string> rights)
        {
            var links = new List<Link>();
            
            foreach (var method in typeof(ProjectController).GetMethods())
            {
                var attrs = (RightTaskMgr[]) method.GetCustomAttributes(typeof(RightTaskMgr), false);
                foreach (var attr in attrs)
                {
                    if (attr.Right.Intersect(rights).Count() == 0)
                        continue;
                    
                    var methodHttp = "";
                    if (method.GetCustomAttributes(typeof(HttpGetAttribute), false).Count() != 0)
                        methodHttp = "GET";
                    else if (method.GetCustomAttributes(typeof(HttpPostAttribute), false).Count() != 0)
                        methodHttp = "POST";
                    else if (method.GetCustomAttributes(typeof(HttpPatchAttribute), false).Count() != 0)
                        methodHttp = "PATCH";
                    else if (method.GetCustomAttributes(typeof(HttpPutAttribute), false).Count() != 0)
                        methodHttp = "PUT";
                    else if (method.GetCustomAttributes(typeof(HttpDeleteAttribute), false).Count() != 0)
                        methodHttp = "DELETE";

                    Console.WriteLine(method.GetCustomAttributes(typeof(Route), false).Length);
                    Console.WriteLine(method.Name);
                    Console.WriteLine(project_id);
                    Console.WriteLine(_linkGenerator.GetUriByAction(HttpContext, method.Name, values: new { project_id }));

                    links.Add(
                        new Link()
                        {
                            Href = _linkGenerator.GetUriByAction(HttpContext, method.Name, values: new { project_id }) ?? "",
                            Rel = "self",
                            Method = methodHttp
                        }
                    );
                }
            }
            
            return links;
        }
        private async Task<List<Link>> UserAction(string telegram_id, long project_id)
        {
            var userId = await AuthUser(telegram_id);
            var rights = await _context.Database
                .SqlQuery<string>(
                    $"select distinct(r2.title) from public.user_project as up join public.role r on up.role_id = r.role_id join public.right_role rr on r.role_id = rr.role_id join public.\"right\" r2 on rr.right_id = r2.right_id where up.user_id = {userId} and project_id = {project_id}"
                )
                .ToListAsync();

            var userLinks = CreateProjectLink(project_id, rights);
            
            return userLinks.ToList();
        }
        
        private async Task<ProjectDto?> GetProjectDto(long project_id)
        {
            var project = await _context.Projects
                .FromSql($"SELECT * FROM public.project WHERE project_id = {project_id} LIMIT 1")
                .ToListAsync();
            
            if (project.Count == 0)
            {
                return null;
            }

            var projectDto = new ProjectDto
            {
                project_id = project[0].ProjectId,
                title = project[0].Title,
                description = project[0].Description ?? ""
            };
            
            return projectDto;
        }
        
        [Route("{project_id}")]
        [HttpGet]
        public async Task<ActionResult<ResponseGetProjectDto>> GetById([FromHeader(Name = "Telegram-Id")] string telegramId, long project_id)
        {
            var projectDto = await GetProjectDto(project_id);
            if (projectDto is null)
            {
                return NotFound();
            }

            var response = new ResponseGetProjectDto()
            {
                project = projectDto,
                links = await UserAction(telegramId, project_id)
            };

            return Ok(response);
        }
        
        [HttpPost]
        public async Task<ActionResult<ProjectDto>> Create(RequestCreateProjectDto data)
        {
            var id = await _context.Database
                .SqlQuery<long>(
                    $"INSERT INTO public.project (title, description) VALUES ({data.title}, {data.description}) RETURNING project_id"
                )
                .ToListAsync();
            
            return await GetProjectDto(id[0]);
        }

        [HttpGet]
        public async Task<ActionResult<List<ProjectDto>>> Get([FromHeader(Name = "Telegram-Id")] string? telegramId)
        {
            long? userId = null;
            if (telegramId != null)
            {
                userId = await AuthUser(telegramId);
            }
            
            var allowProjects = await _context.UserProjects
                .Where(up => up.UserId == (userId ?? up.UserId))
                .Include(up => up.Project)
                .Select(up => new ProjectDto()
                {
                    project_id = up.Project.ProjectId,
                    title = up.Project.Title,
                    description = up.Project.Description ?? ""
                })
                .ToListAsync();
            allowProjects = allowProjects.DistinctBy(p => p.project_id).ToList();

            return Ok(allowProjects);
        }
        
        [Route("{project_id}")]
        [HttpPut]
        [RightTaskMgr("update_project")]
        public async Task<ActionResult<ProjectDto>> Update(long project_id, RequestCreateProjectDto data)
        {
            var id = await _context.Database
                .SqlQuery<long>(
                    $"update public.project as p set (title, description) = ({data.title}, {data.description}) where p.project_id = {project_id} returning project_id"
                )
                .ToListAsync();

            return await GetProjectDto(project_id);
        }

        [Route("{project_id}/user")]
        [HttpPost]
        [RightTaskMgr("update_project", "add_user")]
        public async Task<ActionResult<ProjectDto>> AddUser(long project_id, RequestAddUser data)
        {
            var id = await _context.Database
                .SqlQuery<long>(
                    $"insert into public.user_project (user_id, project_id, role_id) values ({data.user_id}, {project_id}, {data.role_id})"
                )
                .ToListAsync();
            return await GetProjectDto(project_id);
        }
        
        [Route("{project_id}/user")]
        [HttpGet]
        [RightTaskMgr("view_project")]
        public async Task<ActionResult<List<UserRoleDto>>> GetUsers(long project_id)
        {
            var user_roles = await _context.UserProjects
                .FromSql($"select * from public.user_project as up where up.project_id = {project_id}")
                .Select(ur => new UserRoleDto()
                {
                    role_id = ur.RoleId,
                    user_id = ur.UserId
                })
                .ToListAsync();

            return Ok(user_roles);
        }

        [Route("{project_id}/section")]
        [HttpPost]
        [RightTaskMgr("update_project", "add_section")]
        public async Task<ActionResult<ProjectDto>> AddSection(long project_id, RequestCreateSectionDto data)
        {
            var id = await _context.Database
                .SqlQuery<long>(
                    $"insert into public.section (title, project_id) VALUES ({data.title}, {project_id})"
                )
                .ToListAsync();

            return await GetProjectDto(project_id);
        }
        
        [Route("{project_id}/section")]
        [HttpGet]
        [RightTaskMgr("view_project")]
        public async Task<ActionResult<List<long>>> GetSections(long project_id)
        {
            var ids = await _context.Sections
                .Where(u => u.ProjectId == project_id)
                .Select(u => u.SectionId)
                .ToListAsync();

            return Ok(ids);
        }

        [Route("{project_id}/role")]
        [HttpGet]
        [RightTaskMgr("view_project")]
        public async Task<ActionResult<List<long>>> GetRoles(long project_id)
        {
            var roles = await _context.Roles
                .FromSql($"select r.role_id from public.role as r where 'project' = any(r.allow_tables::text[])")
                .Select(r => r.RoleId)
                .ToListAsync();

            return Ok(roles);
        }
    }
}
