using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
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

        public SectionController(TaskmgrContext context)
        {
            _context = context;
        }

        [Route("{section_id}")]
        [HttpGet]
        public async Task<ActionResult<SectionDto>> Index(long section_id)
        {
            var section = await _context.Sections
                .FromSql($"SELECT * FROM public.section WHERE section_id = {section_id} LIMIT 1")
                .ToListAsync();

            if (section.Count == 0)
            {
                return NotFound();
            }

            var sectionDto = new SectionDto()
            {
                project_id = section[0].ProjectId,
                title = section[0].Title,
                section_id = section[0].SectionId
            };

            return Ok(sectionDto);
        }

        [Route("{section_id}")]
        [HttpPut]
        public async Task<ActionResult<SectionDto>> Update(long section_id, RequestCreateSectionDto data)
        {
            var id = await _context.Database
                .SqlQuery<long>(
                    $"update public.section as p set title = {data.title} where p.section_id = {section_id}"
                )
                .ToListAsync();

            return await Index(section_id);
        }

        [Route("{section_id}/card")]
        [HttpGet]
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
            
            return await Index(section_id);
        }
    }
}
