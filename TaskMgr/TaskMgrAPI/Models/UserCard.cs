using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace TaskMgrAPI.Models;

public partial class UserCard
{
    [Key]
    public long UserCardId { get; set; }

    public long UserId { get; set; }

    public long CardId { get; set; }

    public long RoleId { get; set; }
    
    public virtual Card Card { get; set; } = null!;

    public virtual Role Role { get; set; } = null!;

    public virtual User User { get; set; } = null!;
}
