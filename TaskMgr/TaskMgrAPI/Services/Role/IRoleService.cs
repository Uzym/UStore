using TaskMgrAPI.Dtos.Role;

namespace TaskMgrAPI.Services.Role;

public interface IRoleService
{
    public Task<List<RoleDto>> Get(long? id = null, string? title = null, string? description = null,
        string? table = null);
    public Task<List<Models.Role>> GetModels(
        long? id = null
    );
    
}