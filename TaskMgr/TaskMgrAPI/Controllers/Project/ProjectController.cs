// using Microsoft.AspNetCore.Http;
// using Microsoft.AspNetCore.Mvc;
// using Microsoft.EntityFrameworkCore;
// using TaskMgrAPI.Context;
// using TaskMgrAPI.Dtos.User;
// using TaskMgrAPI.Models;
//
// using TaskMgrAPI.Dtos.Role;
// using TaskMgrAPI.Dtos.Project;
//
// namespace TaskMgrAPI.Controllers.Project;
//
// [Route("[controller]")]
// [ApiController]
// public class ProjectController
// {
//     private readonly TaskmgrContext _context;
//
//     public ProjectController(TaskmgrContext context)
//     {
//         _context = context;
//     }
//     
//     [HttpPost]
//     public async Task<ActionResult<long>> Create(RequestCreateProjectDto data)
//     {
//         var id = await _context.Database
//             .SqlQuery<long>(
//                 $"INSERT INTO public.project (title, description) VALUES ({data.title}, {data.description}) RETURNING project_id"
//             )
//             .ToListAsync();
//
//         return id[0];
//     }
//
//     [HttpGet]
//     public async Task<ActionResult<List<long>>> Get()
//     {
//         var projects = await _context.Projects
//             .Select(u => u.ProjectId)
//             .ToListAsync();
//
//         return projects;
//     }
// }