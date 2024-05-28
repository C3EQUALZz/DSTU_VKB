using WinFormsApp.Core.Interfaces.UIElements;

namespace WinFormsApp.Core.Classes.UIElements.Menu;

public class ExpandedMenuState : IMenuState
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

            menuButton.Text = "  " + menuButton.Tag.ToString();
            menuButton.ImageAlign = ContentAlignment.MiddleLeft;
            menuButton.Padding = new Padding(10, 0, 0, 0);
        }
    }

    public void UpdateMenuProperties(Label labelMenu, Button menuButton)
    {
        if (labelMenu.InvokeRequired)
        {
            labelMenu.Invoke(new Action(() => UpdateMenuProperties(labelMenu, menuButton)));
            return;
        }

        labelMenu.Visible = true;
        menuButton.Dock = DockStyle.None;
    }

    public int GetMenuWidth() => 230;
}
