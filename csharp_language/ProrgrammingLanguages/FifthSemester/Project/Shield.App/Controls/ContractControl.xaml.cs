using System.ComponentModel;
using System.Runtime.CompilerServices;
using Microsoft.UI.Xaml.Controls;
using Shield.DataAccess.Models;

namespace Shield.App.Controls;
public sealed partial class ContractControl : UserControl, INotifyPropertyChanged
{
    public int ContractId { get; set; }
    public string Address { get; set; }
    public string Owners { get; set; }
    public string Bailee { get; set; }
    public Plan Plan { get; set; }

    public event PropertyChangedEventHandler PropertyChanged;
    
    public ContractControl()
    {
        this.InitializeComponent();
    }

    public ContractControl(Contract c)
    {
        ContractId = c.ContractId;
        Address = c.Address;
        Plan = c.Plan;
        Owners = c.Owners;
        Bailee = c.Bailee;
        InitializeComponent();
    }

    private void NotifyPropertyChanged([CallerMemberName] string propertyName = "")
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}
