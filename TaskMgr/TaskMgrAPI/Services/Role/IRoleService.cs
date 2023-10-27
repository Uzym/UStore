using TaskMgrAPI.Dtos.Role;

namespace TaskMgrAPI.Services.Role;

public interface IRoleService
{
    public Task<List<RoleDto>> Get(long? id = null, string? title = null, string? description = null,
        string? table = null);
    
}