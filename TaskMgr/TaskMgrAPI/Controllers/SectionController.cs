using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TaskMgrAPI.Context;
using TaskMgrAPI.Models;

namespace TaskMgrAPI.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class SectionController : ControllerBase
    {
        private readonly TaskmgrContext _context;

        public SectionController(TaskmgrContext context)
        {
            _context = context;
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
