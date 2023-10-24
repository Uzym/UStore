namespace StoreAPI.Dtos.Category
{
    public class RequestCreateCategoryDto
    {
        public string? title { get; set; }

        public string? description { get; set; }

        public decimal? discount { get; set; }
    }
}
