using StoreAPI.Dtos.Series;

namespace StoreAPI.Dtos.Firm
{
    public class FirmDto
    {
        public long firm_id { get; set; }

        public string title { get; set; }

        public string? description { get; set; }

        public decimal discount { get; set; }

        public List<string> tags { get;}
    }
}
