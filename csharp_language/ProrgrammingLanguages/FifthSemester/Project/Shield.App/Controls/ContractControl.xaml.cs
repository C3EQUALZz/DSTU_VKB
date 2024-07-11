using System.ComponentModel;
using System.Runtime.CompilerServices;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Media.Imaging;
using Shield.App.Helpers;
using Shield.DataAccess.Models;

namespace Shield.App.Controls;
public sealed partial class ContractControl : UserControl, INotifyPropertyChanged
{
    public int ContractId { get; set; }
    public string Address { get; set; }
    public string Owners { get; set; }
    public string Bailee { get; set; }
    public string Comment { get; set; }
    public Plan Plan { get; set; }
    public BitmapImage Bitmap { get; set; }

    public delegate void ExportRequestedHandler(ContractControl sender);
    public delegate void UpdateRequestedHandler(ContractControl sender);
    public delegate void DeleteRequestedHandler(ContractControl sender);
    public delegate void AlertRequestedHandler(ContractControl sender);

    public event ExportRequestedHandler ExportRequested;
    public event UpdateRequestedHandler UpdateRequested;
    public event DeleteRequestedHandler DeleteRequested;
    public event AlertRequestedHandler AlertRequested;

    public event PropertyChangedEventHandler PropertyChanged;
    
    public ContractControl()
    {
        this.InitializeComponent();
    }

    public ContractControl(Contract c)
    {
        ContractId = c.ContractId;
        Address = c.Address;
        Owners = c.Owners;
        Bailee = c.Bailee;
        Comment = c.Comment;
        Plan = c.Plan;
        Bitmap = BitmapHelper.BytesToBitmap(c.Picture.Data);

        InitializeComponent();
    }

    private void NotifyPropertyChanged([CallerMemberName] string propertyName = "")
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}
