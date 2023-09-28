using System;
using System.Collections.Generic;

namespace TaskMgrAPI.Models;

public partial class Card
{
    public long CardId { get; set; }

    public string Title { get; set; } = null!;

    public string? Description { get; set; }

    public DateTime? Due { get; set; }

    public DateTime? Complete { get; set; }

    public string[]? Tags { get; set; }

    public long SectionId { get; set; }

    public DateTime Created { get; set; }

    public virtual ICollection<Comment> Comments { get; set; } = new List<Comment>();

    public virtual Section Section { get; set; } = null!;

    public virtual ICollection<UserCard> UserCards { get; set; } = new List<UserCard>();
}
