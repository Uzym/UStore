using System;
using System.Collections.Generic;

namespace TaskMgrAPI.Models;

public partial class Project
{
    public string Title { get; set; } = null!;

    public string? Description { get; set; }

    public long ProjectId { get; set; }

    public virtual ICollection<Section> Sections { get; set; } = new List<Section>();

    public virtual ICollection<UserProject> UserProjects { get; set; } = new List<UserProject>();
}
