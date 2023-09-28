using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TaskMgrAPI.Context;
using TaskMgrAPI.Models;

namespace TaskMgrAPI.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class TestController : ControllerBase
    {
        private readonly TaskmgrContext _context;

        public TestController(TaskmgrContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<ActionResult<Role>> GetRoles()
        {
            var res = await _context.Roles
                .FirstOrDefaultAsync();
            return Ok(res);
        }
    }
}
