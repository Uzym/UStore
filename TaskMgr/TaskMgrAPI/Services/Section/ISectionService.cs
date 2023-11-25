using TaskMgrAPI.Dtos.Section;

namespace TaskMgrAPI.Services.Section;

public interface ISectionService
{
    public Task<List<string>> UserRights(string telegramId, long sectionId);
    Task<List<SectionDto>> Get(long? id = null, string? title = null, long? projectId = null);
    Task<SectionDto> Create(string title, long projectId);
    Task<SectionDto> Update(long id, string? title = null, long? projectId = null);
    Task<long> GetSectionId(string telegramId);
}