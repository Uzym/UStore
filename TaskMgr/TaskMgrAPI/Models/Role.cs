using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using Newtonsoft.Json;

namespace TaskMgrAPI.Models;

public partial class Role
{
    [Key]
    public long RoleId { get; set; }

    public string Title { get; set; } = null!;

    public string? Description { get; set; }

    public string[] AllowTables { get; set; } = null!;

    [JsonIgnore]
    public virtual ICollection<RightRole> RightRoles { get; set; } = new List<RightRole>();

    [JsonIgnore]
    public virtual ICollection<UserCard> UserCards { get; set; } = new List<UserCard>();

    [JsonIgnore]
    public virtual ICollection<UserProject> UserProjects { get; set; } = new List<UserProject>();
}
