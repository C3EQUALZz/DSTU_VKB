using System.Windows.Forms;
using ThirdLaboratory.core.abstractClasses;

namespace ThirdLaboratory.core
{
    /// <summary>
    /// Паттерн команда. 
    /// Класс, который описывает команду раскрытия бокового меню. 
    /// </summary>
    internal class ExpandCommand : Command
    {
        public ExpandCommand(Panel panel, Timer timer) : base(panel, timer, 10, 400) { }

        /// <summary>
        /// Запуск определенного метода для работы. 
        /// </summary>
        public override void Execute()
        {
            panel.Height += step;
            if (panel.Height >= targetHeight)
            {
                timer.Stop();
            }
        }
    }
}
