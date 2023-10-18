using TaskMgrAPI.Models;

namespace TaskMgrAPI.Dtos.Project;

public class ResponseGetProjectDto
{
    public ProjectDto project { get; set; }
    public List<Link> links { get; set; }
}