using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.AspNetCore.Cors;
using StoreAPI.Context;
using StoreAPI.Dtos.Firm;

namespace StoreAPI.Controllers
{
    [Route("[controller]")]
    [ApiController]
    [EnableCors]
    public class FirmController : ControllerBase
    {
        private readonly StoreContext _context;

        public FirmController(StoreContext context)
        {
            _context = context;
        }

        [HttpGet("{firm_id}")]
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

        [HttpDelete("{firm_id}/delete")]
        public async Task<ActionResult<bool>> DeleteFirm(
            long firm_id
            )
        {
            var firm = await _context.Firms
                .FindAsync(firm_id);

            if (firm == null)
            {
                return NotFound();
            }

            _context.Firms.Remove(firm);
            await _context.SaveChangesAsync();

            return Ok(true);
        }

        [HttpGet]
        public async Task<ActionResult<List<FirmDto>>> GetByFilters(
            string? title,
            string? description,
            decimal? discount,
            long? series_id
            )
        {
            var firms = await _context.Firms
                .Include(f => f.Series)
                .Where(f => (title == null || f.Title == title) &&
                            (description == null || f.Description == description) &&
                            (discount == null || f.Discount == discount) &&
                            (series_id == null || f.Series.Any(s => s.SeriesId == series_id)))
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
