using WinFormsApp.Core.Classes.HitTest;
using WinFormsApp.Core.Enums.Form;
using WinFormsApp.Core.Interfaces;

namespace WinFormsApp.Core.Classes;

/// <summary>
/// Фабрика для получения стратегии обработки хит-теста
/// </summary>
public class HitTestStrategyFactory
{

    public static IHitTestStrategy GetStrategy(HitTestConstants hitTestConstant)
    {
        return hitTestConstant switch
        {
            HitTestConstants.HTTOPLEFT => new TopLeftStrategy(),
            HitTestConstants.HTTOP => new TopStrategy(),
            HitTestConstants.HTTOPRIGHT => new TopRightStrategy(),
            HitTestConstants.HTLEFT => new LeftStrategy(),
            HitTestConstants.HTRIGHT => new RightStrategy(),
            HitTestConstants.HTBOTTOMLEFT => new BottomLeftStrategy(),
            HitTestConstants.HTBOTTOM => new BottomStrategy(),
            HitTestConstants.HTBOTTOMRIGHT => new BottomRightStrategy(),
            _ => new DefaultStrategy()
        };
    }

}
