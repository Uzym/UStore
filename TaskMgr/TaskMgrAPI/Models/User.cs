using System;
using System.Collections.Generic;

namespace TaskMgrAPI.Models;

public partial class User
{
    public string? Name { get; set; }

    public string TelegramId { get; set; } = null!;

    public long UserId { get; set; }

    public virtual ICollection<Comment> Comments { get; set; } = new List<Comment>();

    public virtual ICollection<UserCard> UserCards { get; set; } = new List<UserCard>();

    public virtual ICollection<UserProject> UserProjects { get; set; } = new List<UserProject>();
}
