namespace StoreAPI.Dtos.Firm
{
    public class RequestCreateFirmDto
    {
        public string? title { get; set; }

        public string? description { get; set; }

        public decimal? discount { get; set; }
    }
}
