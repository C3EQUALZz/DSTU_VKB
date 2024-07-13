using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Shield.App.Controls;
using Shield.App.Dialogs;
using Shield.App.Helpers;
using Shield.App.ViewModels;
using Shield.DataAccess.DTOs;
using Shield.DataAccess.Models;
using System.Net.Http.Json;
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

        UpdateContractsList();
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
            if (content.Plan == null)
            {
                Notify("Ошибка заполнения формы", "План объекта является обязательным");
                return;
            }

            if (content.Picture == null)
            {
                Notify("Ошибка заполнения формы", "Фото объекта является обязательным");
                return;
            }

            var contract = new ContractDto() {
                Bailee = content.Bailee,
                Address = content.Address,
                Comment = content.Comment,
                Owners = content.Owners.Count > 0 ? string.Join(';', content.Owners) : null,
                Plan = new() {
                    Title = content.Plan.DisplayName,
                    Type = content.Plan.DisplayType,
                    Data = File.ReadAllBytes(content.Plan.Path)
                },
                Picture = new() {
                    Title = content.Picture.DisplayName,
                    Type = content.Picture.DisplayType,
                    Data = File.ReadAllBytes(content.Picture.Path)
                },
                SignDate = DateOnly.FromDateTime(DateTime.Now)
            };

            var response = await ApiHelper.CreateContract(contract);

            if (response == null || !response.IsSuccessStatusCode)
            {
                Notify("Ошибка", $"Не удалось создать контракт {(response != null ? $"(ошибка {response.StatusCode}:\n{await response.Content.ReadAsStringAsync()})" : "(превышено время ожидания)")}\nПовторите попытку позже");
            }
            else
            {
                await UpdateContractsList();
            }
        }
    }

    private async Task EditContract(ContractControl sender)
    {
        var dialog = new ContentDialog();
        var content = new CreateContractDialog(sender.ToDto());
        
        dialog.XamlRoot = this.XamlRoot;
        dialog.Style = Application.Current.Resources["DefaultContentDialogStyle"] as Style;
        dialog.Title = "Изменить контракт";
        dialog.PrimaryButtonText = "Сохранить";
        dialog.CloseButtonText = "Отмена";
        dialog.DefaultButton = ContentDialogButton.Primary;
        dialog.Content = content;
        dialog.Width = 1400;

        var result = await dialog.ShowAsync();

        if (result == ContentDialogResult.Primary)
        {
            // Проверяем, что пользователь изменил какое-либо поле
            if (!content.IsEdited)
            {
                Notify("Изменения не применены", "Не найдено изменений для обновления контракта");
                return;
            }

            // Формируем DTO измененного контракта
            var contract = new ContractDto()
            {
                Bailee = content.Bailee,
                Address = content.Address,
                Comment = content.Comment,
                Owners = content.Owners.Count > 0 ? string.Join(';', content.Owners) : null,
                SignDate = sender.Date
            };

            // Отдельно проверяем, если пользователь заменил план здания, и,
            // Если это так, записываем новый файл в DTO
            if (content.Plan != null)
            {
                contract.Plan = new PlanDto()
                {
                    Title = content.Plan.DisplayName,
                    Type = content.Plan.DisplayType,
                    Data = File.ReadAllBytes(content.Plan.Path)
                };
            }

            // Отдельно проверяем, если пользователь заменил изображение здания, и,
            // Если это так, записываем новый файл в DTO
            if (content.Picture != null)
            {
                contract.Picture = new PictureDto()
                {
                    Title = content.Picture.DisplayName,
                    Type = content.Picture.DisplayType,
                    Data = File.ReadAllBytes(content.Picture.Path)
                };
            }

            // Отправляем на сервер изменения
            var response = await ApiHelper.UpdateContract(sender.ContractId, contract);

            // Если сервер отвечает кодом ошибки или не отвечаем, сообщим об этом пользователю
            if (response == null || !response.IsSuccessStatusCode)
            {
                Notify("Ошибка", $"Не удалось изменить контракт {(response != null ? $"(ошибка {response.StatusCode}:\n{await response.Content.ReadAsStringAsync()})" : "(превышено время ожидания)")}\nПовторите попытку позже");
            }
            else
            {
                await UpdateContractsList();
            }
        }
    }

    private async Task DeleteContract(ContractControl sender)
    {
        var dialog = new ContentDialog();

        // XamlRoot must be set in the case of a ContentDialog running in a Desktop app
        dialog.XamlRoot = this.XamlRoot;
        dialog.Style = Application.Current.Resources["DefaultContentDialogStyle"] as Style;
        dialog.Title = $"Вы уверены что хотите удалить контракт #{sender.ContractId} ({sender.Bailee})?";
        dialog.PrimaryButtonText = "Удалить";
        dialog.CloseButtonText = "Отмена";
        dialog.DefaultButton = ContentDialogButton.Primary;

        var result = await dialog.ShowAsync();

        if (result == ContentDialogResult.Primary)
        {
            var response = await ApiHelper.DeleteContract(sender.ContractId);
            if (response == null || !response.IsSuccessStatusCode)
            {
                Notify("Ошибка", $"Не удалось удалить контракт {(response != null ? $"(ошибка {response.StatusCode})" : "(превышено время ожидания)")}");
            }
            await UpdateContractsList();
        }
    }

    private async Task ExportContract(ContractControl sender)
    {

    }

    private async Task PlanContract(ContractControl sender)
    {
        var savePicker = new Windows.Storage.Pickers.FileSavePicker();
        savePicker.SuggestedStartLocation = Windows.Storage.Pickers.PickerLocationId.Desktop;
        savePicker.FileTypeChoices.Add("Revit Document", new List<string>() { ".rvt" });
        savePicker.SuggestedFileName = $"plan_{sender.ContractId}";

        var hwnd = App.MainWindow.GetWindowHandle();
        WinRT.Interop.InitializeWithWindow.Initialize(savePicker, hwnd);

        var file = await savePicker.PickSaveFileAsync();

        if (file != null)
        {
            CachedFileManager.DeferUpdates(file);

            var response = await ApiHelper.GetContract(sender.ContractId);

            if (response == null || !response.IsSuccessStatusCode)
            {
                Notify("Операция отменена", $"Сервер не отвечает или файл не найден в базе данных");
                await file.DeleteAsync();
                return;
            }

            var contract = await response.Content.ReadFromJsonAsync<Contract>();

            if (contract == null)
            {
                Notify("Операция отменена", "Ошибка парсинга ответа сервера");
                await file.DeleteAsync();
                return;
            }

            await FileIO.WriteBytesAsync(file, contract.Plan.Data);
            var status = await CachedFileManager.CompleteUpdatesAsync(file);

            if (status == Windows.Storage.Provider.FileUpdateStatus.Complete)
            {
                
            }
            else
            {
                Notify("Операция отменена", "Файл не может быть сохранен");
                await file.DeleteAsync();
                return;
            }
        }
        else
        {
            Notify("Операция отменена", "Не выбран файл для записи");
            return;
        }
    }

    private async Task AlertContract(ContractControl sender)
    {
        Notify("Сработала сигнализация", $"{sender.Address} - {sender.Bailee}\nID Контракта: {sender.ContractId}\n{sender.Comment}");

        await ApiHelper.CreateAlarm(new() { ContractId = sender.ContractId, Date = DateTime.Now });
    }

    private async void UpdateContractsListBtn_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        await UpdateContractsList();
    }

    private async Task UpdateContractsList()
    {
        contractControls.Clear();

        var response = await ApiHelper.GetAllContracts();

        if (response != null)
        {
            if (response.Count == 0)
            {
                Notify("Пусто!", "Не найдено контрактов в базе данных");
                return;
            }
            
            foreach (var contract in response)
            {
                var control = new ContractControl(contract);
                control.ExportRequested += async (s) => await ExportContract(s);
                control.PlanRequested += async (s) => await PlanContract(s);
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
