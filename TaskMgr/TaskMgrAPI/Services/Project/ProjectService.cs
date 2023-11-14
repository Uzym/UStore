using Microsoft.EntityFrameworkCore;
using TaskMgrAPI.Context;
using TaskMgrAPI.Dtos.Project;
using TaskMgrAPI.Dtos.User;
using TaskMgrAPI.Exceptions;
using TaskMgrAPI.Services.User;

namespace TaskMgrAPI.Services.Project;

public class ProjectService : IProjectService
{
    private readonly TaskmgrContext _context;
    private readonly IUserService _userService;

    public ProjectService(TaskmgrContext context, IUserService userService)
    {
        _context = context;
        _userService = userService;
    }
    
    private static ProjectDto TranslateIntoDto(Models.Project project)
    {
        var dto = new ProjectDto()
        {
            project_id = project.ProjectId,
            title = project.Title,
            description = project.Description ?? "",
        };
        return dto;
    }
    
    public async Task<List<string>> UserRights(string telegramId, long projectId)
    {
        var userId = (await _userService.Get(telegramId: telegramId)).First().user_id;
        var rights = await _context.Database
            .SqlQuery<string>(
                $"select distinct(r2.title) from public.user_project as up join public.role r on up.role_id = r.role_id join public.right_role rr on r.role_id = rr.role_id join public.\"right\" r2 on rr.right_id = r2.right_id where up.user_id = {userId} and project_id = {projectId}"
            )
            .ToListAsync();

        return rights;
    }

    public async Task<List<ProjectDto>> Get(long? id = null, string? title = null, string? description = null, string? telegramId = null)
    {
        long? userId = null;
        if (telegramId != null)
        {
            userId = (await _userService.Get(telegramId: telegramId)).First().user_id;
        }
        
        var idCheck = id is null;
        var titleCheck = title is null;
        var descriptionCheck = description is null;
        
        var projects = await _context.Projects
            .Include(r => r.UserProjects)
            .Where(r =>
                (r.ProjectId == id || idCheck) &&
                (r.Title == title || titleCheck) &&
                (r.Description == description || descriptionCheck) &&
                (r.UserProjects.Any(up => up.UserId == (userId ?? up.UserId)))
            )
            .Select(r => TranslateIntoDto(r))
            .ToListAsync();
        
        return projects;
    }

    public async Task<ProjectDto> Create(string title, string description)
    {
        var model = new Models.Project()
        {
            Title = title,
            Description = description
        };
        await _context.Projects.AddAsync(model);
        await _context.SaveChangesAsync();
            
        return TranslateIntoDto(model);
    }

    public async Task<ProjectDto> Update(long id, string? title = null, string? description = null)
    {
        var project = await _context.Projects
            .Where(c => c.ProjectId == id)
            .FirstOrDefaultAsync();
        if (project is null)
        {
            throw new NotFoundException($"card {id} not found");
        }
        if (title is not null)
        {
            project.Title = title;
        }
        if (description is not null)
        {
            project.Description = description;
        }
        
        await _context.SaveChangesAsync();
        return TranslateIntoDto(project);
    }
    
    public async Task<List<UserRoleDto>> UserProject(long projectId)
    {
        var userRoles = await _context.UserProjects
            .FromSql($"select * from public.user_project as up where up.project_id = {projectId}")
            .Select(ur => new UserRoleDto()
            {
                role_id = ur.RoleId,
                user_id = ur.UserId
            })
            .ToListAsync();

        return userRoles;
    }

    public async Task<List<UserRoleDto>> AddUser(long userId, long projectId, long roleId)
    {
        var id = await _context.Database
            .SqlQuery<long>(
                $"insert into public.user_project (user_id, project_id, role_id) values ({userId}, {projectId}, {roleId})"
            )
            .ToListAsync();
        return await UserProject(projectId);
    }

    public async Task<List<UserRoleDto>> RemoveUser(long userId, long projectId)
    {
        var id = await _context.Database
            .SqlQuery<long>(
                $"delete FROM public.user_project where project_id ={projectId} and user_id = {userId}"
            )
            .ToListAsync();
        return await UserProject(projectId);
    }

    public async Task<List<Models.Project>> GetModels(long? id = null)
    {
        var idCheck = id is null;
        var items = await _context.Projects
            .Where(c => 
                (c.ProjectId == id || idCheck)
            )
            .Include(c => c.Sections)
            .Include(c => c.UserProjects)
            .ToListAsync();

        return items;
    }
}