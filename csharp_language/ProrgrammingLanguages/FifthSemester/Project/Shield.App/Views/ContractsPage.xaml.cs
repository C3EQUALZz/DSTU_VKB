using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Diagnostics;
using System.Runtime.CompilerServices;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.Windows.ApplicationModel.Resources;
using Shield.App.Controls;
using Shield.App.Dialogs;
using Shield.App.Helpers;
using Shield.App.ViewModels;
using Shield.DataAccess.DTOs;
using Windows.Storage;

namespace Shield.App.Views;

public sealed partial class ContractsPage : Page, INotifyPropertyChanged
{
    private ObservableCollection<ContractControl> contractControls = new();
    private string NotificationTitle { get; set; }
    private string NotificationSubtitle { get; set; }

    public event PropertyChangedEventHandler PropertyChanged;

    public ContractsViewModel ViewModel
    {
        get;
    }

    public ContractsPage()
    {
        ViewModel = App.GetService<ContractsViewModel>();
        InitializeComponent();
    }

    private async void CreateContractBtn_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        ContentDialog dialog = new ContentDialog();

        // XamlRoot must be set in the case of a ContentDialog running in a Desktop app
        dialog.XamlRoot = this.XamlRoot;
        dialog.Style = Application.Current.Resources["DefaultContentDialogStyle"] as Style;
        dialog.Title = "Новый контракт";
        dialog.PrimaryButtonText = "Сохранить";
        dialog.CloseButtonText = "Отмена";
        dialog.DefaultButton = ContentDialogButton.Primary;
        dialog.Content = new CreateContractDialog();
        dialog.Width = 1400;

        var result = await dialog.ShowAsync();

    }

    private async void EditContractBtn_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        
    }

    private async void MoreContractBtn_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {

    }

    private async void UpdateContractsListBtn_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        var response = await ApiHelper.GetAllContracts();

        if (response != null)
        {
            Debug.WriteLine(response.Contracts.Count);
            if (response.Contracts.Count == 0)
            {
                Notify("Пусто!", "Не найдено контрактов в базе данных");
                return;
            }

            contractControls.Clear();
            foreach (var contract in response.Contracts)
            {
                contractControls.Add(new(contract));
            }
        }
        else
        {
            Notify("Ошибка выполнения запроса", "Проверьте подключение к интернету или войдите в другой аккаунт");
        }
    }

    private async void DeleteContractBtn_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {

    }

    private void Notify(string title, string subtitle = "")
    {
        NotificationTitle = title;
        NotificationSubtitle = subtitle;

        NotifyPropertyChanged(nameof(NotificationTitle));
        NotifyPropertyChanged(nameof(NotificationSubtitle));

        Notification.IsOpen = true;
    }

    private void NotifyPropertyChanged([CallerMemberName] string propertyName = "")
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}
