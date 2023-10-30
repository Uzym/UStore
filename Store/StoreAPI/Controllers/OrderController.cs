using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using StoreAPI.Clients;
using StoreAPI.Context;
using StoreAPI.Dtos.Card;
using StoreAPI.Dtos.Order;
using StoreAPI.Dtos.Product;
using StoreAPI.Models;
using System;

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
        public async Task<ActionResult<OrderProductDto>> AddOrderProduct(
            [FromHeader(Name = "Telegram-Id")] string tg_id,
            long order_id,
            OrderProductDto data)
        {
            var userId = await AuthUser(tg_id);
            var order = await _context.Orders
                .Include(o => o.OrderProducts)
                .Where(o => o.OrderId == order_id && o.UserId == userId)
                .FirstOrDefaultAsync();

            var product = await _context.Products
                .FindAsync(data.product_id);

            if (order == null || product == null)
            {
                return NotFound();
            }

            await _context.OrderProducts.AddAsync(new OrderProduct
            {
                Order = order,
                Product = product,
                Quantity = data.quantity,
            });

            await _context.SaveChangesAsync();
            
            return Ok(new OrderProductDto
            {
                order_id = order_id,
                product_id = data.product_id,
                quantity = data.quantity
            });
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
                    order_id = op.OrderId,
                    product_id = op.ProductId,
                    quantity = op.Quantity
                })
                .ToListAsync();
            return Ok(products);
        }

        [HttpPatch("{order_id}/product/delete")]
        public async Task<ActionResult<OrderDto>> DeleteOrderProduct(
            [FromHeader(Name = "Telegram-Id")] string tg_id,
            long order_id,
            long product_id)
        {
            var userId = await AuthUser(tg_id);
            
            var orderProduct = await _context.OrderProducts
                .Where(op => op.OrderId == order_id && 
                             op.ProductId == product_id)
                .FirstOrDefaultAsync();
            
            if (orderProduct == null)
            {
                return NotFound();
            }

            if (orderProduct.Quantity <= 1)
            {
                _context.OrderProducts.Remove(orderProduct);
            } else
            {
                orderProduct.Quantity--;
            }

            await _context.SaveChangesAsync();
            return await Index(tg_id, order_id);
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

        [HttpPatch("{order_id}/confirm")]
        public async Task<ActionResult<ResponseGetCardDto>> ConfirmOrder(
            long order_id, 
            long section_id,
            [FromHeader(Name = "Telegram-Id")] string tg_id)
        {
            var userId = await AuthUser(tg_id);
            var user = await _context.Users
                .FindAsync(userId);

            var order = await _context.Orders
                .Where(o => o.OrderId == order_id)
                .FirstOrDefaultAsync();

            if (order == null)
            {
                return NotFound();
            }

            order.Finished = true;
            await _context.SaveChangesAsync();

            string description = "Заказ:\n";
            var orderProducts = await _context.OrderProducts
                .Include(op => op.Product)
                .Where(op => op.OrderId == order_id)
                .ToListAsync();

            decimal sum = 0;
            int iter = 0;

            var due = DateTime.MinValue;
            
            foreach (var op in orderProducts)
            {
                iter++;
                decimal discount = op.Product.Discount;

                var seriesDiscount = await _context.Series
                    .Where(s => s.SeriesId == op.Product.SeriesId)
                    .Select(s => s.Discount)
                    .FirstOrDefaultAsync();

                discount = Math.Min(discount, seriesDiscount);

                var firmDiscount = await _context.Series
                    .Include(s => s.Firm)
                    .Where(s => s.SeriesId == op.Product.SeriesId)
                    .Select(s => s.Firm.Discount)
                    .FirstOrDefaultAsync();

                discount = Math.Min(discount, firmDiscount);

                var categoryDiscount = await _context.Categories
                    .Where(c => c.CategoryId == op.Product.CategoryId)
                    .Select(c => c.Discount)
                    .FirstOrDefaultAsync();

                discount = Math.Min(discount, categoryDiscount);

                sum += (op.Quantity - 1) * op.Product.Cost + op.Product.Cost * discount;

                description += iter.ToString() + "): " + op.Product.Title + " - " + op.Quantity.ToString() + "шт\n\t";
                description += op.Product.Description + "\n\t";
                description += "Цена: " + (op.Product.Cost * discount).ToString() + "\n\t";
                description += "Скидка: " + (1 - discount) * 100 + "%\n";

                if (DateTime.Now.AddHours(3) + op.Product.DeliveryTime > due)
                {
                    due = DateTime.Now.AddHours(3) + op.Product.DeliveryTime;
                }
            }

            description += "ИТОГО: " + sum.ToString() + "\n";
            description += "Контакты пользователя:\n";
            description += "Telegram: " + user?.TgRef ?? "";
            description += "\nEmail: " + user?.Email ?? "";
            description += "\nАдрес: " + user?.Adress ?? "";
            description += "\nТелефон: " + user?.Telephone ?? "";

            string title = user?.Name ?? "";
            title += (" " + order_id.ToString());

            var cardRequest = new RequestCreateCardDto
            {
                title = title,
                description = description,
                due = due,
                tags = new List<string>() { "order" },
            };

            var cardResponse = await _taskMgrClient.CreateCard(
                section_id,
                tg_id,
                cardRequest
            );

            order.CardId = cardResponse.card_id;
            order.Price = sum;
            await _context.SaveChangesAsync();
                
            return Ok(cardResponse);
        }

        [HttpGet("{order_id}/card")]
        public async Task<ActionResult<ResponseGetCardDto>> GetTaskMgrCard(
            [FromHeader(Name = "Telegram-Id")] string tg_id,
            long order_id)
        {
            var userId = await AuthUser(tg_id);
            var user = await _context.Users
                .FindAsync(userId);

            var cardId = await _context.Orders
                .Where(o => o.OrderId == order_id)
                .Select(o => o.CardId)
                .FirstOrDefaultAsync();

            return await _taskMgrClient.GetCardById(tg_id, cardId);
        }
    }
}
