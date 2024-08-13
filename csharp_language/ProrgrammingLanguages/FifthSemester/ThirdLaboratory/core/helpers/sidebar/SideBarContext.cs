using System.Windows.Forms;
using ThirdLaboratory.core.interfaces;
using ThirdLaboratory.core.helpers.sidebar;

namespace ThirdLaboratory.core.helpers
{
    internal class SideBarContext
    {
        private ISideBarState _currentState;
        public Panel SideBar { get; set; }
        public Timer Timer { get; set; }
        public Panel TaskFlowPanel1To5 { get; set; }
        public Panel TaskFlowPanel6To10 { get; set; }
        public Panel TaskFlowPanel11To15 { get; set; }
        public Panel TaskFlowPanel16To20 { get; set; }

        public ISideBarState State
        {
            get => _currentState;
            set => _currentState = value;
        }

        public SideBarContext(Panel sideBar, Timer timer, Panel taskFlowPanel1To5, Panel taskFlowPanel6To10, Panel taskFlowPanel11To15, Panel taskFlowPanel16To20)
        {
            SideBar = sideBar;
            Timer = timer;
            TaskFlowPanel1To5 = taskFlowPanel1To5;
            TaskFlowPanel6To10 = taskFlowPanel6To10;
            TaskFlowPanel11To15 = taskFlowPanel11To15;
            TaskFlowPanel16To20 = taskFlowPanel16To20;

            _currentState = new ExpandedState();
        }

        public void Handle()
        {
            _currentState.Handle(this);
        }

        public void StartAnimation()
        {
            Timer.Start();
            Handle();
        }
    }
}
