using Shield.DataAccess.Enums;

namespace Shield.DataAccess.DTOs;
public class CreateAlarmDto
{
    public DateTime Date { get; set; }
    public int ContractId { get; set; }
    public AlarmResult Result { get; set; }
}
