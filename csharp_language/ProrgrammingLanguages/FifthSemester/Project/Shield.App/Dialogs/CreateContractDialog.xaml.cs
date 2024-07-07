using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using Microsoft.UI.Xaml.Controls;

using Shield.App.Controls;

namespace Shield.App.Dialogs;
public sealed partial class CreateContractDialog : UserControl, INotifyPropertyChanged
{
    private string _planPath = string.Empty;
    public string PlanPath
    {
        get => _planPath;
        set
        {
            if (value != _planPath)
            {
                _planPath = value;
                NotifyPropertyChanged();
            }
        }
    }

    private string _photoPath = string.Empty;
    public string PhotoPath
    {
        get => _photoPath;
        set
        {
            if (value != _photoPath)
            {
                _photoPath = value;
                NotifyPropertyChanged();
            }
        }
    }

    private ObservableCollection<RemovableTextBox> OwnersControls { get; set; } = new();

    public event PropertyChangedEventHandler PropertyChanged;

    public CreateContractDialog()
    {
        this.InitializeComponent();
    }

    private void NotifyPropertyChanged([CallerMemberName] string propertyName = "")
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    private void AddOwnerButtonClick(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        var rtb = new RemovableTextBox();
        rtb.RemoveRequested += (sender) =>
        {
            OwnersControls.Remove(rtb);
        };
        OwnersControls.Add(rtb);
    }
}
