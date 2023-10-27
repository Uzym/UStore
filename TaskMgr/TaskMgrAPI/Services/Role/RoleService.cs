using Microsoft.EntityFrameworkCore;
using TaskMgrAPI.Context;
using TaskMgrAPI.Dtos.Role;

namespace TaskMgrAPI.Services.Role;

public class RoleService : IRoleService
{
    private readonly TaskmgrContext _context;

    public RoleService(TaskmgrContext context)
    {
        _context = context;
    }
    
    private static RoleDto TranslateIntoDto(Models.Role role)
    {
        var dto = new RoleDto()
        {
            role_id = role.RoleId,
            title = role.Title,
            description = role.Description ?? "",
        };
        return dto;
    }

    public async Task<List<RoleDto>> Get(long? id = null, string? title = null, string? description = null, string? table = null)
    {
        var idCheck = id is null;
        var titleCheck = title is null;
        var descriptionCheck = description is null;
        var tableCheck = table is null;

        var roles = await _context.Roles
            .Where(r =>
                (r.RoleId == id || idCheck) &&
                (r.Title == title || titleCheck) &&
                (r.Description == description || descriptionCheck) &&
                (r.AllowTables.Contains(table) || tableCheck)
            )
            .Select(r => TranslateIntoDto(r))
            .ToListAsync();
        
        return roles;
    }
}