using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using Microsoft.UI.Xaml.Controls;
using Shield.App.Controls;
using Shield.App.Helpers;
using Shield.App.ViewModels;
using Windows.UI.Notifications;

namespace Shield.App.Views;
public sealed partial class AlarmsPage : Page, INotifyPropertyChanged
{
    private ObservableCollection<AlarmControl> AlarmControls = new();
    private string NotificationTitle { get; set; }
    private string NotificationSubtitle { get; set; }

    public event PropertyChangedEventHandler PropertyChanged;

    public AlarmsViewModel ViewModel
    {
        get;
    }

    public AlarmsPage()
    {
        ViewModel = App.GetService<AlarmsViewModel>();
        this.InitializeComponent();

        LoadAlarms();
    }

    public async Task LoadAlarms()
    {
        var alarms = await ApiHelper.GetAllAlarms();

        if (alarms == null)
        {
            Notify("Ошибка", "Невозможно загрузить историю срабатываний сигнализаций на объектах\nПопробуйте позже");
            return;
        }

        if (alarms.Count == 0)
        {
            Notify("Пусто!", "Не найдено информации о прошлых срабатываниях сигнализаций");
            return;
        }

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

    private void NotifyPropertyChanged([CallerMemberName] string propertyName = "")
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    private void Notify(string title, string subtitle = "")
    {
        NotificationTitle = title;
        NotificationSubtitle = subtitle;

        NotifyPropertyChanged(nameof(NotificationTitle));
        NotifyPropertyChanged(nameof(NotificationSubtitle));

        Notification.IsOpen = true;
    }
}
