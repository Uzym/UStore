using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.OData.Query;
using Microsoft.AspNetCore.OData.Routing.Controllers;
using TaskMgrAPI.Models;
using TaskMgrAPI.Services.Card;
using TaskMgrAPI.Services.UserCard;

namespace TaskMgrAPI.Controllers.OData;

public class UserCardsController : ODataController
{
    private readonly IUserCardService _userCardService;

    public UserCardsController(IUserCardService userCardService)
    {
        _userCardService = userCardService;
    }
    
    [EnableQuery]
    public async Task<ActionResult<IEnumerable<UserCard>>> Get()
    {
        var items = await _userCardService.GetModels();
        return Ok(items);
    }
}