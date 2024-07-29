using Microsoft.UI.Xaml.Controls;
using Shield.DataAccess.DTOs;

namespace Shield.App.Controls;
public sealed partial class AlarmControl : UserControl
{
    public string Bailee { get; set; }
    public string Address { get; set; }

    public DateTime DateTime { get; set; }
    public DateOnly DateOnly => DateOnly.FromDateTime(DateTime);
    public TimeOnly TimeOnly => TimeOnly.FromDateTime(DateTime);

    public AlarmControl()
    {
        this.InitializeComponent();
    }

    public AlarmControl(AlarmDto alarm)
    {
        if (alarm.Contract != null)
        {
            Bailee = alarm.Contract.Bailee;
            Address = alarm.Contract.Address;
        }
        if (alarm.Date != null) DateTime = alarm.Date.Value;

        this.InitializeComponent();
    }
}
