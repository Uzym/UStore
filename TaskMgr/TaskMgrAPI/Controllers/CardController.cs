using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TaskMgrAPI.Attributes;
using TaskMgrAPI.Context;
using TaskMgrAPI.Models;

using TaskMgrAPI.Dtos.Card;
using TaskMgrAPI.Dtos.Comment;
using TaskMgrAPI.Dtos.Project;
using TaskMgrAPI.Dtos.User;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using TaskMgrAPI.Exceptions;
using TaskMgrAPI.Services.Card;
using TaskMgrAPI.Services.Comment;
using TaskMgrAPI.Services.Role;
using TaskMgrAPI.Services.User;

namespace TaskMgrAPI.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class CardController : ControllerBase
    {
        private LinkGenerator _linkGenerator;
        private readonly ICardService _cardService;
        private readonly IUserService _userService;
        private readonly ICommentService _commentService;

        public CardController(ICardService cardService, IUserService userService, ICommentService commentService, 
            LinkGenerator linkGenerator)
        {
            _cardService = cardService;
            _linkGenerator = linkGenerator;
            _userService = userService;
            _commentService = commentService;
        }
        
        private IEnumerable<Link> CreateProjectLink(long cardId, List<string> rights)
        {
            var links = new List<Link>();
            
            foreach (var method in typeof(CardController).GetMethods())
            {
                var attrs = (RightTaskMgr[]) method.GetCustomAttributes(typeof(RightTaskMgr), false);
                foreach (var attr in attrs)
                {
                    if (attr.Right.Intersect(rights).Count() == 0)
                        continue;
                    
                    var methodHttp = "";
                    if (method.GetCustomAttributes(typeof(HttpGetAttribute), false).Count() != 0)
                        methodHttp = "GET";
                    else if (method.GetCustomAttributes(typeof(HttpPostAttribute), false).Count() != 0)
                        methodHttp = "POST";
                    else if (method.GetCustomAttributes(typeof(HttpPatchAttribute), false).Count() != 0)
                        methodHttp = "PATCH";
                    else if (method.GetCustomAttributes(typeof(HttpPutAttribute), false).Count() != 0)
                        methodHttp = "PUT";
                    else if (method.GetCustomAttributes(typeof(HttpDeleteAttribute), false).Count() != 0)
                        methodHttp = "DELETE";

                    links.Add(
                        new Link()
                        {
                            Href = _linkGenerator.GetPathByAction(method.Name, "Card", new { cardId }) ?? "",
                            Rel = "self",
                            Method = methodHttp
                        }
                    );
                }
            }
            
            return links;
        }
        private async Task<List<Link>> UserAction(string telegramId, long cardId)
        {
            var rights = await _cardService.UserRights(telegramId, cardId);

            var userLinks = CreateProjectLink(cardId, rights);
            
            return userLinks.ToList();
        }

        [HttpGet("{cardId:long}")]
        public async Task<ActionResult<ResponseGetCardDto>> GetById([FromHeader(Name = "Telegram-Id")] string telegramId, long cardId)
        {
            try
            {
                var cardDto = (await _cardService.Get(cardId)).First();

                var response = new ResponseGetCardDto()
                {
                    card = cardDto,
                    links = await UserAction(telegramId, cardId)
                };

                return Ok(response);
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
        
        [HttpPut("{cardId:long}")]
        [RightTaskMgr("update_card")]
        public async Task<ActionResult<CardDto>> Update(long cardId, RequestCreateCardDto data)
        {
            // try
            // {
                var card = await _cardService.Update(cardId,
                    title: data.title,
                    description: data.description,
                    sectionId: data.section_id,
                    due: data.due,
                    tags: data.tags);
                return Ok(card);
            // }
            // catch (NotFoundException ex)
            // {
            //     return NotFound(ex.Message);
            // }
            // catch (Exception ex)
            // {
            //     return BadRequest(ex.Message);
            // }
        }

        [HttpGet("{cardId:long}/comment")]
        [RightTaskMgr("view_card")]
        public async Task<ActionResult<List<long>>> GetComments(long cardId)
        {
            try
            {
                var comments = await _commentService.Get(cardId: cardId);
                return Ok(comments);
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

        //[Route("{card_id}/comment")]
        [HttpPost("{cardId:long}/comment")]
        [RightTaskMgr("add_comment")]
        public async Task<ActionResult<CardDto>> AddComment([FromHeader(Name = "Telegram-Id")] string telegramId, long cardId, RequestCreateCommentDto data)
        {
            try
            {
                var user = (await _userService.Get(telegramId: telegramId)).FirstOrDefault();
                if (user is null)
                {
                    return NotFound();
                }
                var comments = await _commentService.Create(user.user_id, cardId, data.description);
                return Ok(comments);
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

        [HttpGet("{cardId:long}/user")]
        [RightTaskMgr("view_card")]
        public async Task<ActionResult<List<UserRoleDto>>> GetUsers(long cardId)
        {
            try
            {
                var userRoles = await _cardService.UserCard(cardId);
                return Ok(userRoles);
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

        [HttpPost("{cardId:long}/user")]
        [RightTaskMgr("add_comment")]
        public async Task<ActionResult<List<UserRoleDto>>> AddUser(long cardId, RequestAddUser data)
        {
            try
            {
                var userRoles = await _cardService.AddUser(data.user_id, cardId, data.role_id);
                return Ok(userRoles);
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

        [HttpPatch("{cardId:long}/complete")]
        [RightTaskMgr("update_card", "update_card_complete")]
        public async Task<ActionResult<CardDto>> CompleteCard(long cardId)
        {
            try
            {
                var card = await _cardService.Update(cardId,
                    complete: DateTime.Now
                    );
                return Ok(card);
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
        
        [HttpPatch("{cardId:long}/uncomplete")]
        [RightTaskMgr("update_card", "update_card_complete")]
        public async Task<ActionResult<CardDto>> UnCompleteCard(long cardId)
        {
            try
            {
                var card = await _cardService.Update(cardId,
                    complete: null,
                    nullableComplete: true
                );
                return Ok(card);
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
    }
}
