using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using StoreAPI.Context;
using StoreAPI.Dtos.User;

namespace StoreAPI.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class UserController : ControllerBase
    {
        private readonly StoreContext _context;

        public UserController(StoreContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<ActionResult<List<UserDto>>> Get(string? tg_id)
        {
            var users = await _context.Users
                .Where(u => (tg_id == null || u.TgId == tg_id))
                .Select(u => new UserDto
                {
                    user_id = u.UserId,
                    tg_id = u.TgId,
                    name = u.Name,
                    adress = u.Adress ?? "",
                    telephone = u.Telephone ?? "",
                    email = u.Email ?? "",
                    admin = u.Admin
                })
                .ToListAsync();
            return Ok(users);
        }

        [HttpGet("{user_id}")]
        public async Task<ActionResult<UserDto>> Index(long user_id)
        {
            var user = await _context.Users
                .FromSql($"SELECT * FROM public.user WHERE user_id = {user_id} LIMIT 1")
                .ToListAsync();

            if (user.Count == 0)
            {
                return NotFound();
            }

            return Ok(new UserDto
            {
                user_id = user[0].UserId,
                tg_id = user[0].TgId,
                name = user[0].Name,
                adress = user[0].Adress ?? "",
                telephone = user[0].Telephone ?? "",
                email = user[0].Email ?? "",
                tg_ref = user[0].TgRef ?? "",
                admin = user[0].Admin
            });
        }

        [HttpPost]
        public async Task<ActionResult<UserDto>> Create(RequestCreateUserDto data)
        {
            var id = await _context.Database
                .SqlQuery<long>(
                    $"INSERT INTO public.user (tg_id, name, adress, telephone, email, tg_ref, admin) VALUES ({data.tg_id}, {data.name}, {data.adress}, {data.telephone}, {data.email}, {data.tg_ref}, {data.admin}) RETURNING user_id"
                )
                .ToListAsync();
            
            return await Index(id[0]);
        }

        [HttpPut("{user_id}/update")]
        public async Task<ActionResult<UserDto>> Update(
            long user_id,
            RequestCreateUserDto data
            )
        {
            var user = await _context.Users
                .Where(u => u.UserId == user_id)
                .FirstOrDefaultAsync();
            
            if (user == null)
            {
                return NotFound();
            }

            user.TgId = data.tg_id ?? user.TgId;
            user.Name = data.name ?? user.Name;
            user.Adress = data.adress ?? user.Adress;
            user.Telephone = data.telephone ?? user.Telephone;
            user.Email = data.email ?? user.Email;
            user.TgRef = data.tg_ref ?? user.TgRef;
            user.Admin = data.admin ?? user.Admin;

            await _context.SaveChangesAsync();

            return await Index(user_id);
        }
    }
}
