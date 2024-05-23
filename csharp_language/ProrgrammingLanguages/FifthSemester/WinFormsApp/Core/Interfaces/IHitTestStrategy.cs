namespace WinFormsApp.Core.Interfaces;

/// <summary>
/// Интерфейс стратегии обработки хит-теста
/// </summary>
public interface IHitTestStrategy
{
    IntPtr GetHitTestResult(Point clientPoint, Size size, int resizeAreaSize);
}

