using System;
using System.Collections.Generic;

namespace StoreAPI.Models;

public partial class Firm
{
    public long FirmId { get; set; }

    public string Title { get; set; } = null!;

    public string? Description { get; set; }

    public decimal Discount { get; set; }

    public virtual ICollection<Photo> Photos { get; set; } = new List<Photo>();

    public virtual ICollection<Series> Series { get; set; } = new List<Series>();
}
