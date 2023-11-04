using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using StoreAPI.Context;
using StoreAPI.Dtos.Product;

namespace StoreAPI.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class ProductController : ControllerBase
    {
        private readonly StoreContext _context;

        public ProductController(StoreContext context)
        {
            _context = context;
        }

        [HttpGet("{product_id}")]
        public async Task<ActionResult<ProductDto>> Index(long product_id)
        {
            var product = await _context.Products
                .FindAsync(product_id);

            if (product == null)
            {
                return NotFound();
            }

            return Ok(new ProductDto
            {
                product_id = product.ProductId,
                category_id = product.CategoryId,
                series_id = product.SeriesId,
                title = product.Title,
                description = product.Description ?? "",
                cost = product.Cost,
                delivery_time = product.DeliveryTime,
                discount = product.Discount,
            });
        }
        
        [HttpPost]
        public async Task<ActionResult<ProductDto>> CreateProduct(RequestCreateProductDto data)
        {
            var id = await _context.Database
                .SqlQuery<long>(
                $"insert into public.product (category_id, series_id, title, description, cost, delivery_time, discount) values ({data.category_id}, {data.series_id}, {data.title}, {data.description}, {data.cost}, {data.delivery_time}, {data.discount}) returning product_id"
                )
                .ToListAsync();
            
            return await Index(id[0]);
        }

        [HttpPut]
        public async Task<ActionResult<ProductDto>> UpdateProduct(
            long product_id,
            RequestCreateProductDto data
            )
        {
            var product = await _context.Products
                .FindAsync(product_id);

            if (product == null)
            {
                return NotFound();
            }

            product.CategoryId = data.category_id ?? product.CategoryId;
            product.SeriesId = data.series_id ?? product.SeriesId;
            product.Title = data.title ?? product.Title;
            product.Description = data.description ?? product.Description;
            product.Cost = data.cost ?? product.Cost;
            product.DeliveryTime = data.delivery_time ?? product.DeliveryTime;
            product.Discount = data.discount ?? product.Discount;

            await _context.SaveChangesAsync();

            return await Index(product.ProductId);
        }

        [HttpGet]
        public async Task<ActionResult<List<ProductDto>>> GetByFilters(
            long? category_id,
            long? series_id,
            string? title,
            string? description,
            decimal? cost,
            TimeSpan? delivery_time,
            decimal? discount
            )
        {
            var products = await _context.Products
                .Where(p => (category_id == null || p.CategoryId == category_id) &&
                            (series_id == null || p.SeriesId == series_id) &&
                            (title ==  null || p.Title == title) &&
                            (description == null || p.Description == description) &&
                            (cost == null ||  p.Cost == cost) &&
                            (discount == null || p.Discount == discount) &&
                            (delivery_time == null ||  p.DeliveryTime == delivery_time))
                .Select(p => new ProductDto
                {
                    product_id = p.ProductId,
                    category_id = p.CategoryId,
                    series_id = p.SeriesId ?? 0,
                    title = p.Title,
                    description = p.Description ?? "",
                    cost = p.Cost,
                    discount = p.Discount,
                    delivery_time = p.DeliveryTime,
                })
                .ToListAsync();

            return Ok(products);
        }
    }
}
