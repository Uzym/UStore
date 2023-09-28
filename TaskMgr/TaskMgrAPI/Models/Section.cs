using System;
using System.Collections.Generic;

namespace TaskMgrAPI.Models;

public partial class Section
{
    public string Title { get; set; } = null!;

    public long ProjectId { get; set; }

    public long SectionId { get; set; }

    public virtual ICollection<Card> Cards { get; set; } = new List<Card>();

    public virtual Project Project { get; set; } = null!;
}
