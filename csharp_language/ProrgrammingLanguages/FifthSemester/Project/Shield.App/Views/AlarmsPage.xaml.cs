using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Net.Http.Json;
using System.Runtime.CompilerServices;
using Microsoft.UI.Xaml.Controls;
using Shield.App.Controls;
using Shield.App.Helpers;
using Shield.App.ViewModels;
using Shield.DataAccess.DTOs;

namespace Shield.App.Views;
public sealed partial class AlarmsPage : Page
{
    private readonly ShellPage Shell;
    private ObservableCollection<AlarmControl> AlarmControls = new();

    public AlarmsViewModel ViewModel
    {
        get;
    }

    public AlarmsPage()
    {
        ViewModel = App.GetService<AlarmsViewModel>();
        this.InitializeComponent();
        Shell = ShellPage.Instance;
        LoadAlarms();
    }

    public async Task LoadAlarms()
    {
        var response = await ApiHelper.GetAllAlarms();

        if (response == null || !response.IsSuccessStatusCode)
        {
            Shell.Notify("Error".GetLocalized(), "ServerNotRespondingErrorDescription".GetLocalized());
            return;
        }

        var alarms = await response.Content.ReadFromJsonAsync<List<AlarmDto>>();

        if (alarms == null)
        {
            Shell.Notify("Error".GetLocalized(), "UnableToLoadAlarmsErrorDescription".GetLocalized());
            return;
        }

        if (alarms.Count == 0)
        {
            Shell.Notify($"{"Empty".GetLocalized()}!", "EmptyAlarmsListErrorDescription".GetLocalized());
            return;
        }

        alarms.Reverse();

        foreach (var alarm in alarms)
        {
            AlarmControls.Add(new(alarm));
        }
    }

    private async void UpdateListButton_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        AlarmControls.Clear();
        await LoadAlarms();
    }
}
