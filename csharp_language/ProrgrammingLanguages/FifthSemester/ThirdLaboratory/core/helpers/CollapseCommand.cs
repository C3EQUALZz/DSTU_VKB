using System.Windows.Forms;
using ThirdLaboratory.core.abstractClasses;

namespace ThirdLaboratory.core
{
    /// <summary>
    /// Класс, который реализует паттерн команду. В данном случае - это закрытие кнопок - контейнеров. 
    /// Данные кнопки там подписаны, как задание 1 - 5
    /// </summary>
    internal class CollapseCommand : Command
    {
        public CollapseCommand(Panel panel, Timer timer) : base(panel, timer, -10, 60) { }

        /// <summary>
        /// У нас работает до определенных размеров, после чего прекращается работа. 
        /// </summary>
        public override void Execute()
        {
            panel.Height += step;
            if (panel.Height <= targetHeight)
            {
                timer.Stop();
            }
        }
    }
}
