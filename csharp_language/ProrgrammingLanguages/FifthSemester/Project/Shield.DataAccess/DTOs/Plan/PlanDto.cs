namespace Shield.DataAccess.DTOs;
public class PlanDto
{
    public int? PlanId
    {
        get; set;
    }
    public string Title
    {
        get; set;
    }
    public string Type
    {
        get; set;
    }
    public byte[] Data
    {
        get; set;
    }
}
