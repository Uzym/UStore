using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using StoreAPI.Context;
using StoreAPI.Dtos.Series;

namespace StoreAPI.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class SeriesController : ControllerBase
    {
        private readonly StoreContext _context;

        public SeriesController(StoreContext context)
        {
            _context = context;
        }

        [HttpGet("{series_id}")]
        public async Task<ActionResult<SeriesDto>> Index(long series_id)
        {
            var series = await _context.Series
                .FindAsync(series_id);

            if (series == null)
            {
                return NotFound();
            }

            return Ok(new SeriesDto
            {
                series_id = series_id,
                title = series.Title,
                firm_id = series.FirmId,
                description = series.Description,
                discount = series.Discount
            });
        }

        [HttpPost]
        public async Task<ActionResult<SeriesDto>> CreateSeries(RequestCreateSeriesDto data)
        {
            var id = await _context.Database
                .SqlQuery<long>(
                $"insert into public.series (title, description, discount, firm_id) values({data.title}, {data.description}, {data.discount}, {data.firm_id}) returning series_id"
                )
                .ToListAsync();

            return await Index(id[0]);
        }

        [HttpPut("{series_id}/update")]
        public async Task<ActionResult<SeriesDto>> UpdateSeries(
            long series_id,
            RequestCreateSeriesDto data
            )
        {
            var series = await _context.Series
                .FindAsync(series_id);

            if (series == null )
            {
                return NotFound();
            }

            series.Title = data.title ?? series.Title;
            series.Description = data.description ?? series.Description;
            series.Discount = data.discount ?? series.Discount;
            series.FirmId = data.firm_id ?? series.FirmId;

            await _context.SaveChangesAsync();

            return await Index(series.SeriesId);
        }

        [HttpGet]
        public async Task<ActionResult<List<SeriesDto>>> GetByFilters(
            string? title,
            string? description,
            decimal? discount,
            long? firm_id
            )
        {
            var series = await _context.Series
                .Where(s => (title == null || s.Title == title) &&
                            (description == null || s.Description == description) &&
                            (discount == null || s.Discount == discount) &&
                            (firm_id == null || s.FirmId == firm_id))
                .Select(s => new SeriesDto
                {
                    series_id = s.SeriesId,
                    title = s.Title,
                    description = s.Description ?? "",
                    discount = s.Discount,
                    firm_id = s.FirmId
                })
                .ToListAsync();

            return Ok(series);
        }
    }
}
