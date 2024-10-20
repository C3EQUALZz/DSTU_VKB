using ThirdLaboratory.core.interfaces;

namespace ThirdLaboratory.core.helpers.sidebar
{
    internal class ExpandedState : ISideBarState
    {
        public void Handle(SideBarContext context)
        {
            context.SideBar.Width -= 10;

            if (context.SideBar.Width <= 90)
            {
                context.State = new CollapsedState();
                context.Timer.Stop();
            }
        }
    }
}
