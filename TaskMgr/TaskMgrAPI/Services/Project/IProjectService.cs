using TaskMgrAPI.Dtos.Project;
using TaskMgrAPI.Dtos.User;

namespace TaskMgrAPI.Services.Project;

public interface IProjectService
{
    public Task<List<string>> UserRights(string telegramId, long projectId);
    public Task<List<ProjectDto>> Get(long? id = null, string? title = null, string? description = null, string? telegramId = null);
    public Task<ProjectDto> Create(string title, string description);
    public Task<ProjectDto> Update(long id, string? title = null, string? description = null);
    public Task<List<UserRoleDto>> UserProject(long projectId);
    public Task<List<UserRoleDto>> AddUser(long userId, long projectId, long roleId);
    public Task<List<UserRoleDto>> RemoveUser(long userId, long projectId);
    public Task<List<Models.Project>> GetModels(
        long? id = null
    );
}