using Microsoft.EntityFrameworkCore;
using TaskMgrAPI.Context;
using TaskMgrAPI.Services.User;
using TaskMgrAPI.Dtos.Card;
using TaskMgrAPI.Dtos.User;
using TaskMgrAPI.Exceptions;

namespace TaskMgrAPI.Services.Card;

public class CardService : ICardService
{
    private readonly TaskmgrContext _context;
    private readonly IUserService _userService;

    public CardService(TaskmgrContext context, IUserService userService)
    {
        _context = context;
        _userService = userService;
    }
    
    private static CardDto TranslateIntoDto(Models.Card card)
    {
        var dto = new CardDto()
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
        return dto;
    }

    public async Task<List<string>> UserRights(string telegramId, long cardId)
    {
        var userId = (await _userService.Get(telegramId: telegramId)).First().user_id;
        var rights = await _context.Database
            .SqlQuery<string>(
                $"select distinct(r2.title) from public.user_project as up left join public.project p on up.project_id = p.project_id left join public.section s on p.project_id = s.project_id left join public.card c on s.section_id = c.section_id left join public.user_card uc on c.card_id = uc.card_id join public.role r on (r.role_id = up.role_id) or (r.role_id = uc.role_id) join public.right_role rr on r.role_id = rr.role_id join public.\"right\" r2 on r2.right_id = rr.right_id where c.card_id = {cardId} and (up.user_id = {userId} or uc.user_id = {userId})"
            )
            .ToListAsync();
        return rights;
    }

    public async Task<List<Models.Card>> GetModels(long? id = null, string? telegramId = null)
    {
        var idCheck = id is null;
        var telegramCheck = telegramId is null;
        var cards = await _context.Cards
            .Where(c => 
                (c.CardId == id || idCheck)
            )
            .Include(c => c.Comments)
            .Include(c => c.Section)
            .ThenInclude(c => c.Project)
            .ThenInclude(c => c.UserProjects)
            .Include(c => c.UserCards)
            .ToListAsync();

        return cards;
    }

    public async Task<List<CardDto>> Get(long? id = null, string? title = null, string? description = null, long? sectionId = null,
        DateTime? due = null, DateTime? complete = null, string? tag = null)
    {
        var idCheck = id is null;
        var titleCheck = title is null;
        var descriptionCheck = description is null;
        var sectionIdCheck = sectionId is null;
        var dueCheck = due is null;
        var completeCheck = complete is null;
        var tagCheck = tag is null;
        
        var cards = await _context.Cards
            .Where(r =>
                (r.CardId == id || idCheck) &&
                (r.Title == title || titleCheck) &&
                (r.Description == description || descriptionCheck) &&
                (r.SectionId == sectionId || sectionIdCheck) &&
                (r.Due == due || dueCheck) &&
                (r.Complete == complete || completeCheck) &&
                ((r.Tags ?? new string[] {}).Contains(tag) || tagCheck)
            )
            .Select(r => TranslateIntoDto(r))
            .ToListAsync();
        
        return cards;
    }

    public async Task<CardDto> Create(RequestCreateCardDto data, long sectionId)
    {
        var model = new Models.Card()
        {
            SectionId = sectionId,
            Title = data.title,
            Description = data.description,
            Due = data.due,
            Created = DateTime.Now,
            Tags = data.tags.ToArray()
        };
        await _context.Cards.AddAsync(model);
        await _context.SaveChangesAsync();
            
        return TranslateIntoDto(model);
    }

    public async Task<CardDto> Update(long id, string? title = null, string? description = null, long? sectionId = null,
        DateTime? due = null, DateTime? complete = null, List<string>? tags = null, bool nullableComplete = false)
    {
        var card = await _context.Cards
            .Where(c => c.CardId == id)
            .FirstOrDefaultAsync();
        if (card is null)
        {
            throw new NotFoundException($"card {id} not found");
        }
        if (sectionId is not null)
        {
            var section = await _context.Sections
                .Where(s => s.SectionId == sectionId)
                .FirstAsync();
            if (section is null)
            {
                throw new NotFoundException($"section {sectionId} not found");
            }
            card.SectionId = sectionId.Value;
        }
        if (title is not null)
        {
            card.Title = title;
        }
        if (description is not null)
        {
            card.Description = description;
        }
        if (due is not null)
        {
            card.Due = due;
        }
        if (complete is not null || nullableComplete)
        {
            card.Complete = complete;
        }
        if (tags is not null)
        {
            card.Tags = tags.ToArray();
        }

        await _context.SaveChangesAsync();
        return TranslateIntoDto(card);
    }

    public async Task<List<UserRoleDto>> UserCard(long cardId)
    {
        var userRoles = await _context.UserCards
            .FromSql($"select * from public.user_card as up where up.card_id = {cardId}")
            .Select(ur => new UserRoleDto()
            {
                role_id = ur.RoleId,
                user_id = ur.UserId
            })
            .ToListAsync();

        return userRoles;
    }

    public async Task<List<UserRoleDto>> AddUser(long userId, long cardId, long roleId)
    {
        var id = await _context.Database
            .SqlQuery<long>(
                $"insert into public.user_card (user_id, card_id, role_id) values ({userId}, {cardId}, {roleId})"
            )
            .ToListAsync();
        return await UserCard(cardId);
    }

    public async Task<List<UserRoleDto>> RemoveUser(long userId, long cardId)
    {
        var id = await _context.Database
            .SqlQuery<long>(
                $"delete FROM public.user_card where card_id ={cardId} and user_id = {userId}"
            )
            .ToListAsync();
        return await UserCard(cardId);
    }

    public Task<CardDto> Cards(string? title = null, string? description = null, long? sectionId = null, DateTime? due = null,
        DateTime? complete = null, string? tag = null, long? userId = null)
    {
        // var cards = await _context.Cards
        //     .Include(c => c.UserCards)
        //     .Where(c => c.UserCards.Any(uc => uc.UserId == userId) || userId == null)
        //     .Where(c => 
        //         (c.Title) || )
        throw new NotImplementedException();
    }
}