using TaskMgrAPI.Models;

namespace TaskMgrAPI.Dtos.Card;

public class ResponseGetCardDto
{
    public CardDto card { get; set; }
    public List<Link> links { get; set; }
}