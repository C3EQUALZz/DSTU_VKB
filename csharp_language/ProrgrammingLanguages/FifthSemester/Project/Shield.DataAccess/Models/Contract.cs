using System.ComponentModel.DataAnnotations.Schema;

namespace Shield.DataAccess.Models;

public class Contract
{
    public int ContractId { get; set; }
    public string Address { get; set; }
    public string Owners { get; set; }
    public string Bailee { get; set; }

    [ForeignKey("Plan")]
    public int PlanId { get; set; }

    // Navigation properties
    public Plan Plan { get; set; }
    public ICollection<Picture> Pictures { get; } = new List<Picture>();
}
