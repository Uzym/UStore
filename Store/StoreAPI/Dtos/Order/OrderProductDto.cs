namespace StoreAPI.Dtos.Order
{
    public class OrderProductDto
    {
        public long order_id { get; set; }
        public long product_id { get; set; }
        public int quantity { get; set; }
    }
}
