using System.Windows.Forms;

namespace ThirdLaboratory.core.abstractClasses
{
    /// <summary>
    /// Абстрактный класс, которы описывает команду. 
    /// Да-да, нужно сделать интерфейс было, но уже так решился, чтобы зря поля не писать и соблюдать принцип DRY
    /// </summary>
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
