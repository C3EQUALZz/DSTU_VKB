using Microsoft.UI.Xaml.Controls;
using Shield.App.ViewModels;

namespace Shield.App.Views;
public sealed partial class AlarmsPage : Page
{
    public AlarmsViewModel ViewModel
    {
        get;
    }

    public AlarmsPage()
    {
        ViewModel = App.GetService<AlarmsViewModel>();
        this.InitializeComponent();
    }
}
