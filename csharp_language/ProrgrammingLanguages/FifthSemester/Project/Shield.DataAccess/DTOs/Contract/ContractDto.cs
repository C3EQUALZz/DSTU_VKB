namespace Shield.DataAccess.DTOs;
public class ContractDto
{
    public int ContractId { get; set; }
    public string Address { get; set; }
    public string? Owners { get; set; }
    public string Bailee { get; set; }
    public string? Comment { get; set; }
    public string Organization { get; set; }
    public DateOnly SignDate { get; set; }
    public bool IsLegalEntity { get; set; }

    public PlanDto Plan { get; set; }
    public PictureDto Picture { get; set; }
    public ICollection<AlarmDto> Alarms { get; set; } = new List<AlarmDto>();
}
