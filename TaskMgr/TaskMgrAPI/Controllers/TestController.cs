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

        [Route("test")]
        [HttpGet]
        public async Task<ActionResult<string>> Test()
        {
            return Ok("12345");
        }

        [HttpGet]
        public async Task<ActionResult<long>> GetRoles()
        {
            //var res = await _context.Roles
            //    .FirstOrDefaultAsync();
            var id = await _context.Database
                .SqlQuery<long>($"SELECT role_id FROM public.role")
                .ToListAsync();
            return Ok(id[0]);
        }
    }
}
