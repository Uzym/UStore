using System;
using System.Collections.Generic;

namespace StoreAPI.Models;

public partial class OrderProduct
{
    public long OrderProductId { get; set; }

    public long OrderId { get; set; }

    public long ProductId { get; set; }

    public int Quantity { get; set; }

    public virtual Order Order { get; set; } = null!;

    public virtual Product Product { get; set; } = null!;
}
