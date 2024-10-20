using ThirdLaboratory.core.abstractClasses;
using System.Windows.Forms;

namespace ThirdLaboratory.core.helpers
{
    /// <summary>
    /// Паттерн кривая простая фабрика ))))))). 
    /// Здесь грубо говоря, не совсем правильно реализовано, но я пытался инкапсулировать запрос на создание объекта правда....
    /// </summary>
    internal class CommandFactory
    {
        /// <summary>
        /// Метод, который создает команду закрытия и открытия панели (1 - 5 задание и т.п)
        /// </summary>
        /// <param name="panel">Панель, к которой привязываются данные команды</param>
        /// <param name="timer">Таймер, связанный с панелью для анимации. </param>
        /// <returns></returns>
        public static Command CreateCommand(Panel panel, Timer timer)
        {

            if (panel.Height >= 320)
            {
                return new CollapseCommand(panel, timer);
            }
            else
            {
                return new ExpandCommand(panel, timer); 
            }

        }

       
    }
}
