using Microsoft.OpenApi.Models;
using TaskMgrAPI.Context;
using Microsoft.EntityFrameworkCore;

namespace TaskMgrAPI
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);

            // Add services to the container.

            //builder.Services.AddControllers();
            // Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
            builder.Services.AddEndpointsApiExplorer();
            builder.Services.AddSwaggerGen(c => 
            {
                c.SwaggerDoc("v1", new OpenApiInfo { Title = "TaskMgr", Version = "v1" });
            });

            var connectionString = "host=taskmgr_db;port=5432;database=taskmgr;username=postgres;password=postgres";
            builder.Services.AddDbContext<TaskmgrContext>(options =>
                options.UseNpgsql(
                    connectionString
                )
            );

            var app = builder.Build();

            // Configure the HTTP request pipeline.
            if (app.Environment.IsDevelopment())
            {
                app.UseSwagger();
                app.UseSwaggerUI(c => c.SwaggerEndpoint("/swagger/v1/swagger.json", "UStore TaskMgr API"));
            }

            app.UseHttpsRedirection();

            // app.UseAuthorization();


            //app.MapControllers();

            app.Run();
        }
    }
}