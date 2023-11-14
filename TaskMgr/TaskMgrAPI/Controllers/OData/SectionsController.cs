using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.OData.Query;
using Microsoft.AspNetCore.OData.Routing.Controllers;
using TaskMgrAPI.Models;
using TaskMgrAPI.Services.Section;

namespace TaskMgrAPI.Controllers.OData;

public class SectionsController : ODataController
{
    private LinkGenerator _linkGenerator;
    private readonly ISectionService _sectionService;

    public SectionsController(ISectionService sectionService, LinkGenerator linkGenerator)
    {
        _linkGenerator = linkGenerator;
        _sectionService = sectionService;
    }
    
    [EnableQuery]
    public async Task<ActionResult<IEnumerable<Comment>>> Get()
    {
        var items = await _sectionService.GetModels();
        return Ok(items);
    }

    [EnableQuery]
    public async Task<ActionResult<Comment>> Get([FromRoute] long key)
    {
        var item = await _sectionService.GetModels(id: key);
        if (item.Count == 0)
        {
            return NotFound();
        }

        return Ok(item[0]);
    }
}