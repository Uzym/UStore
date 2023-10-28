using Microsoft.EntityFrameworkCore;
using TaskMgrAPI.Context;
using TaskMgrAPI.Dtos.Section;
using TaskMgrAPI.Exceptions;
using TaskMgrAPI.Services.Card;
using TaskMgrAPI.Services.User;

namespace TaskMgrAPI.Services.Section;

public class SectionService : ISectionService
{
    private readonly TaskmgrContext _context;
    private readonly IUserService _userService;

    public SectionService(TaskmgrContext context, IUserService userService)
    {
        _context = context;
        _userService = userService;
    }
    
    private static SectionDto TranslateIntoDto(Models.Section section)
    {
        var dto = new SectionDto()
        {
            section_id = section.SectionId,
            title = section.Title,
            project_id = section.ProjectId,
        };
        return dto;
    }

    public async Task<List<string>> UserRights(string telegramId, long sectionId)
    {
        var userId = (await _userService.Get(telegramId: telegramId)).First().user_id;
        var rights = await _context.Database
            .SqlQuery<string>(
                $"select distinct(r2.title) from public.section as s join public.user_project up on s.project_id = up.project_id join public.role r on up.role_id = r.role_id join public.right_role rr on up.role_id = rr.role_id join public.\"right\" r2 on r2.right_id = rr.right_id where up.user_id = {userId} and s.section_id = {sectionId}"
            )
            .ToListAsync();

        return rights;
    }

    public async Task<List<SectionDto>> Get(long? id = null, string? title = null, long? projectId = null)
    {
        var idCheck = id is null;
        var titleCheck = title is null;
        var projectIdCheck = projectId is null;

        var section = await _context.Sections
            .Where(r =>
                (r.SectionId == id || idCheck) &&
                (r.Title == title || titleCheck) &&
                (r.ProjectId == projectId || projectIdCheck)
            )
            .Select(r => TranslateIntoDto(r))
            .ToListAsync();
        
        return section;
    }

    public async Task<SectionDto> Create(string title, long projectId)
    {
        var project = await _context.Projects
            .Where(c => c.ProjectId == projectId)
            .FirstOrDefaultAsync();
        if (project is null)
        {
            throw new NotFoundException($"project {projectId} not found");
        }
        var id = await _context.Database
            .SqlQuery<long>(
                $"INSERT INTO public.section (title, project_id) VALUES ({title}, {projectId}) RETURNING section_id"
            )
            .ToListAsync();
        
        return (await Get(id: id[0])).First();
    }

    public async Task<SectionDto> Update(long id, string? title = null, long? projectId = null)
    {
        var section = await _context.Sections
            .Where(c => c.SectionId == id)
            .FirstOrDefaultAsync();
        if (section is null)
        {
            throw new NotFoundException($"section {id} not found");
        }
        if (title is not null)
        {
            section.Title = title;
        }
        if (projectId is not null)
        {
            var project = await _context.Projects
                .Where(c => c.ProjectId == projectId)
                .FirstOrDefaultAsync();
            if (project is null)
            {
                throw new NotFoundException($"project {projectId} not found");
            }
            section.ProjectId = projectId.Value;
        }
        await _context.SaveChangesAsync();
        return TranslateIntoDto(section);
    }
}