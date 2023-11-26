using Microsoft.EntityFrameworkCore;
using TaskMgrAPI.Context;
using TaskMgrAPI.Services.User;

namespace TaskMgrAPI.Services.UserProject;

public class UserProjectService : IUserProjectService
{
    private readonly TaskmgrContext _context;
    private readonly IUserService _userService;

    public UserProjectService(TaskmgrContext context, IUserService userService)
    {
        _context = context;
        _userService = userService;
    }
    
    public async Task<List<Models.UserProject>> GetModels(long? id = null, long? userId = null, long? projectId = null, long? roleId = null)
    {
        var idCheck = id is null;
        var userIdCheck = userId is null;
        var projectIdCheck = projectId is null;
        var roleIdCheck = roleId is null;

        var items = await _context.UserProjects
            .Where(c =>
                (c.UserProjectId == id || idCheck) &&
                (c.UserId == userId || userIdCheck) &&
                (c.ProjectId == projectId || projectIdCheck) &&
                (c.RoleId == roleId || roleIdCheck)
            )
            .Include(c => c.User)
            .Include(c => c.Project)
            .Include(c => c.Role)
            .ToListAsync();

        return items;
    }
}