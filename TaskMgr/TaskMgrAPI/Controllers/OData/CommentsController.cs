using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.OData.Query;
using Microsoft.AspNetCore.OData.Routing.Controllers;
using TaskMgrAPI.Models;
using TaskMgrAPI.Services.Card;
using TaskMgrAPI.Services.Comment;
using TaskMgrAPI.Services.User;

namespace TaskMgrAPI.Controllers.OData;

public class CommentsController : ODataController
{
    private LinkGenerator _linkGenerator;
    private readonly ICommentService _commentService;

    public CommentsController(ICommentService commentService, LinkGenerator linkGenerator)
    {
        _linkGenerator = linkGenerator;
        _commentService = commentService;
    }
    
    [EnableQuery]
    public async Task<ActionResult<IEnumerable<Comment>>> Get()
    {
        var items = await _commentService.GetModels();
        return Ok(items);
    }

    [EnableQuery]
    public async Task<ActionResult<Comment>> Get([FromRoute] long key)
    {
        var item = await _commentService.GetModels(id: key);
        if (item.Count == 0)
        {
            return NotFound();
        }

        return Ok(item[0]);
    }
    
    public async Task<ActionResult<Comment>> Post([FromBody] Comment data)
    {
        var comment = await _commentService.Create(
            userId: data.UserId,
            cardId: data.CardId,
            description: data.Description);
        
        var item = await _commentService.GetModels(id: comment.comment_id);
        if (item.Count == 0)
        {
            return NotFound();
        }

        return Ok(item[0]);
    }
}