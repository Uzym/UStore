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

namespace TaskMgrAPI.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class CardController : ControllerBase
    {
        private readonly TaskmgrContext _context;
        private LinkGenerator _linkGenerator;

        public CardController(TaskmgrContext context, LinkGenerator linkGenerator)
        {
            _context = context;
            _linkGenerator = linkGenerator;
        }
        
        private async Task<long> AuthUser(string telegramId)
        {
            var userId = await _context.Users.Where(u => u.TelegramId == telegramId).Select(u => u.UserId).FirstAsync();
            return userId;
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
                    
                    var gets = (HttpGetAttribute[]) method.GetCustomAttributes(typeof(HttpGetAttribute), false);
                    var posts = (HttpPostAttribute[]) method.GetCustomAttributes(typeof(HttpPostAttribute), false);
                    var patches = (HttpPatchAttribute[]) method.GetCustomAttributes(typeof(HttpPatchAttribute), false);
                    var puts = (HttpPutAttribute[]) method.GetCustomAttributes(typeof(HttpPutAttribute), false);
                    var delets = (HttpDeleteAttribute[]) method.GetCustomAttributes(typeof(HttpDeleteAttribute), false);
                    var methodHttp = "";
                    var routeUri = "";
                 
                    if (gets.Count() != 0)
                    {
                        methodHttp = "GET";
                        routeUri = gets.Where(g => g.Template != null).Select(g => g.Template.Substring(9)).FirstOrDefault();
                    }
                    else if (posts.Count() != 0)
                    {
                        methodHttp = "POST";
                        routeUri = posts.Where(p => p.Template != null).Select(p => p.Template.Substring(9)).FirstOrDefault();
                    }
                    else if (patches.Count() != 0)
                    {
                        methodHttp = "PATCH";
                        routeUri = patches.Where(p => p.Template != null).Select(p => p.Template.Substring(9)).FirstOrDefault();
                    }
                    else if (puts.Count() != 0)
                    {
                        methodHttp = "PUT";
                        routeUri = puts.Where(p => p.Template != null).Select(p => p.Template.Substring(9)).FirstOrDefault();
                    }
                    else if (delets.Count() != 0)
                    {
                        methodHttp = "DELETE";
                        routeUri = delets.Where(d => d.Template != null).Select(d => d.Template.Substring(9)).FirstOrDefault();
                    }

                    Console.WriteLine(_linkGenerator.GetUriByAction(HttpContext) + routeUri);
                    links.Add(
                        new Link()
                        {
                            Href = _linkGenerator.GetUriByAction(HttpContext) != null ? _linkGenerator.GetUriByAction(HttpContext) + routeUri : "",
                            Rel = method.Name,
                            Method = methodHttp
                        }
                    );
                }
            }
            
            return links;
        }
        private async Task<List<Link>> UserAction(string telegram_id, long cardId)
        {
            var userId = await AuthUser(telegram_id);
            var rights = await _context.Database
                .SqlQuery<string>(
                    $"select distinct(r2.title) from public.user_card as uc join public.card c on c.card_id = uc.card_id join public.section s on s.section_id = c.section_id join public.project p on p.project_id = s.project_id join public.user_project up on p.project_id = up.project_id join public.role r on (r.role_id = up.role_id) or (r.role_id = uc.role_id) join public.right_role rr on r.role_id = rr.role_id join public.\"right\" r2 on r2.right_id = rr.right_id where uc.user_id = {userId} and uc.card_id = {cardId}"
                )
                .ToListAsync();

            var userLinks = CreateProjectLink(cardId, rights);
            
            return userLinks.ToList();
        }
        
        private async Task<CardDto?> GetCardDto(long card_id)
        {
            var card = await _context.Cards
                .FromSql($"SELECT * FROM public.card WHERE card_id = {card_id} LIMIT 1")
                .ToListAsync();
            
            if (card.Count == 0)
            {
                return null;
            }

            var cardDto = new CardDto()
            {
                card_id = card[0].CardId,
                description = card[0].Description ?? "",
                complete = card[0].Complete,
                title = card[0].Title,
                created = card[0].Created,
                due = card[0].Due,
                section_id = card[0].SectionId,
                tags = (card[0].Tags ?? new string[] {}).ToList()
            };
            
            return cardDto;
        }

        //[Route("{card_id}")]
        [HttpGet("{card_id}")]
        public async Task<ActionResult<ResponseGetCardDto>> GetById([FromHeader(Name = "Telegram-Id")] string telegramId, long card_id)
        {
            var cardDto = await GetCardDto(card_id);
            if (cardDto is null)
            {
                return NotFound();
            }
            
            var response = new ResponseGetCardDto()
            {
                card = cardDto,
                links = await UserAction(telegramId, card_id)
            };
            
            return Ok(response);
        }

        // [HttpGet]
        // public async Task<ActionResult<ResponseGetCardDto>> Get([FromHeader(Name = "Telegram-Id")] string telegramId, string? title)
        // {
            

        //     var response = new ResponseGetCardDto()
        //     {
        //         card = cardDto,
        //         links = await UserAction(telegramId, card_id)
        //     };
            
        //     return Ok(response);
        // }
        
        //[Route("{card_id}")]
        [HttpPut("{card_id}")]
        [RightTaskMgr("update_card")]
        public async Task<ActionResult<CardDto>> Update(long card_id, RequestCreateCardDto data)
        {
            var card = await _context.Cards
                .Where(c => c.CardId == card_id)
                .FirstAsync();

            card.Title = data.title;
            card.Description = data.description;
            card.Due = data.due;
            card.Tags = data.tags.ToArray();

            await _context.SaveChangesAsync();
            return Ok(await GetCardDto(card_id));
        }

        [HttpGet("{card_id}/comment")]
        [RightTaskMgr("view_card")]
        public async Task<ActionResult<List<long>>> GetComments(long card_id)
        {
            var ids = await _context.Comments
                .Where(u => u.CardId == card_id)
                .Select(u => u.CommentId)
                .ToListAsync();

            return Ok(ids);
        }

        //[Route("{card_id}/comment")]
        [HttpPost("{card_id}/comment")]
        [RightTaskMgr("add_comment")]
        public async Task<ActionResult<CardDto>> AddComment(long card_id, RequestCreateCommentDto data)
        {
            var id = await _context.Database
                .SqlQuery<long>(
                    $"insert into public.comment (description, user_id, card_id) VALUES ({data.description}, {data.user_id}, {card_id})"
                )
                .ToListAsync();

            return Ok(await GetCardDto(card_id));
        }

        [HttpGet("{card_id}/user")]
        [RightTaskMgr("view_card")]
        public async Task<ActionResult<List<long>>> GetUsers(long card_id)
        {
            var user_roles = await _context.UserCards
                .FromSql($"select * from public.user_card as up where up.card_id = {card_id}")
                .Select(ur => new UserRoleDto()
                {
                    role_id = ur.RoleId,
                    user_id = ur.UserId
                })
                .ToListAsync();

            return Ok(user_roles);
        }

        //[Route("{card_id}/user")]
        [HttpPost("{card_id}/user")]
        [RightTaskMgr("add_comment")]
        public async Task<ActionResult<CardDto>> AddUser(long card_id, RequestAddUser data)
        {
            var id = await _context.Database
                .SqlQuery<long>(
                    $"insert into public.user_card (user_id, card_id, role_id) values ({data.user_id}, {card_id}, {data.role_id})"
                )
                .ToListAsync();
            return Ok(await GetCardDto(card_id));
        }

        //[Route("{card_id}/role")]
        [HttpGet("{card_id}/role")]
        [RightTaskMgr("view_card")]
        public async Task<ActionResult<List<long>>> GetRoles()
        {
            var roles = await _context.Roles
                .FromSql($"select r.role_id from public.role as r where 'card' = any(r.allow_tables::text[])")
                .Select(r => r.RoleId)
                .ToListAsync();

            return Ok(roles);
        }

        //[Route("{card_id}/complete")]
        [HttpPatch("{card_id}/complete")]
        [RightTaskMgr("update_card", "update_card_complete")]
        public async Task<ActionResult<CardDto>> CompleteCard(long card_id)
        {
            var card = await _context.Cards
                .Where(c => c.CardId == card_id)
                .FirstAsync();

            card.Complete = DateTime.Now;

            await _context.SaveChangesAsync();
            return Ok(await GetCardDto(card_id));
        }
        
        //[Route("{card_id}/uncomplete")]
        [HttpPatch("{card_id}/uncomplete")]
        [RightTaskMgr("update_card", "update_card_complete")]
        public async Task<ActionResult<CardDto>> UnCompleteCard(long card_id)
        {
            var card = await _context.Cards
                .Where(c => c.CardId == card_id)
                .FirstAsync();

            card.Complete = null;

            await _context.SaveChangesAsync();
            return Ok(await GetCardDto(card_id));
        }
    }
}
