using Microsoft.UI.Xaml.Controls;

namespace Shield.App.Controls;

public sealed partial class RegisterLoginContent : UserControl
{
    public string Login => LoginTB.Text;
    public string Password => PasswordTB.Password;

    public RegisterLoginContent()
    {
        this.InitializeComponent();
    }
}
