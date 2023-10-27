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
using TaskMgrAPI.Exceptions;
using TaskMgrAPI.Services.Project;
using TaskMgrAPI.Services.Section;

namespace TaskMgrAPI.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class ProjectController : ControllerBase
    {
        private readonly IProjectService _projectService;
        private readonly ISectionService _sectionService;
        private LinkGenerator _linkGenerator;
        
        public ProjectController(IProjectService projectService, ISectionService sectionService, LinkGenerator linkGenerator)
        {
            _projectService = projectService;
            _linkGenerator = linkGenerator;
            _sectionService = sectionService;
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
        private async Task<List<Link>> UserAction(string telegramId, long projectId)
        {
            var rights = await _projectService.UserRights(telegramId, projectId);

            var userLinks = CreateProjectLink(projectId, rights);
            
            return userLinks.ToList();
        }
        
        [Route("{projectId:long}")]
        [HttpGet]
        public async Task<ActionResult<ResponseGetProjectDto>> GetById([FromHeader(Name = "Telegram-Id")] string telegramId, long projectId)
        {
            try
            {
                var projectDto = (await _projectService.Get(projectId)).First();

                var response = new ResponseGetProjectDto()
                {
                    project = projectDto,
                    links = await UserAction(telegramId, projectId)
                };

                return Ok(response);
            }
            catch (NotFoundException ex)
            {
                return NotFound(ex.Message);
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }
        
        [HttpPost]
        public async Task<ActionResult<ProjectDto>> Create(RequestCreateProjectDto data)
        {
            try
            {
                var projectDto = await _projectService.Create(data.title, data.description);

                return Ok(projectDto);
            }
            catch (NotFoundException ex)
            {
                return NotFound(ex.Message);
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }

        [HttpGet]
        public async Task<ActionResult<List<ProjectDto>>> Get([FromHeader(Name = "Telegram-Id")] string? telegramId)
        {
            try
            {
                var projectsDto = await _projectService.Get(telegramId:telegramId);

                return Ok(projectsDto);
            }
            catch (NotFoundException ex)
            {
                return NotFound(ex.Message);
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }
        
        [Route("{projectId:long}")]
        [HttpPut]
        [RightTaskMgr("update_project")]
        public async Task<ActionResult<ProjectDto>> Update(long projectId, RequestCreateProjectDto data)
        {
            try
            {
                var projectsDto = await _projectService.Update(projectId,
                    data.title,
                    data.description);

                return Ok(projectsDto);
            }
            catch (NotFoundException ex)
            {
                return NotFound(ex.Message);
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }

        [Route("{projectId:long}/user")]
        [HttpPost]
        [RightTaskMgr("update_project", "add_user")]
        public async Task<ActionResult<ProjectDto>> AddUser(long projectId, RequestAddUser data)
        {
            try
            {
                var userRoles = await _projectService.AddUser(data.user_id, projectId, data.role_id);
                return Ok(userRoles);
            }
            catch (NotFoundException ex)
            {
                return NotFound(ex.Message);
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }
        
        [Route("{projectId:long}/user")]
        [HttpGet]
        [RightTaskMgr("view_project")]
        public async Task<ActionResult<List<UserRoleDto>>> GetUsers(long projectId)
        {
            try
            {
                var userRoles = await _projectService.UserProject(projectId);
                return Ok(userRoles);
            }
            catch (NotFoundException ex)
            {
                return NotFound(ex.Message);
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }

        [Route("{projectId:long}/section")]
        [HttpPost]
        [RightTaskMgr("update_project", "add_section")]
        public async Task<ActionResult<ProjectDto>> AddSection(long projectId, RequestCreateSectionDto data)
        {
            try
            {
                var comments = await _sectionService.Create(data.title, projectId);
                return Ok(comments);
            }
            catch (NotFoundException ex)
            {
                return NotFound(ex.Message);
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }
        
        [Route("{projectId:long}/section")]
        [HttpGet]
        [RightTaskMgr("view_project")]
        public async Task<ActionResult<List<long>>> GetSections(long projectId)
        {
            try
            {
                var sections = await _sectionService.Get(projectId: projectId);
                return Ok(sections);
            }
            catch (NotFoundException ex)
            {
                return NotFound(ex.Message);
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }
    }
}
