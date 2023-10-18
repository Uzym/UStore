using System;
using System.Collections.Generic;

namespace StoreAPI.Models;

public partial class Series
{
    public long SeriesId { get; set; }

    public string Title { get; set; } = null!;

    public string? Description { get; set; }

    public long FirmId { get; set; }

    public decimal Discount { get; set; }

    public virtual Firm Firm { get; set; } = null!;

    public virtual ICollection<Photo> Photos { get; set; } = new List<Photo>();

    public virtual ICollection<Product> Products { get; set; } = new List<Product>();
}
