using Newtonsoft.Json;
using StoreAPI.Dtos.Card;
using StoreAPI.Dtos.Comment;
using System;
using System.Text;

namespace StoreAPI.Clients
{
    public class TaskMgrClient : ITaskMgrClient
    {
        private readonly HttpClient _client;

        public TaskMgrClient(HttpClient client)
        {
            _client = client;        
        }

        public async Task<CardDto> AddComment(string telegramId, long cardId, RequestCreateCommentDto data)
        {
            _client.DefaultRequestHeaders.Add("Telegram-Id", telegramId);
            var content = new StringContent(
                System.Text.Json.JsonSerializer.Serialize(data),
                Encoding.UTF8,
                "application/json");
            var res = await _client.PostAsync(
                $"{Environment.GetEnvironmentVariable("TASKMGR_API_URL")}/card/{cardId}/comment", 
                content);
            var resJson = await res.Content.ReadAsStringAsync();
            return JsonConvert.DeserializeObject<CardDto>(resJson);
        }

        public async Task<List<CommentDto>> GetComments(long cardId)
        {
            var res = await _client.GetAsync($"{Environment.GetEnvironmentVariable("TASKMGR_API_URL")}/card/{cardId}/comment");
            var resJson = await res.Content.ReadAsStringAsync();
            return JsonConvert.DeserializeObject<List<CommentDto>>(resJson);
        }

        public async Task<CardDto> CreateCard(long section_id, string tg_id, RequestCreateCardDto data)
        {
            _client.DefaultRequestHeaders.Add("Telegram-Id", tg_id);
            var content = new StringContent(
                System.Text.Json.JsonSerializer.Serialize(data),
                Encoding.UTF8,
                "application/json");
            
            var res = await _client.PostAsync(
                $"{Environment.GetEnvironmentVariable("TASKMGR_API_URL")}/section/{section_id}/card", 
                content);
            var resJson = await res.Content.ReadAsStringAsync();
            return JsonConvert.DeserializeObject<CardDto>(resJson);
        }

        public async Task<ResponseGetCardDto> GetCardById(string tg_id, long card_id)
        {
            _client.DefaultRequestHeaders.Add("Telegram-Id", tg_id);
            var res = await _client.GetAsync($"{Environment.GetEnvironmentVariable("TASKMGR_API_URL")}/card/{card_id}");
            var resJson = await res.Content.ReadAsStringAsync();
            return JsonConvert.DeserializeObject<ResponseGetCardDto>(resJson);
        }

        public async Task<long> GetSection(string telegramId)
        {
            Console.WriteLine($"{Environment.GetEnvironmentVariable("TASKMGR_API_URL")}?telegramId={telegramId}");
            var res = await _client.GetAsync($"{Environment.GetEnvironmentVariable("TASKMGR_API_URL")}/Section?telegramId={telegramId}");
            var content = await res.Content.ReadAsStringAsync();
            if (long.TryParse(content, out long result))
            {
                return result;
            }
            else
            {
                throw new InvalidCastException("API response is not a valid long value");
            }
        }
    }
}
