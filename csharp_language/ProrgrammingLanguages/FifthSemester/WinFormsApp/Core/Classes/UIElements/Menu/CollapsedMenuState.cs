using WinFormsApp.Core.Interfaces.UIElements;

namespace WinFormsApp.Core.Classes.UIElements.Menu;

public class CollapsedMenuState : IMenuState
{
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

    public int GetMenuWidth() => 100;
}
