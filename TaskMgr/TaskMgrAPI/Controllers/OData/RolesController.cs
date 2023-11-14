using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.OData.Query;
using Microsoft.AspNetCore.OData.Routing.Controllers;
using TaskMgrAPI.Models;
using TaskMgrAPI.Services.Comment;
using TaskMgrAPI.Services.Role;

namespace TaskMgrAPI.Controllers.OData;

public class RolesController : ODataController
{
    private LinkGenerator _linkGenerator;
    private readonly IRoleService _roleService;

    public RolesController(IRoleService roleService, LinkGenerator linkGenerator)
    {
        _linkGenerator = linkGenerator;
        _roleService = roleService;
    }
    
    [EnableQuery]
    public async Task<ActionResult<IEnumerable<Comment>>> Get()
    {
        var items = await _roleService.GetModels();
        return Ok(items);
    }

    [EnableQuery]
    public async Task<ActionResult<Comment>> Get([FromRoute] long key)
    {
        var item = await _roleService.GetModels(id: key);
        if (item.Count == 0)
        {
            return NotFound();
        }

        return Ok(item[0]);
    }
}