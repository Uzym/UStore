using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.OData.Query;
using Microsoft.AspNetCore.OData.Routing.Controllers;
using TaskMgrAPI.Models;
using TaskMgrAPI.Services.Project;

namespace TaskMgrAPI.Controllers.OData;

public class ProjectsController : ODataController
{
    private LinkGenerator _linkGenerator;
    private readonly IProjectService _projectService;

    public ProjectsController(IProjectService projectService, LinkGenerator linkGenerator)
    {
        _linkGenerator = linkGenerator;
        _projectService = projectService;
    }
    
    [EnableQuery]
    public async Task<ActionResult<IEnumerable<Comment>>> Get()
    {
        var items = await _projectService.GetModels();
        return Ok(items);
    }

    [EnableQuery]
    public async Task<ActionResult<Comment>> Get([FromRoute] long key)
    {
        var item = await _projectService.GetModels(id: key);
        if (item.Count == 0)
        {
            return NotFound();
        }

        return Ok(item[0]);
    }
}