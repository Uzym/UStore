using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.OData.Query;
using Microsoft.AspNetCore.OData.Routing.Controllers;
using TaskMgrAPI.Models;
using TaskMgrAPI.Services.Card;
using TaskMgrAPI.Services.Comment;
using TaskMgrAPI.Services.User;

namespace TaskMgrAPI.Controllers.OData;

public class CardsController : ODataController
{
    private LinkGenerator _linkGenerator;
    private readonly ICardService _cardService;
    private readonly IUserService _userService;
    private readonly ICommentService _commentService;

    public CardsController(ICardService cardService, IUserService userService, ICommentService commentService, 
        LinkGenerator linkGenerator)
    {
        _cardService = cardService;
        _linkGenerator = linkGenerator;
        _userService = userService;
        _commentService = commentService;
    }
    
    [EnableQuery]
    public async Task<ActionResult<IEnumerable<Card>>> Get([FromHeader] string? telegramId)
    {
        
        var items = await _cardService.GetModels(telegramId: telegramId);
        return Ok(items);
    }

    [EnableQuery]
    public async Task<ActionResult<Card>> Get([FromRoute] long key)
    {
        var item = await _cardService.GetModels(id: key);
        if (item.Count == 0)
        {
            return NotFound();
        }

        return Ok(item[0]);
    }
}