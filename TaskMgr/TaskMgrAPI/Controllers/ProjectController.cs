using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TaskMgrAPI.Context;
using TaskMgrAPI.Dtos.User;
using TaskMgrAPI.Models;

using TaskMgrAPI.Dtos.Role;
using TaskMgrAPI.Dtos.Project;
using TaskMgrAPI.Dtos.Section;

namespace TaskMgrAPI.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class ProjectController : ControllerBase
    {
        private readonly TaskmgrContext _context;

        public ProjectController(TaskmgrContext context)
        {
            _context = context;
        }
        
        private async Task<List<string>> UserAction(long user_id, long project_id)
        { // TODO: ввести свой декоратор в котором мы указываем право, которым должен владеть человек чтобы использовать этот эндпоинт
            var rights = await _context.Database
                .SqlQuery<string>(
                    $"select r2.title from public.user_project as up join public.role r on up.role_id = r.role_id join public.right_role rr on r.role_id = rr.role_id join public.\"right\" r2 on rr.right_id = r2.right_id where up.user_id = {user_id} and project_id = {project_id}"
                )
                .ToListAsync();
            // TODO: теперь нужно сделать параметры для функций которые будут говорить о том какое действие может делать человек
            
            return rights;
        }
        
        [Route("{project_id}")]
        [HttpGet]
        public async Task<ActionResult<ProjectDto>> Index(long project_id)
        {
            var project = await _context.Projects
                .FromSql($"SELECT * FROM public.project WHERE project_id = {project_id} LIMIT 1")
                .ToListAsync();
            
            if (project.Count == 0)
            {
                return NotFound();
            }

            var projectDto = new ProjectDto
            {
                project_id = project[0].ProjectId,
                title = project[0].Title,
                description = project[0].Description ?? ""
            };

            // TODO: сделать логику обработки ролей и прав

            return Ok(projectDto);
        }
        
        [HttpPost]
        public async Task<ActionResult<ProjectDto>> Create(RequestCreateProjectDto data)
        {
            var id = await _context.Database
                .SqlQuery<long>(
                    $"INSERT INTO public.project (title, description) VALUES ({data.title}, {data.description}) RETURNING user_id"
                )
                .ToListAsync();

            return await Index(id[0]);
        }

        [HttpGet]
        public async Task<ActionResult<List<long>>> Get()
        {
            var projects = await _context.Projects
                .Select(u => u.ProjectId)
                .ToListAsync();

            return Ok(projects);
        }
        
        [Route("{project_id}")]
        [HttpPut]
        public async Task<ActionResult<ProjectDto>> Update(long project_id, RequestCreateProjectDto data)
        {
            var id = await _context.Database
                .SqlQuery<long>(
                    $"update public.project as p set (title, description) = ({data.title}, {data.description}) where p.project_id = {project_id} returning project_id"
                )
                .ToListAsync();

            return await Index(project_id);
        }

        [Route("{project_id}/user")]
        [HttpPost]
        public async Task<ActionResult<ProjectDto>> AddUser(long project_id, RequestAddUser data)
        {
            var id = await _context.Database
                .SqlQuery<long>(
                    $"insert into public.user_project (user_id, project_id, role_id) values ({data.user_id}, {project_id}, {data.role_id})"
                )
                .ToListAsync();
            return await Index(project_id);
        }

        [Route("{project_id}/user")]
        [HttpGet]
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
        public async Task<ActionResult<ProjectDto>> AddSection(long project_id, RequestCreateSectionDto data)
        {
            var id = await _context.Database
                .SqlQuery<long>(
                    $"insert into public.section (title, project_id) VALUES ({data.title}, {project_id})"
                )
                .ToListAsync();

            return await Index(project_id);
        }
        
        [Route("{project_id}/section")]
        [HttpGet]
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
