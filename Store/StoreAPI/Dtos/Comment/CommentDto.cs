namespace StoreAPI.Dtos.Comment
{
    public class CommentDto
    {
        public long comment_id { get; set; }
        public string description { get; set; }
        public long user_id { get; set; }
        public long card_id { get; set; }
    }
}
