using TaskMgrAPI.Dtos.User;

namespace TaskMgrAPI.Services.User
{
    public interface IUserService
    {
        Task<int> Create(string Title, int BossUserId);
        Task<UserDto> Get(int GroupId);
    }
}