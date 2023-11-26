namespace TaskMgrAPI.Services.UserProject;

public interface IUserProjectService
{
    public Task<List<Models.UserProject>> GetModels(
        long? id = null,
        long? userId = null,
        long? projectId = null,
        long? roleId = null
    );
}