using Microsoft.EntityFrameworkCore;
using ProjectSTARK.API.Models;

namespace ProjectSTARK.API.Data
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
            // Configure relationships and constraints if necessary
            modelBuilder.Entity<User>()
                .HasOne(u => u.HealthProfile)
                .WithOne(hp => hp.User)
                .HasForeignKey<HealthProfile>(hp => hp.UserId);

            base.OnModelCreating(modelBuilder);
        }
    }
}
