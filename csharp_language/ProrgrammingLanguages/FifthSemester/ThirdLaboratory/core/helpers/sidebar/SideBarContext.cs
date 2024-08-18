using System.Windows.Forms;
using ThirdLaboratory.core.interfaces;
using ThirdLaboratory.core.helpers.sidebar;
using System.Linq;
using System;
using System.Reflection;

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

        /// <summary>
        /// Паттерн состояние. Здесь не совсем грамотно реализовано, надо было сделать интерфейс, от которого идет поиск
        /// Но у меня выходило как-то криво, потому что есть явные привязки к полям, поэтому решил через рефлексию. 
        /// </summary>
        /// <param name="form">главная форма, на которой есть нужные панели</param>
        /// <exception cref="Exception"></exception>
        public SideBarContext(Form form) {
            SideBar = form.Controls.Find("sideBar", true).FirstOrDefault() as Panel;
            TaskFlowPanel1To5 = form.Controls.Find("taskFlowPanel1To5", true).FirstOrDefault() as Panel;
            TaskFlowPanel6To10 = form.Controls.Find("taskFlowPanel6To10", true).FirstOrDefault() as Panel;
            TaskFlowPanel11To15 = form.Controls.Find("taskFlowPanel11To15", true).FirstOrDefault() as Panel;
            TaskFlowPanel16To20 = form.Controls.Find("taskFlowPanel16To20", true).FirstOrDefault() as Panel;

            var timerField = form.GetType().GetField("sideBarTransition", BindingFlags.NonPublic | BindingFlags.Instance);
            if (timerField != null)
            {
                Timer = timerField.GetValue(form) as Timer;
            }

            if (SideBar == null || Timer == null || TaskFlowPanel1To5 == null || TaskFlowPanel6To10 == null || TaskFlowPanel11To15 == null || TaskFlowPanel16To20 == null)
            {
                throw new Exception("Не все компоненты боковой панели были найдены. Проверьте, что все необходимые контролы и таймеры присутствуют на форме.");
            }

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
