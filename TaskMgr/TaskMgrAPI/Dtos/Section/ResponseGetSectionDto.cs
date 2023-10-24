using TaskMgrAPI.Models;

namespace TaskMgrAPI.Dtos.Section;

public class ResponseGetSectionDto
{
    public SectionDto section { get; set; }
    public List<Link> links { get; set; }
}