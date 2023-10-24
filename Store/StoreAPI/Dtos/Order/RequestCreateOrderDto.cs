namespace StoreAPI.Dtos.Order
{
    public class RequestCreateOrderDto
    {
        public long? user_id { get; set; }

        public long? card_id { get; set; }

        public bool? finished { get; set; }

        public decimal? price { get; set; }
    }
}
