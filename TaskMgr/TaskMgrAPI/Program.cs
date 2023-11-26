using System.Text.Json;
using Microsoft.OpenApi.Models;
using TaskMgrAPI.Context;
using Microsoft.EntityFrameworkCore;
using Microsoft.AspNetCore.OData;
using Microsoft.AspNetCore.OData.Extensions;
using Microsoft.Extensions.DependencyInjection.Extensions;
using Microsoft.OData.Edm;
using Microsoft.OData.ModelBuilder;
using Newtonsoft.Json.Serialization;
using TaskMgrAPI.Dtos.Card;
using TaskMgrAPI.Dtos.Project;
using TaskMgrAPI.Dtos.Section;
using TaskMgrAPI.Dtos.User;
using TaskMgrAPI.Models;
using TaskMgrAPI.Services.Card;
using TaskMgrAPI.Services.Comment;
using TaskMgrAPI.Services.Project;
using TaskMgrAPI.Services.Role;
using TaskMgrAPI.Services.Section;
using TaskMgrAPI.Services.User;
using TaskMgrAPI.Services.UserCard;
using TaskMgrAPI.Services.UserProject;

namespace TaskMgrAPI
{
    public class Program
    {
        public static void Main(string[] args)
        {
            AppContext.SetSwitch("Npgsql.EnableLegacyTimestampBehavior", true);
            AppContext.SetSwitch("Npgsql.DisableDateTimeInfinityConversions", true);
            var builder = WebApplication.CreateBuilder(args);

            // Add services to the container.

            builder.Services.AddControllers().AddOData(option =>
            {
                option.Select();
                option.Expand();
                option.Filter();
                option.Count();
                option.SetMaxTop(100);
                option.SkipToken();
                option.AddRouteComponents("OData", GetEdmModel());
            });
            // Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
            builder.Services.AddEndpointsApiExplorer();
            builder.Services.AddSwaggerGen(c => 
            {
                c.SwaggerDoc("v1", new OpenApiInfo { Title = "TaskMgr", Version = "v1" });
            });

            var connectionString = Environment.GetEnvironmentVariable("DB_CONNECTION_STRING");
            builder.Services.AddDbContext<TaskmgrContext>(options =>
                options.UseNpgsql(
                     connectionString
                )
            );

            builder.Services.AddScoped<IUserService, UserService>();
            builder.Services.AddScoped<IRoleService, RoleService>();
            builder.Services.AddScoped<ICommentService, CommentService>();
            builder.Services.AddScoped<ICardService, CardService>();
            builder.Services.AddScoped<ISectionService, SectionService>();
            builder.Services.AddScoped<IProjectService, ProjectService>();
            builder.Services.AddScoped<IUserCardService, UserCardService>();
            builder.Services.AddScoped<IUserProjectService, UserProjectService>();

            var app = builder.Build();

            // Configure the HTTP request pipeline.
            if (app.Environment.IsDevelopment())
            {
                app.UseSwagger();
                app.UseSwaggerUI(c => c.SwaggerEndpoint("/swagger/v1/swagger.json", "UStore TaskMgr API"));
            }

            app.UseHttpsRedirection();

            // app.UseAuthorization();
            app.MapControllers();

            app.Run();
        }
        
        private static IEdmModel GetEdmModel()
        {
            var odataBuilder = new ODataConventionModelBuilder();
            odataBuilder.EntitySet<User>("Users");
            odataBuilder.EntitySet<Card>("Cards");
            odataBuilder.EntitySet<Comment>("Comments");
            odataBuilder.EntitySet<Role>("Roles");
            odataBuilder.EntitySet<Section>("Sections");
            odataBuilder.EntitySet<Project>("Projects");
            odataBuilder.EntitySet<UserCard>("UserCards");
            odataBuilder.EntitySet<UserProject>("UserProjects");

            return odataBuilder.GetEdmModel();
        }
    }
}