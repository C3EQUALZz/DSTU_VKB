namespace SecondLaboratory.Core.AbstractClasses;

public class AbstractPresenter
{
    /// <summary>
    /// Логика закрытия приложения
    /// </summary>
    protected void OnCloseClicked(object? sender, EventArgs e)
    {
        Application.Exit();
    }
}