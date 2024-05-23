using WinFormsApp.Core.Interfaces;
using WinFormsApp.Core.Enums.Form;

namespace WinFormsApp.Core.Classes.HitTest;

/// <summary>
/// Стратегия для обработки хит-теста в верхнем левом углу
/// </summary>
public class TopLeftStrategy : IHitTestStrategy
{
    public IntPtr GetHitTestResult(Point clientPoint, Size size, int resizeAreaSize)
    {
        return clientPoint.Y <= resizeAreaSize && clientPoint.X <= resizeAreaSize ? (IntPtr)HitTestConstants.HTTOPLEFT : IntPtr.Zero;
    }
}

/// <summary>
/// Стратегия для обработки хит-теста в верхней части.
/// </summary>
public class TopStrategy : IHitTestStrategy
{
    public IntPtr GetHitTestResult(Point clientPoint, Size size, int resizeAreaSize)
    {
        return clientPoint.Y <= resizeAreaSize && clientPoint.X > resizeAreaSize && clientPoint.X < (size.Width - resizeAreaSize) ? (IntPtr)HitTestConstants.HTTOP : IntPtr.Zero;
    }
}

/// <summary>
/// Стратегия для обработки хит-теста в верхнем правом углу.
/// </summary>
public class TopRightStrategy : IHitTestStrategy
{
    public IntPtr GetHitTestResult(Point clientPoint, Size size, int resizeAreaSize)
    {
        return clientPoint.Y <= resizeAreaSize && clientPoint.X >= (size.Width - resizeAreaSize) ? (IntPtr)HitTestConstants.HTTOPRIGHT : IntPtr.Zero;
    }
}

/// <summary>
/// Стратегия для обработки хит-теста слева.
/// </summary>
public class LeftStrategy : IHitTestStrategy
{
    public IntPtr GetHitTestResult(Point clientPoint, Size size, int resizeAreaSize)
    {
        return clientPoint.Y > resizeAreaSize && clientPoint.Y <= (size.Height - resizeAreaSize) && clientPoint.X <= resizeAreaSize ? (IntPtr)HitTestConstants.HTLEFT : IntPtr.Zero;
    }
}

/// <summary>
/// Стратегия для обработки хит-теста справа.
/// </summary>
public class RightStrategy : IHitTestStrategy
{
    public IntPtr GetHitTestResult(Point clientPoint, Size size, int resizeAreaSize)
    {
        return clientPoint.Y > resizeAreaSize && clientPoint.Y <= (size.Height - resizeAreaSize) && clientPoint.X > (size.Width - resizeAreaSize) ? (IntPtr)HitTestConstants.HTRIGHT : IntPtr.Zero;
    }
}

/// <summary>
/// Стратегия для обработки хит-теста в нижнем левом углу.
/// </summary>
public class BottomLeftStrategy : IHitTestStrategy
{
    public IntPtr GetHitTestResult(Point clientPoint, Size size, int resizeAreaSize)
    {
        return clientPoint.Y > (size.Height - resizeAreaSize) && clientPoint.X <= resizeAreaSize ? (IntPtr)HitTestConstants.HTBOTTOMLEFT : IntPtr.Zero;
    }
}

/// <summary>
/// Стратегия для обработки хит-теста в нижней части.
/// </summary>
public class BottomStrategy : IHitTestStrategy
{
    public IntPtr GetHitTestResult(Point clientPoint, Size size, int resizeAreaSize)
    {
        return clientPoint.Y > (size.Height - resizeAreaSize) && clientPoint.X > resizeAreaSize && clientPoint.X < (size.Width - resizeAreaSize) ? (IntPtr)HitTestConstants.HTBOTTOM : IntPtr.Zero;
    }
}

/// <summary>
/// Стратегия для обработки хит-теста в нижнем правом углу.
/// </summary>
public class BottomRightStrategy : IHitTestStrategy
{
    public IntPtr GetHitTestResult(Point clientPoint, Size size, int resizeAreaSize)
    {
        return clientPoint.Y > (size.Height - resizeAreaSize) && clientPoint.X >= (size.Width - resizeAreaSize) ? (IntPtr)HitTestConstants.HTBOTTOMRIGHT : IntPtr.Zero;
    }
}

/// <summary>
/// Стратегия по умолчанию для обработки хит-теста.
/// </summary>
public class DefaultStrategy : IHitTestStrategy
{
    public IntPtr GetHitTestResult(Point clientPoint, Size size, int resizeAreaSize)
    {
        return (IntPtr)HitTestConstants.HTCLIENT;
    }
}
