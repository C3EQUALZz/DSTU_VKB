namespace WinFormsApp.Core.Interfaces;

/// <summary>
/// Специализированный интерфейс для основного окна с меню и лабораторными
/// </summary>
public interface IMenuView : IView
{
    event EventHandler MenuButtonClicked;
    void UpdateMenu(bool isCollapsed);
    int MenuPanelWidth { get; set; }
}
