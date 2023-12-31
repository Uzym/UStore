﻿namespace StoreAPI.Dtos.Product
{
    public class RequestCreateProductDto
    {
        public long? category_id { get; set; }

        public long? series_id { get; set;}

        public string? title { get; set; }

        public string? description { get; set; }

        public decimal? cost { get; set; }

        public TimeSpan? delivery_time { get; set; }

        public decimal? discount { get; set; }
    }
}
