namespace WinFormsApp.Core.Interfaces.UIElements;

public interface IMenuState
{
    void UpdateButtonText(Panel menuPanel);
    void UpdateMenuProperties(Label labelMenu, Button menuButton);
    int GetMenuWidth();
}
