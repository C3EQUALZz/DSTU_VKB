using ThirdLaboratory.core.interfaces;

namespace ThirdLaboratory.core.helpers.sidebar
{
    internal class CollapsedState : ISideBarState
    {
        public void Handle(SideBarContext context)
        {
            context.SideBar.Width += 10;

            if (context.SideBar.Width >= 323)
            {
                context.SetState(new ExpandedState());
                context.Timer.Stop();

                context.TaskFlowPanel1To5.Width = context.SideBar.Width;
                context.TaskFlowPanel6To10.Width = context.SideBar.Width;
                context.TaskFlowPanel11To15.Width = context.SideBar.Width;
                context.TaskFlowPanel16To20.Width = context.SideBar.Width;
            }
        }
    }
}
