using System.Collections.ObjectModel;
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

    private async void Page_Loaded(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        ViewModel.Alarms = await ViewModel.GetAlarms();
    }

    private void DataGrid_Sorting(object sender, CommunityToolkit.WinUI.UI.Controls.DataGridColumnEventArgs e)
    {
        var dg = sender as DataGrid;

        if (e.Column.Tag.ToString() == "AlarmId")
        {
            if (e.Column.SortDirection == null || e.Column.SortDirection == DataGridSortDirection.Descending)
            {
                dg.ItemsSource = new List<AlarmDto>(from item in ViewModel.Alarms
                                                    orderby item.AlarmId ascending
                                                    select item);
                e.Column.SortDirection = DataGridSortDirection.Ascending;
            }
            else
            {
                dg.ItemsSource = new List<AlarmDto>(from item in ViewModel.Alarms
                                                    orderby item.AlarmId descending
                                                    select item);
                e.Column.SortDirection = DataGridSortDirection.Descending;
            }
        }
        else if (e.Column.Tag.ToString() == "Date")
        {
            if (e.Column.SortDirection == null || e.Column.SortDirection == DataGridSortDirection.Descending)
            {
                dg.ItemsSource = new List<AlarmDto>(from item in ViewModel.Alarms
                                                    orderby item.Date ascending
                                                    select item);
                e.Column.SortDirection = DataGridSortDirection.Ascending;
            }
            else
            {
                dg.ItemsSource = new List<AlarmDto>(from item in ViewModel.Alarms
                                                    orderby item.Date descending
                                                    select item);
                e.Column.SortDirection = DataGridSortDirection.Descending;
            }
        }
        else if (e.Column.Tag.ToString() == "Organization")
        {
            if (e.Column.SortDirection == null || e.Column.SortDirection == DataGridSortDirection.Descending)
            {
                dg.ItemsSource = new List<AlarmDto>(from item in ViewModel.Alarms
                                                    orderby item.Organization ascending
                                                    select item);
                e.Column.SortDirection = DataGridSortDirection.Ascending;
            }
            else
            {
                dg.ItemsSource = new List<AlarmDto>(from item in ViewModel.Alarms
                                                    orderby item.Organization descending
                                                    select item);
                e.Column.SortDirection = DataGridSortDirection.Descending;
            }
        }
        else if (e.Column.Tag.ToString() == "Address")
        {
            if (e.Column.SortDirection == null || e.Column.SortDirection == DataGridSortDirection.Descending)
            {
                dg.ItemsSource = new List<AlarmDto>(from item in ViewModel.Alarms
                                                    orderby item.Address ascending
                                                    select item);
                e.Column.SortDirection = DataGridSortDirection.Ascending;
            }
            else
            {
                dg.ItemsSource = new List<AlarmDto>(from item in ViewModel.Alarms
                                                    orderby item.Address descending
                                                    select item);
                e.Column.SortDirection = DataGridSortDirection.Descending;
            }
        }
        else if (e.Column.Tag.ToString() == "Result")
        {
            if (e.Column.SortDirection == null || e.Column.SortDirection == DataGridSortDirection.Descending)
            {
                dg.ItemsSource = new List<AlarmDto>(from item in ViewModel.Alarms
                                                    orderby item.Result ascending
                                                    select item);
                e.Column.SortDirection = DataGridSortDirection.Ascending;
            }
            else
            {
                dg.ItemsSource = new List<AlarmDto>(from item in ViewModel.Alarms
                                                    orderby item.Result descending
                                                    select item);
                e.Column.SortDirection = DataGridSortDirection.Descending;
            }
        }

        // Reset sotring in other columns
        foreach (var dgColumn in dg.Columns)
        {
            if (dgColumn.Tag.ToString() != e.Column.Tag.ToString())
            {
                dgColumn.SortDirection = null;
            }
        }
    }
}
