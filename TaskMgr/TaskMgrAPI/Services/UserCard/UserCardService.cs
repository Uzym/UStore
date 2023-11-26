using Microsoft.EntityFrameworkCore;
using TaskMgrAPI.Context;
using TaskMgrAPI.Services.User;

namespace TaskMgrAPI.Services.UserCard;

public class UserCardService : IUserCardService
{
    private readonly TaskmgrContext _context;
    private readonly IUserService _userService;

    public UserCardService(TaskmgrContext context, IUserService userService)
    {
        _context = context;
        _userService = userService;
    }
    
    public async Task<List<Models.UserCard>> GetModels(long? id = null, long? userId = null, long? cardId = null, long? roleId = null)
    {
        var idCheck = id is null;
        var userIdCheck = userId is null;
        var cardIdCheck = cardId is null;
        var roleIdCheck = roleId is null;
        
        var items = await _context.UserCards
            .Where(c => 
                (c.UserCardId == id || idCheck) &&
                (c.UserId == userId || userIdCheck) &&
                (c.CardId == cardId || cardIdCheck) &&
                (c.RoleId == roleId || roleIdCheck)
            )
            .Include(c => c.Card)
            .Include(c => c.User)
            .Include(c => c.Role)
            .ToListAsync();

        return items;
    }
}