using System.ComponentModel.DataAnnotations;

namespace ProjectSTARK.API.Models
{
    public class User
    {
        public int Id { get; set; }

        [Required]
        public string Username { get; set; }

        [Required]
        public string PasswordHash { get; set; }

        [Required]
        public string PasswordSalt { get; set; }

        [Required]
        [EmailAddress]
        public string Email { get; set; }

        public HealthProfile HealthProfile { get; set; }
    }
}
