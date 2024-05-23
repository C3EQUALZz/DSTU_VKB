using WinFormsApp.Core.Classes;
using WinFormsApp.Presenters;
using WinFormsApp.Core.Interfaces.Views;

namespace WinFormsApp.Views;

public partial class FormMain : BaseForm, IMenuView
{
    public event EventHandler? MinimizeClicked;
    public event EventHandler? MaximizeClicked;
    public event EventHandler? CloseClicked;
    public event EventHandler? MenuButtonClicked;

    public FormMain()
    {
        InitializeComponent();
        var _ = new PresenterWithMenu(this);
    }

    public Size FormSize
    {
        get => ClientSize;
        set => ClientSize = value;
    }

    public new FormWindowState WindowState
    {
        get => base.WindowState;
        set => base.WindowState = value;
    }

    public Padding FormPadding
    {
        get => Padding;
        set => Padding = value;
    }

    public int MenuPanelWidth
    {
        get => MenuPanel.Width;
        set => MenuPanel.Width = value;
    }

    private void MinimizeButton_Click(object sender, EventArgs e)
    {
        MinimizeClicked?.Invoke(this, EventArgs.Empty);
    }

    private void MaximizeButton_Click(object sender, EventArgs e)
    {
        MaximizeClicked?.Invoke(this, EventArgs.Empty);
    }

    private void CloseButton_Click(object sender, EventArgs e)
    {
        CloseClicked?.Invoke(this, EventArgs.Empty);
    }

    private void MenuButton_Click(object sender, EventArgs e)
    {
        MenuButtonClicked?.Invoke(this, EventArgs.Empty);
    }

    public void UpdateMenu(bool isCollapsed)
    {
        if (isCollapsed)
        {
            MenuPanel.Width = 100;
            LabelMenu.Visible = false;
            MenuButton.Dock = DockStyle.Top;
            foreach (Button menuButton in MenuPanel.Controls.OfType<Button>())
            {
                menuButton.Text = "";
                menuButton.ImageAlign = ContentAlignment.MiddleCenter;
                menuButton.Padding = new Padding(0);
            }
        }
        else
        {
            MenuPanel.Width = 230;
            LabelMenu.Visible = true;
            MenuButton.Dock = DockStyle.None;
            foreach (Button menuButton in MenuPanel.Controls.OfType<Button>())
            {
                if (menuButton.Tag is null)
                    continue;
                menuButton.Text = "  " + menuButton.Tag.ToString();
                menuButton.ImageAlign = ContentAlignment.MiddleLeft;
                menuButton.Padding = new Padding(10, 0, 0, 0);
            }
        }
    }

}
