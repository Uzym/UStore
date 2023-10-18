using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Xml.Linq;
using TaskMgrAPI.Context;
using TaskMgrAPI.Models;

using TaskMgrAPI.Dtos.User;

namespace TaskMgrAPI.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class UserController : ControllerBase
    {
        private readonly TaskmgrContext _context;

        public UserController(TaskmgrContext context)
        {
            _context = context;
        }

        [Route("{user_id}")]
        [HttpGet]
        public async Task<ActionResult<UserDto>> GetOne(long user_id)
        {
            var user = await _context.Users
                .FromSql($"SELECT * FROM public.user WHERE user_id = {user_id} LIMIT 1")
                .ToListAsync();

            if (user.Count == 0)
            {
                return NotFound();
            }

            var userDto = new UserDto
            {
                user_id = user[0].UserId,
                name = user[0].Name ?? "",
                telegram_id = user[0].TelegramId
            };

            return Ok(userDto);
        }

        [HttpPost]
        public async Task<ActionResult<UserDto>> Create(RequestCreateUserDto data)
        {
            var id = await _context.Database
                .SqlQuery<long>(
                    $"INSERT INTO public.user (name, telegram_id) VALUES ({data.name}, {data.telegram_id}) RETURNING user_id"
                )
                .ToListAsync();

            return await GetOne(id[0]);
        }
        [HttpGet]
        public async Task<ActionResult<List<UserDto>>> GetAll()
        {
            var users = await _context.Users
                .Select(u => new UserDto
                {
                    user_id = u.UserId,
                    name = u.Name ?? "",
                    telegram_id = u.TelegramId
                })
                .ToListAsync();

            return Ok(users);
        }
    }
}
