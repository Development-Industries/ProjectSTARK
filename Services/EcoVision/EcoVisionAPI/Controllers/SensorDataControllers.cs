using Microsoft.AspNetCore.Mvc;
using EcoVisionAPI.Data;
using EcoVisionAPI.Models;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

namespace EcoVisionAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class SensorDataController : ControllerBase
    {
        private readonly AppDbContext _context;

        public SensorDataController(AppDbContext context)
        {
            _context = context;
        }

        [HttpPost]
        public async Task<IActionResult> PostSensorData([FromBody] SensorData data)
        {
            data.Timestamp = DateTime.UtcNow;
            _context.SensorData.Add(data);
            await _context.SaveChangesAsync();
            return Ok();
        }

        [HttpGet]
        public async Task<IActionResult> GetSensorData()
        {
            var data = await _context.SensorData.ToListAsync();
            return Ok(data);
        }
    }
}
