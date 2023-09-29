using System;
using System.Collections.Generic;

namespace TaskMgrAPI.Models;

public partial class RightRole
{
    public long RightRoleId { get; set; }

    public long RightId { get; set; }

    public long RoleId { get; set; }

    public virtual Right Right { get; set; } = null!;

    public virtual Role Role { get; set; } = null!;
}
