namespace ProjectSTARK.API.Models
{
    public class HealthProfile
    {
        public int Id { get; set; }
        public int UserId { get; set; }
        public string HealthData { get; set; }

        public User User { get; set; }
    }
}
