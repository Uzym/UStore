using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using StoreAPI.Context;
using StoreAPI.Dtos.Firm;

namespace StoreAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class FirmController : ControllerBase
    {
        private readonly StoreContext _context;

        public FirmController(StoreContext context)
        {
            _context = context;
        }

        [HttpGet("firm_id")]
        public async Task<ActionResult<FirmDto>> Index(long firm_id)
        {
            var firm = await _context.Firms
                .FindAsync(firm_id);

            if (firm == null)
            {
                return NotFound();
            }

            return Ok(new FirmDto
            {
                firm_id = firm.FirmId,
                title = firm.Title,
                description = firm.Description,
                discount = firm.Discount
            });
        }

        [HttpPost]
        public async Task<ActionResult<FirmDto>> CreateFirm(RequestCreateFirmDto data)
        {
            var id = await _context.Database
                .SqlQuery<long>(
                $"insert into public.firm (title, description, discount) values ({data.title}, {data.description}, {data.discount}) returning firm_id"
                )
                .ToListAsync();

            return await Index(id[0]);
        }

        [HttpPut("{firm_id}/update")]
        public async Task<ActionResult<FirmDto>> UpdateFirm(
            long firm_id,
            RequestCreateFirmDto data
            )
        {
            var firm = await _context.Firms
                .FindAsync(firm_id);

            if (firm == null)
            {
                return NotFound();
            }

            firm.Title = data.title ?? firm.Title;
            firm.Description = data.description ?? firm.Description;
            firm.Discount = data.discount ?? firm.Discount;

            await _context.SaveChangesAsync();

            return await Index(firm_id);
        }

        [HttpGet]
        public async Task<ActionResult<List<FirmDto>>> GetByFilters(
            string? title,
            string? description,
            decimal? discount
            )
        {
            var firms = await _context.Firms
                .Where(f => (title == null || f.Title == title) &&
                            (description == null || f.Description == description) &&
                            (discount == null || f.Discount == discount))
                .Select(f => new FirmDto
                {
                    firm_id = f.FirmId,
                    title = f.Title,
                    description = f.Description ?? "",
                    discount = f.Discount
                })
                .ToListAsync();
            return Ok(firms);
        }
    }
}
