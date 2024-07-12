namespace Shield.DataAccess.Models;
public class Plan
{
    public int PlanId { get; set; }
    public string Title { get; set; }
    public string Type { get; set; }
    public byte[] Data { get; set; }

    public int ContractId { get; set; }
    public Contract Contract { get; set; }
}
