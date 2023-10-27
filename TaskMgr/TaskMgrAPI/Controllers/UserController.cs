using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Xml.Linq;
using TaskMgrAPI.Context;
using TaskMgrAPI.Models;

using TaskMgrAPI.Dtos.User;
using TaskMgrAPI.Services.User;

namespace TaskMgrAPI.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class UserController : ControllerBase
    {
        private readonly IUserService _userService;

        public UserController(IUserService userService)
        {
            _userService = userService;
        }

        [Route("{userId:long}")]
        [HttpGet]
        public async Task<ActionResult<UserDto>> GetOne(long userId)
        {
            try
            {
                var user = await _userService.Get(id: userId);
                if (user.Count == 0)
                {
                    return NotFound();
                }

                return Ok(user[0]);
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }

        [HttpPost]
        public async Task<ActionResult<UserDto>> Create(RequestCreateUserDto data)
        {
            try
            {
                var user = await _userService.Create(data.telegram_id, data.name);
                return Ok(user);
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }
        [HttpGet]
        public async Task<ActionResult<List<UserDto>>> GetAll(
            [FromQuery(Name="telegram_id")] string? telegramId, 
            [FromQuery(Name="name")] string? name)
        {
            try
            {
                var user = await _userService.Get(telegramId: telegramId, name: name);
                return Ok(user);
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }
    }
}
