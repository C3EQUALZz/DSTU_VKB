using System.Windows.Forms;
using ThirdLaboratory.core.abstractClasses;

namespace ThirdLaboratory.core.helpers
{
    /// <summary>
    /// Здесь реализован паттерн стратегия, который устанавливает состояния для определенной панели. 
    /// </summary>
    internal class CommandContext
    {
        private readonly Form mainForm;
        private Command _currentCommand;
        private readonly ComponentFinder _finder;

        /// <summary>
        /// Здесь передаю ссылку на главную форму, чтобы можно было искать элементы. 
        /// Так сказать, Dependency injection
        /// </summary>
        /// <param name="form">главная форма, на которой нужно искать кнопки с определенными тегами. </param>
        public CommandContext(Form form) {
            mainForm = form;
            _finder = new ComponentFinder(mainForm);
        }

        /// <summary>
        /// Сеттер для команды, здесь передается тег кнопки, которой нажали. 
        /// С помощью этого будет определяться привязанная панель и таймер. 
        /// </summary>
        /// <param name="panelTag">тэг кнопки для создания команды</param>
        public void SetCommand(string panelTag)
        {
            var panel = _finder.FindPanelByTag(panelTag);
            var timer = _finder.FindTimerByTag(panelTag);

            _currentCommand = CommandFactory.CreateCommand(panel, timer);

            timer.Start();
        }

        /// <summary>
        /// Точка запуска у стратегии
        /// </summary>
        public void Execute()
        {
            _currentCommand?.Execute();
        }

    }
}
