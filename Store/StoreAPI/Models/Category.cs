using System;
using System.Collections.Generic;

namespace StoreAPI.Models;

public partial class Category
{
    public long CategoryId { get; set; }

    public string Title { get; set; } = null!;

    public string? Description { get; set; }

    public decimal Discount { get; set; }

    public virtual ICollection<Photo> Photos { get; set; } = new List<Photo>();

    public virtual ICollection<Product> Products { get; set; } = new List<Product>();
}
