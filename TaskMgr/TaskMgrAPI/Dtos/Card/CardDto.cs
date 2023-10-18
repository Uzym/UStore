namespace TaskMgrAPI.Dtos.Card;

public class CardDto
{
    public long card_id { get; set; }
    public string title { get; set; }
    public string description { get; set; }
    public DateTime? due { get; set; }
    public DateTime? complete { get; set; }
    public List<string> tags { get; set; }
    public DateTime created { get; set; }
    public long section_id { get; set; }
}