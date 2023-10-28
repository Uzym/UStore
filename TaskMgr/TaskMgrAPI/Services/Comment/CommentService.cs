using Microsoft.EntityFrameworkCore;
using TaskMgrAPI.Context;
using TaskMgrAPI.Dtos.Comment;
using TaskMgrAPI.Exceptions;

namespace TaskMgrAPI.Services.Comment;

public class CommentService : ICommentService
{
    private readonly TaskmgrContext _context;
    public CommentService(TaskmgrContext context)
    {
        _context = context;
    }
    
    private static CommentDto TranslateIntoDto(Models.Comment comment)
    {
        var dto = new CommentDto()
        {
            comment_id = comment.CommentId,
            description = comment.Description ?? "",
            card_id = comment.CardId,
            user_id = comment.UserId
        };
        return dto;
    }

    public async Task<List<CommentDto>> Get(long? id = null, string? description = null, long? userId = null, long? cardId = null)
    {
        var idCheck = id is null;
        var descriptionCheck = description is null;
        var userIdCheck = userId is null;
        var cardIdCheck = cardId is null;
        
        var comments = await _context.Comments
            .Where(r =>
                (r.CommentId == id || idCheck) &&
                (r.Description == description || descriptionCheck) &&
                (r.UserId == userId || userIdCheck) &&
                (r.CardId == cardId || cardIdCheck)
            )
            .Select(r => TranslateIntoDto(r))
            .ToListAsync();
        
        return comments;
    }

    public async Task<CommentDto> Create(long userId, long cardId, string description)
    {
        var user = await _context.Users
            .Where(u => u.UserId == userId)
            .FirstOrDefaultAsync();
        if (user is null)
        {
            throw new NotFoundException($"user {userId} not found");
        }
        var card = await _context.Cards
            .Where(u => u.CardId == cardId)
            .FirstOrDefaultAsync();
        if (card is null)
        {
            throw new NotFoundException($"card {cardId} not found");
        }
        
        var model = new Models.Comment()
        {
            UserId = userId,
            CardId = cardId,
            Description = description
        };
        await _context.Comments.AddAsync(model);
        await _context.SaveChangesAsync();
            
        return TranslateIntoDto(model);
    }
}