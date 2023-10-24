using System;
using System.Collections.Generic;

namespace StoreAPI.Models;

public partial class Order
{
    public long OrderId { get; set; }

    public long UserId { get; set; }

    public long CardId { get; set; }

    public bool Finished { get; set; }

    public decimal Price { get; set; }

    public virtual ICollection<OrderProduct> OrderProducts { get; set; } = new List<OrderProduct>();

    public virtual User User { get; set; } = null!;
}
