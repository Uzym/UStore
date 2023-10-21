using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using StoreAPI.Context;
using StoreAPI.Dtos.Category;

namespace StoreAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class CategoryController : ControllerBase
    {
        private readonly StoreContext _context;

        public CategoryController(StoreContext context)
        {
            _context = context;
        }

        [HttpGet("{category_id}")]
        public async Task<ActionResult<CategoryDto>> Index(long category_id)
        {
            var category = await _context.Categories
                .FindAsync(category_id);

            if (category == null)
            {
                return NotFound();
            }

            return new CategoryDto
            {
                category_id = category.CategoryId,
                title = category.Title,
                discount = category.Discount,
                description = category.Description,
            };
        }

        [HttpPost]
        public async Task<ActionResult<CategoryDto>> CreateCategory(RequestCreateCategoryDto data)
        {
            var id = await _context.Database
                .SqlQuery<long>(
                $"insert into public.category (title, description, discount) values ({data.title}, {data.description}, {data.discount}) returning category_id"
                )
                .ToListAsync();

            return await Index(id[0]);
        }

        [HttpPut("{category_id}/update")]
        public async Task<ActionResult<CategoryDto>> UpdateCategory(
            long category_id,
            string? title,
            string? description,
            decimal? discount
            )
        {
            var category = await _context.Categories
                .FindAsync(category_id);

            if (category == null)
            {
                return NotFound();
            }

            category.Title = title ?? category.Title;
            category.Description = description ?? category.Description;
            category.Discount = discount ?? category.Discount;

            await _context.SaveChangesAsync();

            return await Index(category_id);
        }

        [HttpGet]
        public async Task<ActionResult<List<CategoryDto>>> GetByFilters(
            string? title,
            string? description,
            decimal? discount
            )
        {
            var categories = await _context.Categories
                .Where(c =>
                (title == null || c.Title == title) &&
                (description == null || c.Description == description) &&
                (discount == null || c.Discount == discount)
                )
                .Select(c => new CategoryDto
                {
                    category_id = c.CategoryId,
                    title = c.Title,
                    description = c.Description ?? "",
                    discount = c.Discount
                })
                .ToListAsync();

            return Ok(categories);
        }
    }
}
