using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Xml.Linq;
using TaskMgrAPI.Context;
using TaskMgrAPI.Dtos.Card;
using TaskMgrAPI.Models;

using TaskMgrAPI.Dtos.User;
using TaskMgrAPI.Services.Card;
using TaskMgrAPI.Services.User;

namespace TaskMgrAPI.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class UserController : ControllerBase
    {
        private readonly IUserService _userService;
        private readonly ICardService _cardService;

        public UserController(IUserService userService, ICardService cardService)
        {
            _userService = userService;
            _cardService = cardService;
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

        [HttpGet("{userId:long}/card")]
        public async Task<ActionResult<List<CardDto>>> GetUserCards(
            long userId,
            [FromQuery(Name="title")] string? title,
            [FromQuery(Name="due")] DateTime? due,
            [FromQuery(Name="complete")] DateTime? complete,
            [FromQuery(Name="tag")] string? tag
        )
        {
            try
            {
                
                return Ok();
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }
    }
}
