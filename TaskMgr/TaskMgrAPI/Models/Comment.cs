using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace TaskMgrAPI.Models;

public partial class Comment
{
    [Key]
    public long CommentId { get; set; }

    public string Description { get; set; } = null!;

    public long UserId { get; set; }

    public long CardId { get; set; }
    
    public virtual Card Card { get; set; } = null!;

    public virtual User User { get; set; } = null!;
}
