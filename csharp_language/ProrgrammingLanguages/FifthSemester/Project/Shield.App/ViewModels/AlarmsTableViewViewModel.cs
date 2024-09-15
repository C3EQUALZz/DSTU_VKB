using System.Net.Http.Json;
using CommunityToolkit.Mvvm.ComponentModel;
using Shield.App.Helpers;
using Shield.App.Views;
using Shield.DataAccess.DTOs;
using Shield.DataAccess.Models;

namespace Shield.App.ViewModels;

public partial class AlarmsTableViewViewModel : ObservableRecipient
{
    private ShellPage Shell = ShellPage.Instance;

    [ObservableProperty]
    public List<AlarmDto> m_Alarms;

    public AlarmsTableViewViewModel()
    {
        Alarms = [];
    }

    public async Task<List<AlarmDto>> GetAlarms()
    {
        var response = await ApiHelper.GetAllAlarms();

        if (response == null || !response.IsSuccessStatusCode)
        {
            Shell.Notify("Error".GetLocalized(), "ServerNotRespondingErrorDescription".GetLocalized());
            return [];
        }

        var alarms = await response.Content.ReadFromJsonAsync<List<AlarmDto>>();

        if (alarms == null)
        {
            Shell.Notify("Error".GetLocalized(), "UnableToLoadAlarmsErrorDescription".GetLocalized());
            return [];
        }

        if (alarms.Count == 0)
        {
            Shell.Notify($"{"Empty".GetLocalized()}!", "EmptyAlarmsListErrorDescription".GetLocalized());
            return [];
        }
//#if DEBUG
//        Shell.Notify($"Alarms found: {alarms.Count}");
//#endif

        return alarms;
    }
}
