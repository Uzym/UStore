using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace TaskMgrAPI.Models;

public partial class Section
{
    public string Title { get; set; } = null!;

    public long ProjectId { get; set; }

    [Key]
    public long SectionId { get; set; }
    
    public virtual ICollection<Card> Cards { get; set; } = new List<Card>(); 

    public virtual Project Project { get; set; } = null!;
}
