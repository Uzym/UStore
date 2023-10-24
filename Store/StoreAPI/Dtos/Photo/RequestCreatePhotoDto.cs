namespace StoreAPI.Dtos.Photo
{
    public class RequestCreatePhotoDto
    {
        public string? name { get; set; }

        public long? product_id { get; set; }

        public long? category_id { get; set; }

        public long? series_id { get; set; }

        public long? firm_id { get; set; }
    }
}
