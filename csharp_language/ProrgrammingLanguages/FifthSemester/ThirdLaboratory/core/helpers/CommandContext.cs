using System.Windows.Forms;
using ThirdLaboratory.core.abstractClasses;

namespace ThirdLaboratory.core.helpers
{
    internal class CommandContext
    {
        private readonly Form mainForm;
        private Command _currentCommand;

        public CommandContext(Form form) {
            mainForm = form;
        }

        public void SetCommand(string panelTag)
        {
            var panel = ComponentFactory.FindPanelByTag(mainForm, panelTag);
            var timer = ComponentFactory.FindTimerByTag(mainForm, panelTag);

            _currentCommand = CommandFactory.CreateCommand(panel, timer);

            timer.Start();
        }

        public void Execute()
        {
            _currentCommand?.Execute();
        }

    }
}
