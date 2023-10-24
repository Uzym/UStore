using System;
using System.Collections.Generic;

namespace StoreAPI.Models;

public partial class User
{
    public long UserId { get; set; }

    public string TgId { get; set; } = null!;

    public string Name { get; set; } = null!;

    public string? Adress { get; set; }

    public string? Telephone { get; set; }

    public string? Email { get; set; }

    public string? TgRef { get; set; }

    public bool Admin { get; set; }

    public virtual ICollection<Order> Orders { get; set; } = new List<Order>();
}
