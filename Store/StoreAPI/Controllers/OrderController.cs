using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using StoreAPI.Clients;
using StoreAPI.Context;
using StoreAPI.Dtos.Order;
using StoreAPI.Dtos.Product;
using StoreAPI.Models;

namespace StoreAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class OrderController : ControllerBase
    {
        private readonly StoreContext _context;
        private readonly ITaskMgrClient _taskMgrClient;

        private async Task<long> AuthUser(string tg_id)
        {
            var userId = await _context.Users
                .Where(u => u.TgId == tg_id)
                .Select(u => u.UserId)
                .FirstAsync();
            return userId;
        }

        public OrderController(StoreContext context, ITaskMgrClient taskMgrClient)
        {
            _context = context;
            _taskMgrClient = taskMgrClient;
        }

        [HttpGet]
        public async Task<ActionResult<List<OrderDto>>> Get([FromHeader(Name = "Telegram-Id")] string tg_id, bool? finished)
        {
            var userId = await AuthUser(tg_id);
            var orders = await _context.Orders
                .Where(o => (finished == null || o.Finished == finished) &&
                            o.UserId == userId)
                .Select(o => new OrderDto
                {
                    order_id = o.OrderId,
                    card_id = o.CardId,
                    finished = o.Finished,
                    price = o.Price,
                    user_id = o.UserId,
                })
                .ToListAsync();

            return Ok(orders);
        }

        [HttpGet("{order_id}")]
        public async Task<ActionResult<OrderDto>> Index([FromHeader(Name = "Telegram-Id")] string tg_id, long order_id)
        {
            var userId = await AuthUser(tg_id);
            var order = await _context.Orders
                .Where(o => o.OrderId == order_id && o.UserId == userId)
                .FirstOrDefaultAsync();

            if (order == null)
            {
                return NotFound();
            }

            return Ok(new OrderDto 
            { 
                order_id = order.OrderId,
                card_id = order.CardId,
                finished = order.Finished,
                price = order.Price,
                user_id = userId,
            });
        }

        [HttpPost]
        public async Task<ActionResult<OrderDto>> CreateOrder(
            [FromHeader(Name = "Telegram-Id")] string tg_id,
            RequestCreateOrderDto data)
        {
            var userId = await AuthUser(tg_id);
            var notFinishedOrder = await _context.Orders
                .Where(o => o.UserId == userId && !o.Finished)
                .FirstOrDefaultAsync();

            if (notFinishedOrder != null)
            {
                notFinishedOrder.Price += data.price ?? 0;
                await _context.SaveChangesAsync();
                return await Index(tg_id, notFinishedOrder.OrderId);
            }

            var order = new Order
            {
                UserId = userId,
                CardId = data.card_id ?? 0,
                Finished = false,
                Price = data.price ?? 0,
            };

            await _context.Orders.AddAsync(order);
            await _context.SaveChangesAsync();

            return await Index(tg_id, order.OrderId);
        }

        [HttpPost("{order_id}/products")]
        public async Task<ActionResult<List<OrderProductDto>>> AddOrderProduct(
            [FromHeader(Name = "Telegram-Id")] string tg_id, 
            long order_id)
        {
            await AuthUser(tg_id); //TODO
            return Ok(products);
        }

        [HttpGet("{order_id}/products")]
        public async Task<ActionResult<List<OrderProductDto>>> GetOrderProducts(
            [FromHeader(Name = "Telegram-Id")] string tg_id, 
            long order_id)
        {
            await AuthUser(tg_id);
            var products = await _context.OrderProducts
                .Where(op => op.OrderId == order_id)
                .Select(op => new OrderProductDto
                {
                    productId = op.ProductId,
                    quantity = op.Quantity
                })
                .ToListAsync();
            return Ok(products);
        }

        [HttpDelete("{order_id}/product")]
        public async Task<ActionResult<OrderDto>> DeleteOrderProduct(
            [FromHeader(Name = "Telegram-Id")] string tg_id, 
            long order_id)
        {
            var userId = await AuthUser(tg_id);
            var order = await _context.Orders
                .Include(o => o.OrderProducts)
                .Where(o => o.OrderId == order_id && o.UserId == userId)
                .FirstOrDefaultAsync();

            if (order == null)
            {
                return NotFound();
            }

            order.OrderProducts.Clear();
            await _context.SaveChangesAsync();
            return Ok(order);
        }

        [HttpDelete]
        public async Task<ActionResult<bool>> DeleteOrder(
            [FromHeader(Name = "Telegram-Id")] string tg_id, 
            long order_id)
        {
            var userId = await AuthUser(tg_id);
            var order = await _context.Orders
                .Where(o => o.OrderId == order_id && o.UserId == userId)
                .FirstOrDefaultAsync();

            if (order == null)
            {
                return NotFound();
            }

            _context.Orders.Remove(order);
            await _context.SaveChangesAsync();
            return Ok(order);
        }


    }
}
