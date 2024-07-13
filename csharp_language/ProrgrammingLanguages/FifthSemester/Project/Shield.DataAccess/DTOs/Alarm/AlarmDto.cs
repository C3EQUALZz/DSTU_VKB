namespace Shield.DataAccess.DTOs;
public class AlarmDto
{
    public int? AlarmId { get; set; }
    public DateTime? Date { get; set; }
    public ContractDto? Contract { get; set; }
}
