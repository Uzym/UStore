using TaskMgrAPI.Dtos.User;

namespace TaskMgrAPI.Dtos.Project
{
    public class ProjectDto
    {
        public long project_id {  get; set; }
        public string title { get; set; }
        public string description { get; set; }
    }
}
