using System;
using System.Collections.Generic;

namespace TaskMgrAPI.Models;

public partial class Right
{
    public long RightId { get; set; }

    public string Title { get; set; } = null!;

    public virtual ICollection<RightRole> RightRoles { get; set; } = new List<RightRole>();
}
