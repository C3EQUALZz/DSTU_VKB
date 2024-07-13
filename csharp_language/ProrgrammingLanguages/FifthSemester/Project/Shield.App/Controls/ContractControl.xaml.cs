using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Media.Imaging;
using Shield.App.Helpers;
using Shield.DataAccess.DTOs;

namespace Shield.App.Controls;
public sealed partial class ContractControl : UserControl, INotifyPropertyChanged
{
    public int ContractId { get; set; }
    public string Address { get; set; }
    public string? OwnersString { get; set; }
    public ObservableCollection<TextBlock> OwnersControls { get; set; } = new();
    public string Bailee { get; set; }
    public string? Comment { get; set; }
    public PlanDto Plan { get; set; }
    public PictureDto Picture { get; set; }
    public BitmapImage Bitmap { get; set; }
    public DateOnly Date { get; set; }
    public List<AlarmDto> Alarms { get; set; }

    public delegate void ExportRequestedHandler(ContractControl sender);
    public delegate void PlanRequestedHandler(ContractControl sender);
    public delegate void EditRequestedHandler(ContractControl sender);
    public delegate void DeleteRequestedHandler(ContractControl sender);
    public delegate void AlertRequestedHandler(ContractControl sender);

    public event ExportRequestedHandler ExportRequested;
    public event PlanRequestedHandler PlanRequested;
    public event EditRequestedHandler EditRequested;
    public event DeleteRequestedHandler DeleteRequested;
    public event AlertRequestedHandler AlertRequested;

    public event PropertyChangedEventHandler PropertyChanged;
    
    public ContractControl()
    {
        this.InitializeComponent();
    }

    public ContractControl(ContractDto c)
    {
        ContractId = c.ContractId;
        Address = c.Address;
        OwnersString = c.Owners;
        Bailee = c.Bailee;
        Comment = c.Comment;
        Plan = c.Plan;
        Date = c.SignDate;
        Picture = c.Picture;
        Alarms = c.Alarms.ToList();
        Bitmap = BitmapHelper.BytesToBitmap(c.Picture.Data);

        var baileeTB = new TextBlock();
        baileeTB.Text = "1. " + Bailee;
        OwnersControls.Add(baileeTB);

        if (OwnersString != null)
        {
            var splittedOwners = OwnersString.Split(';');
            for (var i = 0; i < splittedOwners.Count(); i++)
            {
                var tb = new TextBlock();
                tb.Text = $"{i + 2}. {splittedOwners[i]}";
                OwnersControls.Add(tb);
            }
        }

        InitializeComponent();
    }

    // Возвращает ContractDto, где Plan = null
    public ContractDto ToDto(bool keepDate = true)
    {
        return new ContractDto()
        {
            Bailee = Bailee,
            Address = Address,
            Comment = Comment,
            Owners = OwnersString,
            Picture = new()
            {
                Title = Picture.Title,
                Type = Picture.Type,
                Data = Picture.Data
            },
            SignDate = keepDate ? Date : DateOnly.FromDateTime(DateTime.Now)
        };
    } 

    private void NotifyPropertyChanged([CallerMemberName] string propertyName = "")
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    private void ExportButton_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        ExportRequested?.Invoke(this);
    }

    private void EditButton_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        EditRequested?.Invoke(this);
    }

    private void DeleteButton_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        DeleteRequested?.Invoke(this);
    }

    private void AlertButton_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        AlertRequested?.Invoke(this);
    }

    private void PlanButton_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        PlanRequested?.Invoke(this);
    }
}
