using FluentTransitions;
using FluentTransitions.Methods;
using WinFormsApp.Core.Interfaces.UIElements;

namespace WinFormsApp.Core.Classes.UIElements.Menu;

/// <summary>
/// Класс SideBar представляет боковую панель меню, которая может быть свернута или развернута.
/// </summary>
public class SideBar(Panel MenuPanel, Label LabelMenu, Button MenuButton)
{
    private const int AnimationDuration = 800;
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

        var transition = new Transition(new EaseInEaseOut(TimeSpan.FromMilliseconds(AnimationDuration)));
        transition.Add(MenuPanel, "Width", currentState.GetMenuWidth());
        transition.TransitionCompleted += (o, e) =>
        {

            if (currentState is ExpandedMenuState)
            {
                currentState.UpdateButtonText(MenuPanel);
            }

            currentState.UpdateMenuProperties(LabelMenu, MenuButton);

        };
        transition.Run();
    }
}
