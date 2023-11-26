namespace TaskMgrAPI.Services.UserCard;

public interface IUserCardService
{
    public Task<List<Models.UserCard>> GetModels(
        long? id = null,
        long? userId = null,
        long? cardId = null,
        long? roleId = null
    );
}