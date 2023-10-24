namespace StoreAPI.Dtos.Series
{
    public class SeriesDto
    {
        public long series_id { get; set; }

        public string title { get; set; }

        public string? description { get; set; }

        public decimal discount { get; set; }

        public long firm_id { get; set; }
    }
}
