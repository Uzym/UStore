using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.StaticFiles;
using Minio;
using System.Text.RegularExpressions;

namespace S3_Service.Controllers
{
    [ApiController]
    [Route("[controller]")]
    // [EnableCors]
    public class FilesController : ControllerBase
    {
        private const string BucketName = "store";

        private readonly ILogger<FilesController> _logger;
        private readonly MinioClient _minioClient;

        public FilesController(
            ILogger<FilesController> logger,
            MinioClient minioClient)
        {
            _logger = logger;
            _minioClient = minioClient;
        }

        [HttpPost("/upload")]
        public async Task<IActionResult> UploadFile(IFormFile file)
        {
            var bea = new BucketExistsArgs()
                .WithBucket(BucketName);

            bool found = await _minioClient.BucketExistsAsync(bea);

            if (!found) {
                var mba = new MakeBucketArgs()
                    .WithBucket(BucketName);
                await _minioClient.MakeBucketAsync(mba);
                _logger.LogInformation("mybucket is created successfully");
            }
            _logger.LogInformation($"{found}");

            if (file is null)
                return BadRequest("Must upload a valid file!");

            if (file.Length > 15728640) {
                return BadRequest("Размер файла не должен превышать 15 МБ");
            }

            var name = Path.GetFileNameWithoutExtension(file.FileName);
            var extension = Path.GetExtension(file.FileName);
            var str1 = DateTime.Now.ToString();
            var str2 = Regex.Replace(str1, "[ :/.,]", "_");
            var fileName = $"{name}_{str2}{extension}";

            var filePath = Path.GetTempFileName();

            _logger.LogInformation($"Temp file name: '{filePath}'.");

            try
            {
                await using var stream = System.IO.File.Create(filePath);
                await file.CopyToAsync(stream);
                stream.Seek(0, SeekOrigin.Begin);

                _logger.LogInformation($"File copied to stream {stream.Name} {stream.Length}.");

                PutObjectArgs putObjectArgs = new PutObjectArgs()
                                      .WithBucket(BucketName)
                                      .WithObject(fileName)
                                      .WithObjectSize(stream.Length)
                                      .WithStreamData(stream)
                                      .WithContentType(file.ContentType);
                
                await _minioClient.PutObjectAsync(putObjectArgs);
            }
            catch (Exception exception)
            {
                _logger.LogError(exception, exception.Message);
                throw;
            }

            return Ok(new {FileName = fileName});
        }

        [HttpPost("/download")]
        public async Task<IActionResult> DownloadFile(string fileName)
        {
            var bea = new BucketExistsArgs()
                .WithBucket(BucketName);
            bool found = await _minioClient.BucketExistsAsync(bea);
            if (!found) {
                var mba = new MakeBucketArgs()
                    .WithBucket(BucketName);
                await _minioClient.MakeBucketAsync(mba);
                _logger.LogInformation("mybucket is created successfully");
            }

            try
            {
                if (string.IsNullOrEmpty(fileName))
                    return BadRequest($"'{nameof(fileName)} cannot be null or empty!'");

                var filePath = Path.GetTempFileName();
                _logger.LogInformation($"Temp file name: '{filePath}'.");
            
                var stream = System.IO.File.Create(filePath);
                stream.Seek(0, SeekOrigin.Begin);
            
                StatObjectArgs statObjectArgs = new StatObjectArgs()
                                           .WithBucket(BucketName)
                                           .WithObject(fileName);

                await _minioClient.StatObjectAsync(statObjectArgs);

                GetObjectArgs getObjectArgs = new GetObjectArgs()
                                         .WithBucket(BucketName)
                                         .WithObject(fileName)
                                         .WithCallbackStream((s) =>
                                              {
                                                  s.CopyTo(stream);
                                              });

                await _minioClient.GetObjectAsync(getObjectArgs);

                stream.Seek(0, SeekOrigin.Begin);

                if (!new FileExtensionContentTypeProvider().TryGetContentType(fileName, out var contentType))
                    contentType = "application/octet-stream";

            
                return File(stream, contentType, fileName);
            }
            catch (Exception ex)
            {
                return NotFound("file is not found");
            }
        }

        [HttpDelete("/remove")]
        public async Task<ActionResult<bool>> RemoveFile(string fileName)
        {
            if (string.IsNullOrEmpty(fileName))
                return BadRequest($"'{nameof(fileName)} cannot be null or empty!'");

            try
            {
                var removeObjectArgs = new RemoveObjectArgs()
                    .WithBucket(BucketName)
                    .WithObject(fileName);
                await _minioClient.RemoveObjectAsync(removeObjectArgs);
                return Ok(true);
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }
    }
}