namespace TaskMgrAPI.Dtos.Card;

public class RequestCreateCardDto
{
    public string title { get; set; }
    public string description { get; set; }
    public DateTime? due { get; set; }
    public List<string> tags { get; set; }
    public long section_id { get; set; }
}