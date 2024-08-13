using System.Windows.Forms;

namespace ThirdLaboratory.core.abstractClasses
{
    internal abstract class Command
    {
        protected Panel panel;
        protected Timer timer;

        protected int step;
        protected int targetHeight;

        public Command(Panel panel, Timer timer, int step, int targetHeight)
        {
            this.panel = panel;
            this.timer = timer;
            this.step = step;
            this.targetHeight = targetHeight;
        }

        public abstract void Execute();
    }

}
