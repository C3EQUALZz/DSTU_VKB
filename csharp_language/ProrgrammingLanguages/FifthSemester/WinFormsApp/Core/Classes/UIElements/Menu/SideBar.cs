using FluentTransitions.Methods;
using FluentTransitions;
using WinFormsApp.Core.Interfaces.UIElements;

namespace WinFormsApp.Core.Classes.UIElements.Menu;

/// <summary>
/// Класс SideBar представляет боковую панель меню, которая может быть свернута или развернута.
/// </summary>
public class SideBar(Panel MenuPanel, Label LabelMenu, Button MenuButton)
{
    private const int AnimationDuration = 300;
    private IMenuState currentState = new ExpandedMenuState();

    /// <summary>
    /// Устанавливает новое состояние меню и обновляет его в соответствии с этим состоянием.
    /// Нужен для реализации контекста в паттерне стратегия. 
    /// </summary>
    /// <param name="NewState">Новое состояние меню.</param>
    public void SetMenuState(IMenuState NewState)
    {
        currentState = NewState;

        if (currentState is CollapsedMenuState)
        {
            currentState.UpdateButtonText(MenuPanel);
        }

        var transition = new Transition(new Linear(TimeSpan.FromMilliseconds(AnimationDuration)));
        transition.Add(MenuPanel, "Width", currentState.GetMenuWidth());
        transition.TransitionCompleted += (o, e) =>
        {
            currentState.UpdateMenuProperties(LabelMenu, MenuButton);

            if (currentState is ExpandedMenuState)
            {
                currentState.UpdateButtonText(MenuPanel);
            }
        };
        transition.Run();
    }
}
