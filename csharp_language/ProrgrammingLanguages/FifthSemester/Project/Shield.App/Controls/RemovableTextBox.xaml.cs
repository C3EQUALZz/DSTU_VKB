using Microsoft.UI.Xaml.Controls;

namespace Shield.App.Controls;
public sealed partial class RemovableTextBox : UserControl
{
    public string Value
    {
        get => TB.Text;
        set => TB.Text = value;
    }

    public delegate void TextChangedHandler(RemovableTextBox sender, TextBox tbsender, TextChangedEventArgs e);
    public event TextChangedHandler TextChanged;

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

    private void TB_TextChanged(object sender, TextChangedEventArgs e)
    {
        TextChanged?.Invoke(this, (TextBox)sender, e);
    }
}
