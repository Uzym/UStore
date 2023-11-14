using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.OData.Query;
using Microsoft.AspNetCore.OData.Routing.Controllers;
using TaskMgrAPI.Models;
using TaskMgrAPI.Services.User;

namespace TaskMgrAPI.Controllers.OData;

public class UsersController : ODataController
{
    private LinkGenerator _linkGenerator;
    private readonly IUserService _userService;

    public UsersController(IUserService userService, LinkGenerator linkGenerator)
    {
        _linkGenerator = linkGenerator;
        _userService = userService;
    }
    
    [EnableQuery]
    public async Task<ActionResult<IEnumerable<Comment>>> Get()
    {
        var items = await _userService.GetModels();
        return Ok(items);
    }

    [EnableQuery]
    public async Task<ActionResult<Comment>> Get([FromRoute] long key)
    {
        var item = await _userService.GetModels(id: key);
        if (item.Count == 0)
        {
            return NotFound();
        }

        return Ok(item[0]);
    }
}