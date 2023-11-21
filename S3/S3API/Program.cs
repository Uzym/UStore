using Microsoft.Extensions.Options;
using Microsoft.OpenApi.Models;
using Minio;
using S3API.Options;

namespace S3API
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);

            // Add services to the container.

            builder.Services.AddControllers();
            // Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
            builder.Services.AddSingleton(sp =>
            { 
                return new MinioClient()
                    .WithEndpoint("minio:9000")
                    .WithCredentials("minioadmin", "minioadmin")
                    .WithSSL(false)
                    .Build();
            });
            builder.Services.AddEndpointsApiExplorer();
            builder.Services.AddSwaggerGen(c =>
            {
                c.SwaggerDoc("v1", new OpenApiInfo {Title = "S3 API", Version = "v1"});
            });
            
            // builder.Services.Configure<MinioOptions>(Configuration.GetSection(nameof(MinioOptions)));
            
            builder.Services.AddCors();

            var app = builder.Build();

            // Configure the HTTP request pipeline.
            if (app.Environment.IsDevelopment())
            {
                app.UseSwagger();
                app.UseSwaggerUI(c => c.SwaggerEndpoint("/swagger/v1/swagger.json", "S3 API"));
            }
            app.UseRouting();
            app.UseHttpsRedirection();

            //app.UseAuthorization();

            app.UseCors(x => x
                .AllowAnyMethod()
                .AllowAnyHeader()
                .SetIsOriginAllowed(origin => true)
                .AllowCredentials());

            app.MapControllers();

            app.Run();
        }
    }
}