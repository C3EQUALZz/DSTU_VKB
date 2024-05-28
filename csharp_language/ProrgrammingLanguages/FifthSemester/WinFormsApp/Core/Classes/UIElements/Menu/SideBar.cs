using FluentTransitions.Methods;
using FluentTransitions;
using WinFormsApp.Core.Interfaces.UIElements;

namespace WinFormsApp.Core.Classes.UIElements.Menu;

public class SideBar(Panel MenuPanel, Label LabelMenu, Button MenuButton)
{
    private const int AnimationDuration = 100;
    private IMenuState currentState = new ExpandedMenuState();


    public void UpdateMenu(bool isCollapsed)
    {
        var transition = new Transition(new Linear(TimeSpan.FromMilliseconds(AnimationDuration)));

        currentState = isCollapsed ? new CollapsedMenuState() : new ExpandedMenuState();
        
        transition.Add(MenuPanel, "Width", currentState.GetMenuWidth());
        transition.TransitionCompleted += (o, e) =>
        {
            currentState.UpdateButtonText(MenuPanel);
            currentState.UpdateMenuProperties(LabelMenu, MenuButton);
        };
        transition.Run();
    }
}
