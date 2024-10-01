using System.Reflection;
using CommunityToolkit.WinUI.UI.Controls;
using Microsoft.UI.Xaml.Controls;
using Shield.App.Helpers;
using Shield.App.Misc;
using Shield.App.ViewModels;
using Shield.DataAccess.DTOs;
using Spire.Doc;

namespace Shield.App.Views;
public sealed partial class AlarmsTableViewPage : Page
{
    public AlarmsTableViewViewModel ViewModel
    {
        get;
    }

    public AlarmsTableViewPage()
    {
        ViewModel = App.GetService<AlarmsTableViewViewModel>();
        InitializeComponent();
    }

    private void ApplyFiltering()
    {
        ViewModel.Alarms = new(from item in ViewModel.AlarmsDB
                           where ViewModel.PickedFrom == null || ViewModel.PickedFrom.Value.Date <= item.Date.Value.Date
                           where ViewModel.PickedUntil == null || item.Date.Value.Date <= ViewModel.PickedUntil.Value.Date
                           select item);
    }
    private void ApplySorting(DataGridColumn? columnToSort = null, bool preserveDirection = true)
    {
        columnToSort ??= AlarmsDG.Columns.ToList().Find(c => c.SortDirection != null);

        if (columnToSort != null)
        {
            if (columnToSort.Tag.ToString() == "AlarmId")
            {
                if (preserveDirection == false || columnToSort.SortDirection == null)
                {
                    if (columnToSort.SortDirection == null || columnToSort.SortDirection == CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Descending)
                    {
                        ViewModel.Alarms = new(from item in ViewModel.Alarms
                                               orderby item.AlarmId ascending
                                               select item);
                        columnToSort.SortDirection = CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Ascending;
                    }
                    else
                    {
                        ViewModel.Alarms = new(from item in ViewModel.Alarms
                                               orderby item.AlarmId descending
                                               select item);
                        columnToSort.SortDirection = CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Descending;
                    }
                }
                else
                {
                    if (columnToSort.SortDirection == null || columnToSort.SortDirection == CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Descending)
                    {
                        ViewModel.Alarms = new(from item in ViewModel.Alarms
                                               orderby item.AlarmId descending
                                               select item);
                        columnToSort.SortDirection = CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Descending;
                    }
                    else
                    {
                        ViewModel.Alarms = new(from item in ViewModel.Alarms
                                               orderby item.AlarmId ascending
                                               select item);
                        columnToSort.SortDirection = CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Ascending;
                    }
                }
            }
            else if (columnToSort.Tag.ToString() == "Date")
            {
                if (preserveDirection == false || columnToSort.SortDirection == null)
                {
                    if (columnToSort.SortDirection == null || columnToSort.SortDirection == CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Descending)
                    {
                        ViewModel.Alarms = new(from item in ViewModel.Alarms
                                               orderby item.Date ascending
                                               select item);
                        columnToSort.SortDirection = CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Ascending;
                    }
                    else
                    {
                        ViewModel.Alarms = new(from item in ViewModel.Alarms
                                               orderby item.Date descending
                                               select item);
                        columnToSort.SortDirection = CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Descending;
                    }
                }
                else
                {
                    if (columnToSort.SortDirection == null || columnToSort.SortDirection == CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Descending)
                    {
                        ViewModel.Alarms = new(from item in ViewModel.Alarms
                                               orderby item.Date descending
                                               select item);
                        columnToSort.SortDirection = CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Descending;
                    }
                    else
                    {
                        ViewModel.Alarms = new(from item in ViewModel.Alarms
                                               orderby item.Date ascending
                                               select item);
                        columnToSort.SortDirection = CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Ascending;
                    }
                }
            }
            else if (columnToSort.Tag.ToString() == "Organization")
            {
                if (preserveDirection == false || columnToSort.SortDirection == null)
                {
                    if (columnToSort.SortDirection == null || columnToSort.SortDirection == CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Descending)
                    {
                        ViewModel.Alarms = new(from item in ViewModel.Alarms
                                               orderby item.Organization ascending
                                               select item);
                        columnToSort.SortDirection = CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Ascending;
                    }
                    else
                    {
                        ViewModel.Alarms = new(from item in ViewModel.Alarms
                                               orderby item.Organization descending
                                               select item);
                        columnToSort.SortDirection = CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Descending;
                    }
                }
                else
                {
                    if (columnToSort.SortDirection == null || columnToSort.SortDirection == CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Descending)
                    {
                        ViewModel.Alarms = new(from item in ViewModel.Alarms
                                               orderby item.Organization descending
                                               select item);
                        columnToSort.SortDirection = CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Descending;
                    }
                    else
                    {
                        ViewModel.Alarms = new(from item in ViewModel.Alarms
                                               orderby item.Organization ascending
                                               select item);
                        columnToSort.SortDirection = CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Ascending;
                    }
                }
            }
            else if (columnToSort.Tag.ToString() == "Address")
            {
                if (preserveDirection == false || columnToSort.SortDirection == null)
                {
                    if (columnToSort.SortDirection == null || columnToSort.SortDirection == CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Descending)
                    {
                        ViewModel.Alarms = new(from item in ViewModel.Alarms
                                               orderby item.Address ascending
                                               select item);
                        columnToSort.SortDirection = CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Ascending;
                    }
                    else
                    {
                        ViewModel.Alarms = new(from item in ViewModel.Alarms
                                               orderby item.Address descending
                                               select item);
                        columnToSort.SortDirection = CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Descending;
                    }
                }
                else
                {
                    if (columnToSort.SortDirection == null || columnToSort.SortDirection == CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Descending)
                    {
                        ViewModel.Alarms = new(from item in ViewModel.Alarms
                                               orderby item.Address descending
                                               select item);
                        columnToSort.SortDirection = CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Descending;
                    }
                    else
                    {
                        ViewModel.Alarms = new(from item in ViewModel.Alarms
                                               orderby item.Address ascending
                                               select item);
                        columnToSort.SortDirection = CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Ascending;
                    }
                }
            }
            else if (columnToSort.Tag.ToString() == "Result")
            {
                if (preserveDirection == false || columnToSort.SortDirection == null)
                {
                    if (columnToSort.SortDirection == null || columnToSort.SortDirection == CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Descending)
                    {
                        ViewModel.Alarms = new(from item in ViewModel.Alarms
                                               orderby item.Result ascending
                                               select item);
                        columnToSort.SortDirection = CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Ascending;
                    }
                    else
                    {
                        ViewModel.Alarms = new(from item in ViewModel.Alarms
                                               orderby item.Result descending
                                               select item);
                        columnToSort.SortDirection = CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Descending;
                    }
                }
                else
                {
                    if (columnToSort.SortDirection == null || columnToSort.SortDirection == CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Descending)
                    {
                        ViewModel.Alarms = new(from item in ViewModel.Alarms
                                               orderby item.Result descending
                                               select item);
                        columnToSort.SortDirection = CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Descending;
                    }
                    else
                    {
                        ViewModel.Alarms = new(from item in ViewModel.Alarms
                                               orderby item.Result ascending
                                               select item);
                        columnToSort.SortDirection = CommunityToolkit.WinUI.UI.Controls.DataGridSortDirection.Ascending;
                    }
                }
            }

            // Reset sotring in other columns
            foreach (var dgColumn in AlarmsDG.Columns)
            {
                if (dgColumn.Tag.ToString() != columnToSort.Tag.ToString())
                {
                    dgColumn.SortDirection = null;
                }
            }
        }
    }

    private async void Page_Loaded(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        await ViewModel.LoadAlarms();
        ShowAllCB.IsChecked = true;
    }

    private void DataGrid_Sorting(object sender, CommunityToolkit.WinUI.UI.Controls.DataGridColumnEventArgs e)
    {
        ApplySorting(e.Column, false);
    }

    private void ShowAllCB_Checked(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        ViewModel.EnableSearch = false;

        ViewModel.PickedFrom = null;
        ViewModel.PickedUntil = null;
        FromCDP.Date = null;
        UntilCDP.Date = null;

        ApplyFiltering();
        ApplySorting();
    }
    private void ShowAllCB_Unchecked(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        ViewModel.EnableSearch = true;
    }

    private void FromCDP_DateChanged(CalendarDatePicker sender, CalendarDatePickerDateChangedEventArgs args)
    {
        ViewModel.PickedFrom = args.NewDate;
        ApplyFiltering();
        ApplySorting();
    }
    private void UntilCDP_DateChanged(CalendarDatePicker sender, CalendarDatePickerDateChangedEventArgs args)
    {
        ViewModel.PickedUntil = args.NewDate;
        ApplyFiltering();
        ApplySorting();
    }

    private async void ExportMFI_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        var menuFlyoutItem = sender as MenuFlyoutItem;

        if (menuFlyoutItem?.DataContext is AlarmDto alarm)
        {
            // Вызовем диалоговое окно выбора файла, чтобы узнать, куда пользователь хочет сохранить отчет

            var savePicker = new Windows.Storage.Pickers.FileSavePicker();
            savePicker.SuggestedStartLocation = Windows.Storage.Pickers.PickerLocationId.Desktop;
            savePicker.FileTypeChoices.Add("Word Document", new List<string>() { ".docx" });
            savePicker.SuggestedFileName = $"alarm_report_{alarm.AlarmId}";

            var hwnd = App.MainWindow.GetWindowHandle();
            WinRT.Interop.InitializeWithWindow.Initialize(savePicker, hwnd);

            var file = await savePicker.PickSaveFileAsync();

            if (file != null)
            {
                var templatePath = Path.Combine(Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location), "Misc", "WordTemplates", $"{(alarm.Result == DataAccess.Enums.AlarmResult.Robbery ? "alarm_report_steal_template.docx" : "alarm_report_false_template.docx")}");

                // Через Spire.Doc сохраним отчет в выбранный файл

                var doc = new Document();
                doc.LoadFromFile(templatePath);

                var rnd = new Random();
                var stolenItem = StolenItem.Items[rnd.Next(0, StolenItem.Items.Count)];

                var replaceDict = new Dictionary<string, string>()
            {
                { "#contract.Organization#", alarm.Contract.Organization },
                { "#contract.Address#", alarm.Contract.Address },
                { "#report.Date#", DateTime.Now.ToString()[..10] },
                { "#contract.Bailee#", alarm.Contract.Bailee },
                { "#contract.Owners#", alarm.Contract.Owners.Replace(";", ", ") },
                { "#alarm.Date#", alarm.Date.Value.Date.ToString()[..10] },
                { "#alarm.Time#",  $"{alarm.Date.Value.Hour}:{alarm.Date.Value.Minute}:{alarm.Date.Value.Second}"},
                { "#item.Name#",  $"{stolenItem.Name}"},
                { "#item.Meta#",  $"{stolenItem.Meta}"},
                { "#item.Count#",  $"{rnd.Next(0, 1001)}"},
                { "#item.Price#",  $"{stolenItem.Price}"},
            };

                foreach (var kvp in replaceDict)
                {
                    doc.Replace(kvp.Key, kvp.Value, true, true);
                }

                doc.SaveToFile(file.Path);

                doc.Close();

                ShellPage.Instance.Notify("AlarmCreatedNotification".GetLocalized(), $"{"Alarm".GetLocalized()} №{alarm.AlarmId}\n{file.Path}");
            }
        }
    }
}
