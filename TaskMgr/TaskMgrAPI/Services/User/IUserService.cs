namespace TaskMgrAPI.Services.User;
using TaskMgrAPI.Dtos.User;

public interface IUserService
{
    public Task<List<UserDto>> Get(long? id = null, string? telegramId = null, string? name = null);
    public Task<UserDto> Create(string telegramId, string name);
}