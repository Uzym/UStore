using StoreAPI.Dtos.Card;

namespace StoreAPI.Clients
{
    public interface ITaskMgrClient
    {
        Task<ResponseGetCardDto> GetCardById(string tg_id, long card_id);

        Task<CardDto> CreateCard(long section_id, string tg_id, RequestCreateCardDto data);

        Task<long> GetSection(string telegramId);
    }
}
