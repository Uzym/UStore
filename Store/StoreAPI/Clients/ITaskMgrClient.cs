using StoreAPI.Dtos.Card;
using StoreAPI.Dtos.Comment;

namespace StoreAPI.Clients
{
    public interface ITaskMgrClient
    {
        Task<ResponseGetCardDto> GetCardById(string tg_id, long card_id);

        Task<CardDto> CreateCard(long section_id, string tg_id, RequestCreateCardDto data);

        Task<long> GetSection(string telegramId);

        Task<CardDto> AddComment(string telegramId, long cardId, RequestCreateCommentDto data);

        Task<List<CommentDto>> GetComments(long cardId);
    }
}
