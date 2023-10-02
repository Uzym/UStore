using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TaskMgrAPI.Context;
using TaskMgrAPI.Models;

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

        [Get]
        public async Task<ActionResult<UserDto>> Get(int id)
        {
            try
            {
                
                return Ok(user);
            }
            catch (NotFoundException ex)
            {
                return NotFound(ex.Message);
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }

        [HttpPost]
        public async Task<ActionResult<UserDto>> Create(RequestCreateUserDto data)
        {

        }

        [HttpGet]
        public async Task<ActionResult<long>> GetRoles()
        {
            //var res = await _context.Roles
            //    .FirstOrDefaultAsync();
            var id = await _context.Database
                .SqlQuery<long>($"SELECT role_id FROM public.role")
                .ToListAsync();
            return Ok(id[0]);
        }
    }
}
