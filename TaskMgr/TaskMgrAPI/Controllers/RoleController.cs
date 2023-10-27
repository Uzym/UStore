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
    }
}
