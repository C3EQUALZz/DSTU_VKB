using Microsoft.UI.Xaml.Controls;
using Shield.App.ViewModels;

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
}
