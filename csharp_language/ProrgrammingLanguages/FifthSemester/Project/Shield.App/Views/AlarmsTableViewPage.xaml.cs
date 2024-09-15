using CommunityToolkit.WinUI.UI.Controls;
using Microsoft.UI.Xaml.Controls;
using Shield.App.ViewModels;
using Shield.DataAccess.DTOs;

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
}
