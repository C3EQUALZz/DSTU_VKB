namespace Shield.DataAccess.Models;
public class Alarm
{
    public int AlarmId { get; set; }
    public DateTime Date { get; set; }

    public int ContractId { get; set; }
    public Contract Contract { get; set; }
}
