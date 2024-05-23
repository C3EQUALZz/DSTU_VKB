namespace WinFormsApp.Core.Interfaces.Views;


/// <summary>
/// Общий интерфейс представление (MVP), которое должно выполнять каждое окно. 
/// </summary>
public interface IView
{
    event EventHandler MinimizeClicked;
    event EventHandler MaximizeClicked;
    event EventHandler CloseClicked;

    Size FormSize { get; set; }
    FormWindowState WindowState { get; set; }
    Padding FormPadding { get; set; }
}


