using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace TaskMgrAPI.Models;

public partial class UserProject
{
    [Key]
    public long UserProjectId { get; set; }

    public long UserId { get; set; }

    public long ProjectId { get; set; }

    public long RoleId { get; set; }
    
    public virtual Project Project { get; set; } = null!;

    public virtual Role Role { get; set; } = null!;

    public virtual User User { get; set; } = null!;
}
