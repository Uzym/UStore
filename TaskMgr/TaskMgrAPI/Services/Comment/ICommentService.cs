using TaskMgrAPI.Dtos.Comment;

namespace TaskMgrAPI.Services.Comment;

public interface ICommentService
{
    public Task<List<CommentDto>> Get(long? id = null, string? description = null, long? userId = null, long? cardId = null);
    public Task<CommentDto> Create(long userId, long cardId, string description);
}