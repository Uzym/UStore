using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TaskMgrAPI.Attributes;
using TaskMgrAPI.Context;
using TaskMgrAPI.Dtos.Project;
using TaskMgrAPI.Dtos.Section;
using TaskMgrAPI.Models;
using TaskMgrAPI.Dtos.Card;

namespace TaskMgrAPI.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class SectionController : ControllerBase
    {
        private readonly TaskmgrContext _context;
        private LinkGenerator _linkGenerator;

        public SectionController(TaskmgrContext context, LinkGenerator linkGenerator)
        {
            _context = context;
            _linkGenerator = linkGenerator;
        }
        
        private async Task<long> AuthUser(string telegramId)
        {
            var userId = await _context.Users.Where(u => u.TelegramId == telegramId).Select(u => u.UserId).FirstAsync();
            return userId;
        }

        private IEnumerable<Link> CreateProjectLink(long section_id, List<string> rights)
        {
            var links = new List<Link>();
            
            foreach (var method in typeof(SectionController).GetMethods())
            {
                var attrs = (RightTaskMgr[]) method.GetCustomAttributes(typeof(RightTaskMgr), false);
                foreach (var attr in attrs)
                {
                    if (attr.Right.Intersect(rights).Count() == 0)
                        continue;
                    
                    var methodHttp = "";
                    if (method.GetCustomAttributes(typeof(HttpGetAttribute), false).Count() != 0)
                        methodHttp = "GET";
                    else if (method.GetCustomAttributes(typeof(HttpPostAttribute), false).Count() != 0)
                        methodHttp = "POST";
                    else if (method.GetCustomAttributes(typeof(HttpPatchAttribute), false).Count() != 0)
                        methodHttp = "PATCH";
                    else if (method.GetCustomAttributes(typeof(HttpPutAttribute), false).Count() != 0)
                        methodHttp = "PUT";
                    else if (method.GetCustomAttributes(typeof(HttpDeleteAttribute), false).Count() != 0)
                        methodHttp = "DELETE";

                    links.Add(
                        new Link()
                        {
                            Href = _linkGenerator.GetUriByAction(HttpContext, method.Name, values: new { section_id }) ?? "",
                            Rel = "self",
                            Method = methodHttp
                        }
                    );
                }
            }
            
            return links;
        }
        private async Task<List<Link>> UserAction(string telegram_id, long section_id)
        {
            var userId = await AuthUser(telegram_id);
            var rights = await _context.Database
                .SqlQuery<string>(
                    $"select distinct(r2.title) from public.section as s join public.user_project up on s.project_id = up.project_id join public.role r on up.role_id = r.role_id join public.right_role rr on up.role_id = rr.role_id join public.\"right\" r2 on r2.right_id = rr.right_id where up.user_id = {userId} and s.section_id = {section_id}"
                )
                .ToListAsync();

            var userLinks = CreateProjectLink(section_id, rights);
            
            return userLinks.ToList();
        }
        
        private async Task<SectionDto?> GetSectionDto(long section_id)
        {
            var section = await _context.Sections
                .FromSql($"SELECT * FROM public.section WHERE section_id = {section_id} LIMIT 1")
                .ToListAsync();
            
            if (section.Count == 0)
            {
                return null;
            }

            var sectionDto = new SectionDto()
            {
                project_id = section[0].ProjectId,
                title = section[0].Title,
                section_id = section[0].SectionId
            };
            
            return sectionDto;
        }

        [Route("{section_id}")]
        [HttpGet]
        public async Task<ActionResult<ResponseGetSectionDto>> GetById([FromHeader(Name = "Telegram-Id")] string telegramId, long section_id)
        {
            var sectionDto = await GetSectionDto(section_id);
            if (sectionDto is null)
            {
                return NotFound();
            }
            
            var response = new ResponseGetSectionDto()
            {
                section = sectionDto,
                links = await UserAction(telegramId, section_id)
            };
            
            return Ok(response);
        }

        [Route("{section_id}")]
        [HttpPut]
        [RightTaskMgr("update_section", "update_project")]
        public async Task<ActionResult<SectionDto>> Update(long section_id, RequestCreateSectionDto data)
        {
            var id = await _context.Database
                .SqlQuery<long>(
                    $"update public.section as p set title = {data.title} where p.section_id = {section_id}"
                )
                .ToListAsync();

            return Ok(await GetSectionDto(section_id));
        }

        [Route("{section_id}/card")]
        [HttpGet]
        [RightTaskMgr("view_section", "view_project")]
        public async Task<ActionResult<List<long>>> GetCards(long section_id)
        {
            var ids = await _context.Cards
                .FromSql($"select * from public.card as up where up.section_id = {section_id}")
                .Select(c => c.CardId)
                .ToListAsync();

            return Ok(ids);
        }

        [Route("{section_id}/card")]
        [HttpPost]
        [RightTaskMgr("add_card")]
        public async Task<ActionResult<SectionDto>> AddCard(long section_id, RequestCreateCardDto data)
        {
            var model = new Models.Card()
            {
                SectionId = section_id,
                Title = data.title,
                Description = data.description,
                Due = data.due,
                Created = DateTime.Now,
                Tags = data.tags.ToArray()
            };
            await _context.Cards.AddAsync(model);
            await _context.SaveChangesAsync();
            
            return Ok(await GetSectionDto(section_id));
        }
    }
}
