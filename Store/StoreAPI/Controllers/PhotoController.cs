using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using StoreAPI.Context;
using StoreAPI.Dtos.Photo;

namespace StoreAPI.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class PhotoController : ControllerBase
    {
        private readonly StoreContext _context;

        public PhotoController(StoreContext context)
        {
            _context = context;
        }

        [HttpGet("{photo_id}")]
        public async Task<ActionResult<PhotoDto>> Index(long photo_id)
        {
            var photo = await _context.Photos
                .Where(p => p.PhotoId == photo_id)
                .FirstOrDefaultAsync();

            if (photo == null)
            {
                return NotFound();
            }

            return new PhotoDto
            {
                photo_id = photo.PhotoId,
                name = photo.Name,
                product_id = photo.ProductId,
                firm_id = photo.FirmId,
                series_id = photo.SeriesId,
                category_id = photo.CategoryId,
            };
        }

        [HttpPost]
        public async Task<ActionResult<PhotoDto>> CreatePhoto(RequestCreatePhotoDto data)
        {
            var id = await _context.Database
                .SqlQuery<long>(
                    $"insert into public.photo (name, product_id, category_id, series_id, firm_id) VALUES ({data.name}, {data.product_id}, {data.category_id}, {data.series_id}, {data.firm_id}) RETURNING photo_id"
                )
                .ToListAsync();

            return await Index(id[0]);
        }

        [HttpDelete("{photo_id}")]
        public async Task<ActionResult<bool>> DeletePhoto(long photo_id)
        {
            var photo = await _context.Photos
                .Where(p => p.PhotoId == photo_id)
                .FirstOrDefaultAsync();

            if (photo == null)
            {
                return NotFound();
            }

            _context.Photos.Remove(photo);
            await _context.SaveChangesAsync();

            return Ok(true);
        }

        [HttpGet]
        public async Task<ActionResult<List<string>>> GetByFilters(
             long? product_id,
             long? firm_id,
             long? series_id,
             long? category_id
            )
        {
            var photos = await _context.Photos
                .Where(p => 
                (product_id == null || p.ProductId == product_id) &&
                (firm_id == null || p.FirmId == firm_id) &&
                (series_id == null || p.SeriesId == series_id) &&
                (category_id == null || p.CategoryId == category_id))
                .Select(p => p.Name)
                .ToListAsync();

            return Ok(photos);
        }
    }
}
