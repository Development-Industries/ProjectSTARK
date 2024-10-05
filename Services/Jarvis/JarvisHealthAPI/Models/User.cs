
using System.ComponentModel.DataAnnotations;

// User.cs
namespace JarvisHealthAPI.Models
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

// UserDto.cs

namespace JarvisHealthAPI.Models
{
    public class UserDto
    {
        [Required]
        public string Username { get; set; }

        [Required]
        [EmailAddress]
        public string Email { get; set; }

        [Required]
        [MinLength(6)]
        public string Password { get; set; }
    }
}

// LoginDto.cs

namespace JarvisHealthAPI.Models
{
    public class LoginDto
    {
        [Required]
        public string Username { get; set; }

        [Required]
        public string Password { get; set; }
    }
}
