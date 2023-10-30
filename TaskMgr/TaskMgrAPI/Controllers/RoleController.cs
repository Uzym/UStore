using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TaskMgrAPI.Context;
using TaskMgrAPI.Dtos.Card;
using TaskMgrAPI.Dtos.Role;
using TaskMgrAPI.Exceptions;
using TaskMgrAPI.Services.Role;

namespace TaskMgrAPI.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class RoleController : Controller
    {
         private readonly IRoleService _roleService;
         public RoleController(IRoleService roleService)
         {
             _roleService = roleService;
         }

         [HttpGet("{roleId:long}")]
         public async Task<ActionResult<RoleDto>> GetById(long roleId)
         {
             try
             {
                 var role = (await _roleService.Get(id: roleId)).FirstOrDefault();
                 if (role is null)
                 {
                     return NotFound();
                 }
                 return Ok(role);
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

         [HttpGet]
         public async Task<ActionResult<List<RoleDto>>> GetAll(
             [FromQuery(Name = "title")] string? title,
             [FromQuery(Name = "description")] string? description,
             [FromQuery(Name = "table")] string? table
         )
         {
             try
             {
                 var roles = await _roleService.Get(
                     title: title,
                     description: description,
                     table: table
                 );
                 return Ok(roles);
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
