namespace WinFormsApp.Core.Interfaces.Views;

/// <summary>
/// Специализированный интерфейс для основного окна с меню и лабораторными
/// </summary>
public interface IMenuView : IView
{
    event EventHandler MenuButtonClicked;
    void UpdateMenu(bool isCollapsed);
    int MenuPanelWidth { get; set; }
}
