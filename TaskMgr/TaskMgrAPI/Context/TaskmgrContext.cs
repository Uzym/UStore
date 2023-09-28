using System;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;
using TaskMgrAPI.Models;

namespace TaskMgrAPI.Context;

public partial class TaskmgrContext : DbContext
{
    public TaskmgrContext()
    {
    }

    public TaskmgrContext(DbContextOptions<TaskmgrContext> options)
        : base(options)
    {
    }

    public virtual DbSet<Card> Cards { get; set; }

    public virtual DbSet<Comment> Comments { get; set; }

    public virtual DbSet<Project> Projects { get; set; }

    public virtual DbSet<Role> Roles { get; set; }

    public virtual DbSet<Section> Sections { get; set; }

    public virtual DbSet<User> Users { get; set; }

    public virtual DbSet<UserCard> UserCards { get; set; }

    public virtual DbSet<UserProject> UserProjects { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
#warning To protect potentially sensitive information in your connection string, you should move it out of source code. You can avoid scaffolding the connection string by using the Name= syntax to read it from configuration - see https://go.microsoft.com/fwlink/?linkid=2131148. For more guidance on storing connection strings, see http://go.microsoft.com/fwlink/?LinkId=723263.
        => optionsBuilder.UseNpgsql("Server=taskmgr_db; Port=5432; Database=taskmgr; Integrated Security=false; User Id=postgres; Password=postgres");

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.HasPostgresEnum("taskmgr_rights", new[] { "view_project", "update_project", "delete_project", "view_section", "update_section", "delete_section", "add_section", "view_card", "update_card", "update_card_complete", "delete_card", "add_card", "add_comment", "view_comment", "delete_comment", "add_user", "delete_user", "view_user" });

        modelBuilder.Entity<Card>(entity =>
        {
            entity.HasKey(e => e.CardId).HasName("card_pk");

            entity.ToTable("card");

            entity.Property(e => e.CardId)
                .UseIdentityAlwaysColumn()
                .HasColumnName("card_id");
            entity.Property(e => e.Complete).HasColumnName("complete");
            entity.Property(e => e.Created)
                .HasDefaultValueSql("now()")
                .HasColumnName("created");
            entity.Property(e => e.Description)
                .HasColumnType("character varying")
                .HasColumnName("description");
            entity.Property(e => e.Due).HasColumnName("due");
            entity.Property(e => e.SectionId).HasColumnName("section_id");
            entity.Property(e => e.Tags)
                .HasColumnType("character varying[]")
                .HasColumnName("tags");
            entity.Property(e => e.Title)
                .HasColumnType("character varying")
                .HasColumnName("title");

            entity.HasOne(d => d.Section).WithMany(p => p.Cards)
                .HasForeignKey(d => d.SectionId)
                .HasConstraintName("card_fk");
        });

        modelBuilder.Entity<Comment>(entity =>
        {
            entity.HasKey(e => e.CommentId).HasName("comment_pk");

            entity.ToTable("comment");

            entity.Property(e => e.CommentId)
                .UseIdentityAlwaysColumn()
                .HasColumnName("comment_id");
            entity.Property(e => e.CardId).HasColumnName("card_id");
            entity.Property(e => e.Description)
                .HasColumnType("character varying")
                .HasColumnName("description");
            entity.Property(e => e.UserId).HasColumnName("user_id");

            entity.HasOne(d => d.Card).WithMany(p => p.Comments)
                .HasForeignKey(d => d.CardId)
                .HasConstraintName("comment_fk");

            entity.HasOne(d => d.User).WithMany(p => p.Comments)
                .HasForeignKey(d => d.UserId)
                .HasConstraintName("comment_fk_1");
        });

        modelBuilder.Entity<Project>(entity =>
        {
            entity.HasKey(e => e.ProjectId).HasName("project_pk");

            entity.ToTable("project");

            entity.HasIndex(e => e.ProjectId, "project_project_id_idx").IsUnique();

            entity.Property(e => e.ProjectId)
                .UseIdentityAlwaysColumn()
                .HasColumnName("project_id");
            entity.Property(e => e.Description)
                .HasColumnType("character varying")
                .HasColumnName("description");
            entity.Property(e => e.Title)
                .HasColumnType("character varying")
                .HasColumnName("title");
        });

        modelBuilder.Entity<Role>(entity =>
        {
            entity.HasKey(e => e.RoleId).HasName("role_pk");

            entity.ToTable("role");

            entity.Property(e => e.RoleId)
                .UseIdentityAlwaysColumn()
                .HasColumnName("role_id");
            entity.Property(e => e.AllowTables)
                .HasColumnType("character varying[]")
                .HasColumnName("allow_tables");
            entity.Property(e => e.Description)
                .HasColumnType("character varying")
                .HasColumnName("description");
            entity.Property(e => e.Title)
                .HasColumnType("character varying")
                .HasColumnName("title");
        });

        modelBuilder.Entity<Section>(entity =>
        {
            entity.HasKey(e => e.SectionId).HasName("section_pk");

            entity.ToTable("section");

            entity.HasIndex(e => e.SectionId, "section_section_id_idx").IsUnique();

            entity.Property(e => e.SectionId)
                .UseIdentityAlwaysColumn()
                .HasColumnName("section_id");
            entity.Property(e => e.ProjectId).HasColumnName("project_id");
            entity.Property(e => e.Title)
                .HasColumnType("character varying")
                .HasColumnName("title");

            entity.HasOne(d => d.Project).WithMany(p => p.Sections)
                .HasForeignKey(d => d.ProjectId)
                .HasConstraintName("section_fk");
        });

        modelBuilder.Entity<User>(entity =>
        {
            entity.HasKey(e => e.UserId).HasName("user_pk");

            entity.ToTable("user");

            entity.HasIndex(e => e.UserId, "user_user_id_idx").IsUnique();

            entity.Property(e => e.UserId)
                .UseIdentityAlwaysColumn()
                .HasColumnName("user_id");
            entity.Property(e => e.Name)
                .HasColumnType("character varying")
                .HasColumnName("name");
            entity.Property(e => e.TelegramId)
                .HasColumnType("character varying")
                .HasColumnName("telegram_id");
        });

        modelBuilder.Entity<UserCard>(entity =>
        {
            entity.HasKey(e => e.UserCardId).HasName("user_card_pk");

            entity.ToTable("user_card");

            entity.Property(e => e.UserCardId)
                .UseIdentityAlwaysColumn()
                .HasColumnName("user_card_id");
            entity.Property(e => e.CardId).HasColumnName("card_id");
            entity.Property(e => e.RoleId).HasColumnName("role_id");
            entity.Property(e => e.UserId).HasColumnName("user_id");

            entity.HasOne(d => d.Card).WithMany(p => p.UserCards)
                .HasForeignKey(d => d.CardId)
                .HasConstraintName("user_card_fk_1");

            entity.HasOne(d => d.Role).WithMany(p => p.UserCards)
                .HasForeignKey(d => d.RoleId)
                .HasConstraintName("user_card_fk_2");

            entity.HasOne(d => d.User).WithMany(p => p.UserCards)
                .HasForeignKey(d => d.UserId)
                .HasConstraintName("user_card_fk");
        });

        modelBuilder.Entity<UserProject>(entity =>
        {
            entity.HasKey(e => e.UserProjectId).HasName("user_project_pk");

            entity.ToTable("user_project");

            entity.Property(e => e.UserProjectId)
                .UseIdentityAlwaysColumn()
                .HasColumnName("user_project_id");
            entity.Property(e => e.ProjectId).HasColumnName("project_id");
            entity.Property(e => e.RoleId).HasColumnName("role_id");
            entity.Property(e => e.UserId).HasColumnName("user_id");

            entity.HasOne(d => d.Project).WithMany(p => p.UserProjects)
                .HasForeignKey(d => d.ProjectId)
                .HasConstraintName("user_project_fk_1");

            entity.HasOne(d => d.Role).WithMany(p => p.UserProjects)
                .HasForeignKey(d => d.RoleId)
                .HasConstraintName("user_project_fk_2");

            entity.HasOne(d => d.User).WithMany(p => p.UserProjects)
                .HasForeignKey(d => d.UserId)
                .HasConstraintName("user_project_fk");
        });

        OnModelCreatingPartial(modelBuilder);
    }

    partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
}
