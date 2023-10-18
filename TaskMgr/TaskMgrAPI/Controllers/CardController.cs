using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TaskMgrAPI.Context;
using TaskMgrAPI.Models;

using TaskMgrAPI.Dtos.Card;
using TaskMgrAPI.Dtos.Comment;
using TaskMgrAPI.Dtos.Project;
using TaskMgrAPI.Dtos.User;

namespace TaskMgrAPI.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class CardController : ControllerBase
    {
        private readonly TaskmgrContext _context;

        public CardController(TaskmgrContext context)
        {
            _context = context;
        }

        [Route("{card_id}")]
        [HttpGet]
        public async Task<ActionResult<CardDto>> Index(long card_id)
        {
            var card = await _context.Cards
                .Where(c => c.CardId == card_id)
                .FirstAsync();

            var cardDto = new CardDto()
            {
                card_id = card.CardId,
                description = card.Description ?? "",
                complete = card.Complete,
                title = card.Title,
                created = card.Created,
                due = card.Due,
                section_id = card.SectionId,
                tags = (card.Tags ?? new string[] {}).ToList()
            };
            
            return Ok(cardDto);
        }

        [Route("{card_id}")]
        [HttpPut]
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
            return await Index(card_id);
        }

        [Route("{card_id}/comment")]
        [HttpGet]
        public async Task<ActionResult<List<long>>> GetComments(long card_id)
        {
            var ids = await _context.Comments
                .Where(u => u.CardId == card_id)
                .Select(u => u.CommentId)
                .ToListAsync();

            return Ok(ids);
        }

        [Route("{card_id}/comment")]
        [HttpPost]
        public async Task<ActionResult<CardDto>> AddComment(long card_id, RequestCreateCommentDto data)
        {
            var id = await _context.Database
                .SqlQuery<long>(
                    $"insert into public.comment (description, user_id, card_id) VALUES ({data.description}, {data.user_id}, {card_id})"
                )
                .ToListAsync();

            return await Index(card_id);
        }

        [Route("{card_id}/user")]
        [HttpGet]
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

        [Route("{card_id}/user")]
        [HttpPost]
        public async Task<ActionResult<CardDto>> AddUser(long card_id, RequestAddUser data)
        {
            var id = await _context.Database
                .SqlQuery<long>(
                    $"insert into public.user_card (user_id, card_id, role_id) values ({data.user_id}, {card_id}, {data.role_id})"
                )
                .ToListAsync();
            return await Index(card_id);
        }

        [Route("{card_id}/role")]
        [HttpGet]
        public async Task<ActionResult<List<long>>> GetRoles()
        {
            var roles = await _context.Roles
                .FromSql($"select r.role_id from public.role as r where 'card' = any(r.allow_tables::text[])")
                .Select(r => r.RoleId)
                .ToListAsync();

            return Ok(roles);
        }

        [Route("{card_id}/complete")]
        [HttpPatch]
        public async Task<ActionResult<CardDto>> CompleteCard(long card_id)
        {
            var card = await _context.Cards
                .Where(c => c.CardId == card_id)
                .FirstAsync();

            card.Complete = DateTime.Now;

            await _context.SaveChangesAsync();
            return await Index(card_id);
        }
        
        [Route("{card_id}/uncomplete")]
        [HttpPatch]
        public async Task<ActionResult<CardDto>> UnCompleteCard(long card_id)
        {
            var card = await _context.Cards
                .Where(c => c.CardId == card_id)
                .FirstAsync();

            card.Complete = null;

            await _context.SaveChangesAsync();
            return await Index(card_id);
        }
    }
}
