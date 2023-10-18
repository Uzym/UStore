using System;
using System.Collections.Generic;

namespace StoreAPI.Models;

public partial class Photo
{
    public long PhotoId { get; set; }

    public long? ProductId { get; set; }

    public long? CategoryId { get; set; }

    public long? SeriesId { get; set; }

    public long? FirmId { get; set; }

    public string Name { get; set; } = null!;

    public virtual Category? Category { get; set; }

    public virtual Firm? Firm { get; set; }

    public virtual Product? Product { get; set; }

    public virtual Series? Series { get; set; }
}
