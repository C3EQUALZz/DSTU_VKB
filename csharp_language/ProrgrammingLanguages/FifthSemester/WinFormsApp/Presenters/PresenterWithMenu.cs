using WinFormsApp.Core.Interfaces.Views;

namespace WinFormsApp.Presenters;


/// <summary>
/// Презентер, который может работать с Form, у которого есть Menu
/// </summary>
public class PresenterWithMenu
{
    private readonly IMenuView _view;
    private Size _formSize;

    public PresenterWithMenu(IMenuView view)
    {
        _view = view;
        _view.MinimizeClicked += OnMinimizeClicked;
        _view.MaximizeClicked += OnMaximizeClicked;
        _view.CloseClicked += OnCloseClicked;
        _view.MenuButtonClicked += OnMenuButtonClicked;
    }

    /// <summary>
    /// Логика обработки нажатия на кнопку, когда пользователь сворачивает приложение
    /// </summary>
    private void OnMinimizeClicked(object? sender, EventArgs e)
    {
        _formSize = _view.FormSize;
        _view.WindowState = FormWindowState.Minimized;
    }

    /// <summary>
    /// Логика обработки нажатия на кнопку, когда пользователь разворачивает на весь экран приложение
    /// </summary>
    private void OnMaximizeClicked(object? sender, EventArgs e)
    {
        if (_view.WindowState == FormWindowState.Normal)
        {
            _formSize = _view.FormSize;
            _view.WindowState = FormWindowState.Maximized;
        }

        else
        {
            _view.WindowState = FormWindowState.Normal;
            _view.FormSize = _formSize;

        }

    }

    /// <summary>
    /// Логика закрытия приложения
    /// </summary>
    private void OnCloseClicked(object? sender, EventArgs e)
    {
        Application.Exit();
    }

    /// <summary>
    /// Логика нажатия на меню
    /// </summary>
    private void OnMenuButtonClicked(object? sender, EventArgs e)
    {
        var isCollapsed = _view.MenuPanelWidth > 200;
        _view.UpdateMenu(isCollapsed);
    }

}
