namespace TaskMgrAPI.Dtos.Comment;

public class RequestCreateCommentDto
{
    public string description { get; set; }
    public long user_id { get; set; }
}