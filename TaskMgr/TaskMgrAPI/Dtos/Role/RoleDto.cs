namespace TaskMgrAPI.Dtos.Role
{
    public class RoleDto
    {
        public long role_id { get; set; }
        public string title { get; set; }
        public string description { get; set; }
        public List<RightDto> rights { get; set; }
    }
}
