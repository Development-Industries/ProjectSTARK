using Microsoft.EntityFrameworkCore;
using EcoVisionAPI.Models;
using System.Collections.Generic;

namespace EcoVisionAPI.Data
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options)
            : base(options)
        {
        }

        public DbSet<SensorData> SensorData { get; set; }

        internal Task SaveChangesAsync()
        {
            throw new NotImplementedException();
        }
    }
}
