using System;
using System.Collections.Generic;

namespace StoreAPI.Models;

public partial class Product
{
    public long ProductId { get; set; }

    public long CategoryId { get; set; }

    public long? SeriesId { get; set; }

    public string Title { get; set; } = null!;

    public string? Description { get; set; }

    public decimal Cost { get; set; }

    public TimeSpan DeliveryTime { get; set; }

    public decimal Discount { get; set; }

    public virtual Category Category { get; set; } = null!;

    public virtual ICollection<OrderProduct> OrderProducts { get; set; } = new List<OrderProduct>();

    public virtual ICollection<Photo> Photos { get; set; } = new List<Photo>();

    public virtual Series? Series { get; set; }
}
