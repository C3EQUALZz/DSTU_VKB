using Microsoft.UI.Xaml.Controls;

namespace Shield.App.Controls;

public sealed partial class RegisterContent : UserControl
{
    public string Login => LoginTB.Text;
    public string Email => EmailTB.Text;
    public string Password => PasswordTB.Password;

    public RegisterContent()
    {
        this.InitializeComponent();
    }
}
