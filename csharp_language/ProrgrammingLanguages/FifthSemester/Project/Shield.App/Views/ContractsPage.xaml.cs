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
using Shield.DataAccess.Models;
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

        UpdateContractsLV();
    }

    private async void CreateContractBtn_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        var dialog = new ContentDialog();
        var content = new CreateContractDialog();

        // XamlRoot must be set in the case of a ContentDialog running in a Desktop app
        dialog.XamlRoot = this.XamlRoot;
        dialog.Style = Application.Current.Resources["DefaultContentDialogStyle"] as Style;
        dialog.Title = "Новый контракт";
        dialog.PrimaryButtonText = "Сохранить";
        dialog.CloseButtonText = "Отмена";
        dialog.DefaultButton = ContentDialogButton.Primary;
        dialog.Content = content;
        dialog.Width = 1400;

        var result = await dialog.ShowAsync();

        if (result == ContentDialogResult.Primary)
        {
            var contract = new Contract() {
                Bailee = content.Bailee,
                Address = content.Address,
                Comment = content.Comment,
                Owners = string.Join(';', content.Owners),
                Plan = new() {
                    Title = content.Plan.DisplayName,
                    Type = content.Plan.DisplayType,
                    Data = File.ReadAllBytes(content.Plan.Path)
                },
                Picture = new Picture() {
                    Title = content.Photo.DisplayName,
                    Type = content.Photo.DisplayType,
                    Data = File.ReadAllBytes(content.Photo.Path)
                }    
            };

            var response = await ApiHelper.CreateContract(contract);

            if (response == null || !response.IsSuccessStatusCode)
            {
                Notify("Ошибка", $"Не удалось создать контракт {(response != null ? $"(ошибка {response.StatusCode})" : "(превышено время ожидания)")}");
            }

            await UpdateContractsLV();
        }
    }

    private async Task EditContract(ContractControl sender)
    {
        
    }

    private async Task DeleteContract(ContractControl sender)
    {
        var response = await ApiHelper.DeleteContract(sender.ContractId);
        if (response == null || !response.IsSuccessStatusCode)
        {
            Notify("Ошибка", $"Не удалось удалить контракт {(response != null ? $"(ошибка {response.StatusCode})" : "(превышено время ожидания)")}");
        }
        await UpdateContractsLV();
    }

    private async Task ExportContract(ContractControl sender)
    {

    }

    private async Task AlertContract(ContractControl sender)
    {
        Notify("ALERT TEST", $"{sender.ContractId}\n{sender.Address}\n{sender.Bailee}\n{sender.Owners}\n{sender.Comment}");
    }

    private async void UpdateContractsListBtn_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        await UpdateContractsLV();
    }

    private async Task UpdateContractsLV()
    {
        contractControls.Clear();

        var response = await ApiHelper.GetAllContracts();

        if (response != null)
        {
            if (response.Contracts.Count == 0)
            {
                Notify("Пусто!", "Не найдено контрактов в базе данных");
                return;
            }
            
            foreach (var contract in response.Contracts)
            {
                var control = new ContractControl(contract);
                control.ExportRequested += async (s) => await ExportContract(s);
                control.EditRequested += async (s) => await EditContract(s);
                control.DeleteRequested += async (s) => await DeleteContract(s);
                control.AlertRequested += async (s) => await AlertContract(s);
                contractControls.Add(control);
            }
        }
        else
        {
            Notify("Ошибка выполнения запроса", "Проверьте подключение к интернету или войдите в другой аккаунт");
        }
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
