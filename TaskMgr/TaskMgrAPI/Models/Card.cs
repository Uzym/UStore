using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Runtime.Serialization;
using System.Text.Json.Serialization;

namespace TaskMgrAPI.Models;

public class Card
{
    [Key]
    [JsonPropertyName("card_id")]
    public long CardId { get; set; }

    [JsonPropertyName("title")]
    public string Title { get; set; } = null!;

    [JsonPropertyName("description")]
    public string? Description { get; set; }

    [JsonPropertyName("due")]
    public DateTime? Due { get; set; }

    [JsonPropertyName("complete")]
    public DateTime? Complete { get; set; }

    [JsonPropertyName("tags")]
    public string[]? Tags { get; set; }

    [JsonPropertyName("section_id")]
    public long SectionId { get; set; }

    [JsonPropertyName("created")]
    public DateTime Created { get; set; }

    [JsonPropertyName("comments")]
    public virtual ICollection<Comment> Comments { get; set; } = new List<Comment>();

    [JsonPropertyName("section")]
    public virtual Section Section { get; set; } = null!;

    [JsonPropertyName("user_cards")]
    public virtual ICollection<UserCard> UserCards { get; set; } = new List<UserCard>();
}
