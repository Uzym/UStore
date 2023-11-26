using TaskMgrAPI.Dtos.Card;
using TaskMgrAPI.Dtos.User;

namespace TaskMgrAPI.Services.Card;

public interface ICardService
{
    public Task<List<string>> UserRights(string telegramId, long cardId);
    public Task<List<Models.Card>> GetModels(
        long? id = null,
        string? telegramId = null
    );
    public Task<List<CardDto>> Get(
        long? id = null, 
        string? title = null, 
        string? description = null, 
        long? sectionId = null,
        DateTime? due = null,
        DateTime? complete = null, 
        string? tags = null
    );
    public Task<CardDto> Create(RequestCreateCardDto data, long sectionId);
    public Task<CardDto> Update(
        long id, 
        string? title = null, 
        string? description = null, 
        long? sectionId = null,
        DateTime? due = null,
        DateTime? complete = null, 
        List<string>? tags = null,
        bool nullableComplete = false
    );
    public Task<List<UserRoleDto>> UserCard(long cardId);
    public Task<List<UserRoleDto>> AddUser(long userId, long cardId, long roleId);
    public Task<List<UserRoleDto>> RemoveUser(long userId, long cardId);
    
    public Task<CardDto> Cards(
        string? title = null, 
        string? description = null, 
        long? sectionId = null,
        DateTime? due = null,
        DateTime? complete = null, 
        string? tag = null,
        long? userId = null
    );
}