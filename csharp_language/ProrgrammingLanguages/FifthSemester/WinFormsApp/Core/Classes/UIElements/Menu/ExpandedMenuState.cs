using WinFormsApp.Core.Interfaces.UIElements;

namespace WinFormsApp.Core.Classes.UIElements.Menu;

/// <summary>
/// Представляет развернутое состояние меню. Реализует интерфейс <see cref="IMenuState"/>.
/// </summary>
public class ExpandedMenuState : IMenuState
{

    /// <summary>
    /// Обновляет текст кнопок в указанной панели меню, чтобы отразить развернутое состояние.
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

            var newText = "  " + menuButton.Tag.ToString();
            menuButton.ImageAlign = ContentAlignment.MiddleLeft;
            menuButton.Padding = new Padding(10, 0, 0, 0);

            TextAnimator.AnimateText(menuButton, newText, 30);
        }
    }

    /// <summary>
    /// Обновляет свойства меню, чтобы отразить развернутое состояние.
    /// </summary>
    /// <param name="labelMenu">Метка меню.</param>
    /// <param name="menuButton">Кнопка меню.</param>
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

    /// <summary>
    /// Возвращает ширину меню в развернутом состоянии.
    /// </summary>
    public int GetMenuWidth() => 230;
}

/// <summary>
/// Предоставляет метод для анимации текста кнопки.
/// </summary>
static class TextAnimator
{
    /// <summary>
    /// Анимирует текст кнопки, постепенно отображая каждый символ.
    /// Нужен для того, чтобы пофиксить баг с резким появлением текста из-за чего происходит разрыв анимации.
    /// </summary>
    /// <param name="button">Кнопка, текст которой нужно анимировать.</param>
    /// <param name="text">Текст для анимации.</param>
    /// <param name="interval">Интервал между появлением каждого символа в миллисекундах.</param>
    public static void AnimateText(Button button, string text, int interval)
    {
        var timer = new System.Windows.Forms.Timer { Interval = interval };
        int currentLength = 0;

        timer.Tick += (s, e) =>
        {
            if (currentLength < text.Length)
            {
                button.Text = text[..(currentLength + 1)];
                currentLength++;
            }
            else
            {
                timer.Stop();
                timer.Dispose();
            }
        };

        timer.Start();
    }
}
