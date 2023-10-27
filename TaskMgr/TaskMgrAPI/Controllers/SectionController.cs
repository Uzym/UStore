using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TaskMgrAPI.Attributes;
using TaskMgrAPI.Context;
using TaskMgrAPI.Dtos.Project;
using TaskMgrAPI.Dtos.Section;
using TaskMgrAPI.Models;
using TaskMgrAPI.Dtos.Card;
using TaskMgrAPI.Exceptions;
using TaskMgrAPI.Services.Card;
using TaskMgrAPI.Services.Section;

namespace TaskMgrAPI.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class SectionController : ControllerBase
    {
        private LinkGenerator _linkGenerator;
        private readonly ICardService _cardService;
        private readonly ISectionService _sectionService;

        public SectionController(ICardService cardService, ISectionService sectionService, LinkGenerator linkGenerator)
        {
            _linkGenerator = linkGenerator;
            _cardService = cardService;
            _sectionService = sectionService;
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
        private async Task<List<Link>> UserAction(string telegramId, long sectionId)
        {
            var rights = await _sectionService.UserRights(telegramId, sectionId);

            var userLinks = CreateProjectLink(sectionId, rights);
            
            return userLinks.ToList();
        }

        [Route("{sectionId:long}")]
        [HttpGet]
        public async Task<ActionResult<ResponseGetSectionDto>> GetById([FromHeader(Name = "Telegram-Id")] string telegramId, long sectionId)
        {
            try
            {
                var section = (await _sectionService.Get(sectionId)).First();

                var response = new ResponseGetSectionDto()
                {
                    section = section,
                    links = await UserAction(telegramId, sectionId)
                };

                return Ok(response);
            }
            catch (NotFoundException ex)
            {
                return NotFound(ex.Message);
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }

        [Route("{sectionId:long}")]
        [HttpPut]
        [RightTaskMgr("update_section", "update_project")]
        public async Task<ActionResult<SectionDto>> Update(long sectionId, RequestCreateSectionDto data)
        {
            try
            {
                var section = await _sectionService.Update(sectionId, data.title, data.project_id);
                return Ok(section);
            }
            catch (NotFoundException ex)
            {
                return NotFound(ex.Message);
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }

        [Route("{sectionId:long}/card")]
        [HttpGet]
        [RightTaskMgr("view_section", "view_project")]
        public async Task<ActionResult<List<long>>> GetCards(long sectionId)
        {
            try
            {
                var cardDtos = await _cardService.Get(sectionId: sectionId);
                return Ok(cardDtos);
            }
            catch (NotFoundException ex)
            {
                return NotFound(ex.Message);
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }

        [Route("{sectionId:long}/card")]
        [HttpPost]
        [RightTaskMgr("add_card")]
        public async Task<ActionResult<CardDto>> AddCard([FromHeader(Name = "Telegram-Id")] string telegramId, long sectionId, RequestCreateCardDto data)
        {
            try
            {
                var cardDto = await _cardService.Create(data, sectionId);

                return Ok(cardDto);
            }
            catch (NotFoundException ex)
            {
                return NotFound(ex.Message);
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }
    }
}
