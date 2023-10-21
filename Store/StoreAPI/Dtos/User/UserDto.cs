namespace StoreAPI.Dtos.User
{
    public class UserDto
    {
        public long user_id { get; set; }

        public string tg_id { get; set; }

        public string name { get; set; }

        public string? adress { get; set; }

        public string? telephone { get; set; }

        public string? email { get; set; }

        public string? tg_ref { get; set; }

        public bool admin { get; set; }
    }
}
