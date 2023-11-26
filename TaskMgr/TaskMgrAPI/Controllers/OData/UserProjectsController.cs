using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.OData.Query;
using Microsoft.AspNetCore.OData.Routing.Controllers;
using TaskMgrAPI.Models;
using TaskMgrAPI.Services.UserProject;

namespace TaskMgrAPI.Controllers.OData;

public class UserProjectsController : ODataController
{
    private readonly IUserProjectService _userProjectService;

    public UserProjectsController(IUserProjectService userProjectService)
    {
        _userProjectService = userProjectService;
    }

    [EnableQuery]
    public async Task<ActionResult<IEnumerable<UserProject>>> Get()
    {
        var items = await _userProjectService.GetModels();
        return Ok(items);
    }
}