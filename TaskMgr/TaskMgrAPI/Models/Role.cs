using System;
using System.Collections.Generic;

namespace TaskMgrAPI.Models;

public partial class Role
{
    public long RoleId { get; set; }

    public string Title { get; set; } = null!;

    public string? Description { get; set; }

    public string[] AllowTables { get; set; } = null!;

    public virtual ICollection<RightRole> RightRoles { get; set; } = new List<RightRole>();

    public virtual ICollection<UserCard> UserCards { get; set; } = new List<UserCard>();

    public virtual ICollection<UserProject> UserProjects { get; set; } = new List<UserProject>();
}
