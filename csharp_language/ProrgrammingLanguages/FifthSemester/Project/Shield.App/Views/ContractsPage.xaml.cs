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
using Shield.App.Enums;
using System.Reflection;
using Spire.Doc;
using Shield.App.Services;

namespace Shield.App.Views;

public sealed partial class ContractsPage : Page, INotifyPropertyChanged
{
    private readonly ShellPage Shell;
    private ObservableCollection<ContractControl> contractControls = new();

    private SortingType SortingType { get; set; } = SortingType.None;

    public event PropertyChangedEventHandler PropertyChanged;

    public ContractsViewModel ViewModel
    {
        get;
    }

    public ContractsPage()
    {
        ViewModel = App.GetService<ContractsViewModel>();
        Shell = ShellPage.Instance;
        InitializeComponent();
    }

    private async void CreateContractBtn_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        var dialog = new ContentDialog();
        var content = new CreateContractDialog();

        dialog.XamlRoot = this.XamlRoot;
        dialog.Style = Application.Current.Resources["DefaultContentDialogStyle"] as Style;
        dialog.Title = "CreateContractDialogTitle".GetLocalized();
        dialog.PrimaryButtonText = "Save".GetLocalized();
        dialog.CloseButtonText = "Cancel".GetLocalized();
        dialog.DefaultButton = ContentDialogButton.Primary;
        dialog.Content = content;
        dialog.Width = 1400;

        var result = await dialog.ShowAsync();

        if (result == ContentDialogResult.Primary)
        {
            if (content.Plan == null)
            {
                Shell.Notify("FormFillError".GetLocalized(), "PlanIsRequiedError".GetLocalized());
                return;
            }

            if (content.Picture == null)
            {
                Shell.Notify("FormFillError".GetLocalized(), "PhotoIsRequiredError".GetLocalized());
                return;
            }

            var contract = new ContractDto() {
                Bailee = content.Bailee,
                Address = content.Address,
                Comment = content.Comment,
                Organization = content.Organization,
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
                await ProcessResponseErroStatusCode(response);
                return;
            }

            await UpdateContractsList();
        }
    }

    private async Task EditContract(ContractControl sender)
    {
        var dialog = new ContentDialog();
        var content = new CreateContractDialog(sender.ToDto());
        
        dialog.XamlRoot = this.XamlRoot;
        dialog.Style = Application.Current.Resources["DefaultContentDialogStyle"] as Style;
        dialog.Title = "EditContractDialogTitle".GetLocalized();
        dialog.PrimaryButtonText = "Save".GetLocalized();
        dialog.CloseButtonText = "Cancel".GetLocalized();
        dialog.DefaultButton = ContentDialogButton.Primary;
        dialog.Content = content;
        dialog.Width = 1400;

        var result = await dialog.ShowAsync();

        if (result == ContentDialogResult.Primary)
        {
            // Проверяем, что пользователь изменил какое-либо поле
            if (!content.IsEdited)
            {
                Shell.Notify("ChangedNotAppliedErrorTitle".GetLocalized(), "ChangedNotAppliedErrorDescription".GetLocalized());
                return;
            }

            // Формируем DTO измененного контракта
            var contract = new ContractDto()
            {
                Bailee = content.Bailee,
                Address = content.Address,
                Comment = content.Comment,
                Organization = content.Organization,
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
                await ProcessResponseErroStatusCode(response);
                return;
            }

            await RefreshContractControl(sender);
        }
    }

    private async Task DeleteContract(ContractControl sender)
    {
        var dialog = new ContentDialog();

        dialog.XamlRoot = this.XamlRoot;
        dialog.Style = Application.Current.Resources["DefaultContentDialogStyle"] as Style;
        dialog.Title = $"{"ContractDeletionApprovalDialogTitle".GetLocalized()} #{sender.ContractId} ({sender.Bailee})?";
        dialog.PrimaryButtonText = "Delete".GetLocalized();
        dialog.CloseButtonText = "Cancel".GetLocalized();
        dialog.DefaultButton = ContentDialogButton.Primary;

        var result = await dialog.ShowAsync();

        if (result == ContentDialogResult.Primary)
        {
            var response = await ApiHelper.DeleteContract(sender.ContractId);

            if (response == null || !response.IsSuccessStatusCode)
            {
                await ProcessResponseErroStatusCode(response);
                return;
            }

            await UpdateContractsList();
        }
    }

    private async Task ExportContract(ContractControl sender)
    {
        // Вызовем диалоговое окно выбора файла, чтобы узнать, куда пользователь хочет сохранить отчет

        var savePicker = new Windows.Storage.Pickers.FileSavePicker();
        savePicker.SuggestedStartLocation = Windows.Storage.Pickers.PickerLocationId.Desktop;
        savePicker.FileTypeChoices.Add("Word Document", new List<string>() { ".docx" });
        savePicker.SuggestedFileName = $"report_{sender.ContractId}";

        var hwnd = App.MainWindow.GetWindowHandle();
        WinRT.Interop.InitializeWithWindow.Initialize(savePicker, hwnd);

        var file = await savePicker.PickSaveFileAsync();

        if (file != null)
        {
            var templatePath = Path.Combine(Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location), "Misc", "WordTemplates", "template.docx");
            var contract = sender.ToDto();

            // Через Spire.Doc сохраним отчет в выбранный файл

            var doc = new Document();
            doc.LoadFromFile(templatePath);
            var replaceDict = new Dictionary<string, string>()
            {
                { "#contract.SignDate#", contract.SignDate.ToString() },
                { "#contract.Organization#", contract.Organization },
                { "#contract.Bailee#", contract.Bailee },
                { "#contract.Address#", contract.Address }
            };

            foreach (var kvp in replaceDict)
            {
                doc.Replace(kvp.Key, kvp.Value, true, true);
            }

            doc.SaveToFile(file.Path);

            doc.Close();

            Shell.Notify("ReportCreatedNotification".GetLocalized(), $"{"Contract".GetLocalized()} №{contract.ContractId}\n{file.Path}");
        }
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

            var response = await ApiHelper.GetContractFull(sender.ContractId);

            if (response == null || !response.IsSuccessStatusCode)
            {
                await file.DeleteAsync();
                await ProcessResponseErroStatusCode(response);
                return;
            }

            var contract = await response.Content.ReadFromJsonAsync<Contract>();

            if (contract == null)
            {
                Shell.Notify("OperationCancelled".GetLocalized(), "HttpResponseParseError".GetLocalized());
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
                Shell.Notify("OperationCancelled".GetLocalized(), "FileCannotBeSavedError".GetLocalized());
                await file.DeleteAsync();
                return;
            }
        }
        else
        {
            Shell.Notify("OperationCancelled".GetLocalized(), "FileToWriteNotSelectedError".GetLocalized());
            return;
        }
    }

    private async Task AlertContract(ContractControl sender)
    {
        var dialog = new ContentDialog();

        dialog.XamlRoot = this.XamlRoot;
        dialog.Style = Application.Current.Resources["DefaultContentDialogStyle"] as Style;
        dialog.Title = $"{"ContractAlertApprovalDialogTitle".GetLocalized()} #{sender.ContractId} ({sender.Organization})?";
        dialog.PrimaryButtonText = "Apply".GetLocalized();
        dialog.CloseButtonText = "Cancel".GetLocalized();
        dialog.DefaultButton = ContentDialogButton.Primary;

        var result = await dialog.ShowAsync();

        if (result == ContentDialogResult.Primary)
        {
            Shell.Notify("AlarmWorked".GetLocalized(), $"{sender.Address} - {sender.Organization}\nID: {sender.ContractId}\n{"Bailee".GetLocalized()}: {sender.Bailee}\n{sender.Comment}");
            
            var response = await ApiHelper.CreateAlarm(new() { ContractId = sender.ContractId, Date = DateTime.Now });

            if (response == null || !response.IsSuccessStatusCode)
            {
                await ProcessResponseErroStatusCode(response);
                return;
            }

            await RefreshContractControl(sender);
        }
    }

    private async Task RefreshContractControl(ContractControl sender)
    {
        var response = await ApiHelper.GetContractInfo(sender.ContractId);

        if (response == null || !response.IsSuccessStatusCode)
        {
            await ProcessResponseErroStatusCode(response);
            return;
        }

        var dto = await response.Content.ReadFromJsonAsync<ContractDto>();

        if (dto == null)
        {
            return;
        }

        sender.FromDto(dto);
    }

    private async void UpdateContractsListBtn_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        await UpdateContractsList();
    }

    private async Task UpdateContractsList()
    {
        contractControls.Clear();

        var response = await ApiHelper.GetAllContracts();

        if (response == null || !response.IsSuccessStatusCode)
        {
            await ProcessResponseErroStatusCode(response);
            return;
        }

        var contracts = await response.Content.ReadFromJsonAsync<List<ContractDto>>();

        if (contracts != null)
        {
            if (contracts.Count == 0)
            {
                Shell.Notify($"{"Empty".GetLocalized()}!", "NoContractsFound".GetLocalized());
                return;
            }
            
            foreach (var contract in contracts)
            {
                var control = new ContractControl(contract);
                control.ExportRequested += async (s) => await ExportContract(s);
                control.PlanRequested += async (s) => await PlanContract(s);
                control.EditRequested += async (s) => await EditContract(s);
                control.DeleteRequested += async (s) => await DeleteContract(s);
                control.AlertRequested += async (s) => await AlertContract(s);
                contractControls.Add(control);
            }

            ResortContractsList();
        }
        else
        {
            Shell.Notify("RequestRuntimeError".GetLocalized(), "CheckInternetConnectionOrLogin".GetLocalized());
        }
    }

    private void NotifyPropertyChanged([CallerMemberName] string propertyName = "")
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    private void ResortContractsList()
    {
        if (SortingType != SortingType.None)
        {
            switch (SortingType)
            {
                case SortingType.Bailee:
                    contractControls = new(contractControls.OrderBy(c => c.Bailee));
                    break;
                case SortingType.Address:
                    contractControls = new(contractControls.OrderBy(c => c.Address));
                    break;
                case SortingType.AlarmsCount:
                    contractControls = new(contractControls.OrderBy(c => c.Alarms.Count));
                    break;
            }

            NotifyPropertyChanged(nameof(contractControls));
        }
    }

    private async void SortNone_Click(object sender, RoutedEventArgs e)
    {
        SortingType = SortingType.None;
        await UpdateContractsList();
    }

    private void SortName_Click(object sender, RoutedEventArgs e)
    {
        SortingType = SortingType.Bailee;
        ResortContractsList();
    }

    private void SortAddress_Click(object sender, RoutedEventArgs e)
    {
        SortingType = SortingType.Address;
        ResortContractsList();
    }

    private void SortAlarms_Click(object sender, RoutedEventArgs e)
    {
        SortingType = SortingType.AlarmsCount;
        ResortContractsList();
    }

    private async Task ProcessResponseErroStatusCode(HttpResponseMessage? response, string? defaultMessage = null)
    {
        if (response == null)
        {
            Shell.Notify("Error".GetLocalized(), "ServerNotRespondingErrorDescription".GetLocalized());
            return;
        }

        switch (response.StatusCode)
        {
            case System.Net.HttpStatusCode.Unauthorized:
                Shell.Notify("Error".GetLocalized(), "NotAuthorizedErrorDescription".GetLocalized());
                break;
            case System.Net.HttpStatusCode.Forbidden:
                Shell.Notify("Error".GetLocalized(), "NotAllowedErrorDescription".GetLocalized());
                break;
            case System.Net.HttpStatusCode.NotFound:
                Shell.Notify("Error".GetLocalized(), "NotFoundErrorDescription".GetLocalized());
                break;
            case System.Net.HttpStatusCode.TooManyRequests:
                Shell.Notify("Error".GetLocalized(), "TooManyRequestsErrorDescription".GetLocalized());
                break;
            case System.Net.HttpStatusCode.InternalServerError:
                Shell.Notify("Error".GetLocalized(), "InternalServerErrorDescription".GetLocalized());
                System.Diagnostics.Debug.WriteLine(await response.Content.ReadAsStringAsync());
                break;
            case System.Net.HttpStatusCode.BadRequest:
                Shell.Notify("Error".GetLocalized(), "BadRequestErrorDescription".GetLocalized());
                break;
            default:
                Shell.Notify("Error".GetLocalized(), defaultMessage ?? "DefaultErrorMessageDescription".GetLocalized());
                break;
        }
    }

    private async void Page_Loaded(object sender, RoutedEventArgs e)
    {
        await UpdateContractsList();
    }
}
