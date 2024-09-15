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
    public List<DateTime> Dates => Alarms.Select(a => a.Date.Value).Order().ToList();

    public List<AlarmDto> AlarmsDB { get; private set; }

    [ObservableProperty]
    public DateTimeOffset? m_PickedFrom;

    [ObservableProperty]
    public DateTimeOffset? m_PickedUntil;

    [ObservableProperty]
    public List<AlarmDto> m_Alarms;

    [ObservableProperty]
    public bool m_EnableSearch;

    [ObservableProperty]
    public DateTimeOffset m_StartDate;

    [ObservableProperty]
    public DateTimeOffset m_EndDate;

    public AlarmsTableViewViewModel()
    {
        Alarms = [];
        EnableSearch = false;
    }

    public async Task<List<AlarmDto>> LoadAlarms()
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

        var dates = alarms.Select(a => a.Date.Value).Order().ToList();
        StartDate = dates[0];
        EndDate = dates[^1];

        AlarmsDB = alarms;
        Alarms = new List<AlarmDto>(alarms);

        return Alarms;
    }
}
