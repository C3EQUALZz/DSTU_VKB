using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using Microsoft.UI;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Media;
using Shield.App.Controls;
using Shield.App.Helpers;
using Windows.Storage;
using Windows.Storage.Pickers;

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

    public string Bailee => BaileeTB.Text;
    public string Address => AddressTB.Text;
    public string Comment => CommentTB.Text;
    public List<string> Owners => OwnersControls.Select(x => x.Value).ToList();

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

    private async void LoadPhotoButtonClick(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {        
        var file = await FilePickerHelper.PickSingleFile();

        if (file != null)
        {
            PhotoPath = file.Name;
            PhotoPathTB.Foreground = new SolidColorBrush(Colors.White);
        }
        else
        {
            PhotoPath = "ошибка";
            PhotoPathTB.Foreground = new SolidColorBrush(Colors.IndianRed);
        }
    }

    private async void LoadPlanButtonClick(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        var file = await FilePickerHelper.PickSingleFile("rvt");

        if (file != null)
        {
            PlanPath = file.Name;
            PlanPathTB.Foreground = new SolidColorBrush(Colors.White);
        }
        else
        {
            PlanPath = "ошибка";
            PlanPathTB.Foreground = new SolidColorBrush(Colors.IndianRed);
        }
    }
}
