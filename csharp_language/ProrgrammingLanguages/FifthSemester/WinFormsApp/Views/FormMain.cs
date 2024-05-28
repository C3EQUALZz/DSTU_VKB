using WinFormsApp.Core.Classes;
using WinFormsApp.Presenters;
using WinFormsApp.Core.Interfaces.Views;
using WinFormsApp.Core.Classes.UIElements.Menu;

namespace WinFormsApp.Views;

public partial class FormMain : BaseForm, IMenuView
{
    public event EventHandler? MinimizeClicked;
    public event EventHandler? MaximizeClicked;
    public event EventHandler? CloseClicked;
    public event EventHandler? MenuButtonClicked;
    private readonly SideBar _sideBar;

    public FormMain()
    {
        InitializeComponent();
        var _ = new PresenterWithMenu(this);
        _sideBar = new SideBar(MenuPanel, LabelMenu, MenuButton);
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
        _sideBar.UpdateMenu(isCollapsed);
    }









}
