using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using StoreAPI.Context;
using StoreAPI.Dtos.User;

namespace StoreAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class UserController : ControllerBase
    {
        private readonly StoreContext _context;

        public UserController(StoreContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<ActionResult<List<UserDto>>> GetAll()
        {
            var users = await _context.Users
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
        public async Task<ActionResult<UserDto>> GetOne(long user_id)
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
            
            return await GetOne(id[0]);
        }

        [HttpPut("{user_id}/update")]
        public async Task<ActionResult<UserDto>> Update(
            long user_id,
            string? tg_id,
            string? name,
            string? adress,
            string? telephone,
            string? email,
            string? tg_ref,
            bool? admin
            )
        {
            var user = await _context.Users
                .Where(u => u.UserId == user_id)
                .FirstOrDefaultAsync();
            
            if (user == null)
            {
                return NotFound();
            }

            user.TgId = tg_id ?? user.TgId;
            user.Name = name ?? user.Name;
            user.Adress = adress ?? user.Adress;
            user.Telephone = telephone ?? user.Telephone;
            user.Email = email ?? user.Email;
            user.TgRef = tg_ref ?? user.TgRef;
            user.Admin = admin ?? user.Admin;

            await _context.SaveChangesAsync();

            return await GetOne(user_id);
        }
    }
}
