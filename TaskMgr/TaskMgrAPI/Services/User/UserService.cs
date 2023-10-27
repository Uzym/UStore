using TaskMgrAPI.Dtos.User;
using TaskMgrAPI.Context;
using TaskMgrAPI.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Internal;

namespace TaskMgrAPI.Services.User;

public class UserService : IUserService
{
    private readonly TaskmgrContext _context;

    public UserService(TaskmgrContext context)
    {
        _context = context;
    }

    private static UserDto TranslateIntoDto(Models.User user)
    {
        var userDto = new UserDto
        {
            user_id = user.UserId,
            name = user.Name ?? "",
            telegram_id = user.TelegramId
        };
        return userDto;
    }
    
    public async Task<List<UserDto>> Get(long? id = null, string? telegramId = null, string? name = null)
    {
        var idCheck = id is null;
        var telegramIdCheck = telegramId is null;
        var nameCheck = name is null;
        var users = await _context.Users
            .Where(u => 
                (u.UserId == id || idCheck) &&
                (u.TelegramId == telegramId || telegramIdCheck) &&
                (u.Name == name || nameCheck))
            .Select(u => TranslateIntoDto(u))
            .ToListAsync();
        
        return users;
    }

    public async Task<UserDto> Create(string telegramId, string name)
    {
        var existUser = await _context.Users
            .Where(u => u.TelegramId == telegramId)
            .FirstOrDefaultAsync();
        if (existUser is not null)
        {
            return TranslateIntoDto(existUser);
        }
        var id = await _context.Database
            .SqlQuery<long>(
                $"INSERT INTO public.user (name, telegram_id) VALUES ({name}, {telegramId}) RETURNING user_id"
            )
            .ToListAsync();
        
        return (await Get(id: id[0])).First();
    }
}