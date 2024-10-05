using Microsoft.EntityFrameworkCore;
using JarvisHealthAPI.Models;
using System.Collections.Generic;
using System.Reflection.Emit;

namespace JarvisHealthAPI.Data
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options)
            : base(options)
        {
        }

        public DbSet<User> Users { get; set; }
        public DbSet<HealthProfile> HealthProfiles { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            // Configure entity relationships if needed
        }
    }
}
