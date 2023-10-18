namespace TaskMgrAPI.Dtos.Section;

public class SectionDto
{
    public long section_id { set; get; }
    public string title { get; set; }
    public long project_id { get; set; }
}