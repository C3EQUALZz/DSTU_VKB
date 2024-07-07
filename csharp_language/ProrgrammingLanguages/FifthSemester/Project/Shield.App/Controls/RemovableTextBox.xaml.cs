using Microsoft.UI.Xaml.Controls;

namespace Shield.App.Controls;
public sealed partial class RemovableTextBox : UserControl
{
    public string Value => TB.Text;

    public delegate void RemoveRequestedHandler(RemovableTextBox sender);
    public event RemoveRequestedHandler RemoveRequested;

    public RemovableTextBox()
    {
        this.InitializeComponent();
    }

    private void RB_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        RemoveRequested?.Invoke(this);
    }
}
