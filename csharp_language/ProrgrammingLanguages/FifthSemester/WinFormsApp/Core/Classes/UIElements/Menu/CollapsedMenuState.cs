using WinFormsApp.Core.Interfaces.UIElements;

namespace WinFormsApp.Core.Classes.UIElements.Menu;

/// <summary>
/// Представляет свернутое состояние меню. Реализует интерфейс <see cref="IMenuState"/>.
/// </summary>
public class CollapsedMenuState : IMenuState
{
    /// <summary>
    /// Убирает текст кнопок в панели меню, чтобы отразить свернутое состояние.
    /// </summary>
    /// <param name="menuPanel">Панель, содержащая кнопки меню.</param>
    public void UpdateButtonText(Panel menuPanel)
    {
        if (menuPanel.InvokeRequired)
        {
            menuPanel.Invoke(new Action(() => UpdateButtonText(menuPanel)));
            return;
        }

        foreach (Button menuButton in menuPanel.Controls.OfType<Button>())
        {
            if (menuButton.Tag is null)
                continue;

            menuButton.Text = "";
            menuButton.ImageAlign = ContentAlignment.MiddleCenter;
            menuButton.Padding = new Padding(0);
        }
    }

    /// <summary>
    /// Нужно для того, чтобы выровнять иконку по центру, которая находится слева от текста. 
    /// У нас при сворачивании удаляется текст, так что происходит такое вот телодвижение. 
    /// </summary>
    /// <param name="labelMenu">Метка, связанная с меню.</param>
    /// <param name="menuButton">Кнопка, используемая для переключения меню.</param>
    public void UpdateMenuProperties(Label labelMenu, Button menuButton)
    {
        if (labelMenu.InvokeRequired)
        {
            labelMenu.Invoke(new Action(() => UpdateMenuProperties(labelMenu, menuButton)));
            return;
        }

        labelMenu.Visible = false;
        menuButton.Dock = DockStyle.Top;
    }

    /// <summary>
    /// Возвращает ширину меню в свернутом состоянии.
    /// </summary>
    /// <returns>Ширина меню в свернутом состоянии.</returns>
    public int GetMenuWidth() => 100;
}
