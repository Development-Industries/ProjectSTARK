using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace JarvisHealthAPI.Models
{
    public class HealthProfile
    {
        [Key]
        [ForeignKey("User")]
        public int UserId { get; set; }

        public User User { get; set; }

        public string DietaryPreferences { get; set; }
        public string Lifestyle { get; set; }
        public string MedicalConditions { get; set; }
        // Additional fields as needed
    }
}
