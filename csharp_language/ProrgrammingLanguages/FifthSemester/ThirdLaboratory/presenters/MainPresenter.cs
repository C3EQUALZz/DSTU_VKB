using System;
using ThirdLaboratory.core.interfaces;
using System.Windows.Forms;

namespace ThirdLaboratory.presenters
{
    /// <summary>
    /// Презентер для главного окна, реализован паттерн MVP
    /// </summary>
    internal class MainPresenter : IMainPresenter
    {
        private readonly IMainView _view;
        private readonly IFormFactory _formFactory;
        private readonly ICommandContext _commandContext;
        private readonly ISideBarContext _sideBarContext;

        public MainPresenter(
            IMainView view,
            IFormFactory formFactory,
            ICommandContext commandContext,
            ISideBarContext sideBarContext
            )
        {
            _view = view;
            _formFactory = formFactory;
            _commandContext = commandContext;
            _sideBarContext = sideBarContext;
        }

        /// <summary>
        /// Обработчик нажатия на кнопку раскрытия меню.
        /// Здесь запускается анимация именно раскрытия меню. 
        /// </summary>
        public void OnMenuButtonClick(object sender, EventArgs e)
        {
            _sideBarContext.StartAnimation();
        }

        /// <summary>
        /// При раскрытии каждого блока (1 - 5 задание и т.п) у вас есть кнопки с выбором задания. 
        /// Так вот, это обработчик нажатия на эту кнопку, который в зависимости от имени тэга в кнопке создает форму
        /// </summary>
        public void OnQuestionButtonClick(object sender, EventArgs e)
        {
            if (sender is Button button && button.Tag is string formName)
            {
                var formInstance = _view.GetOpenFormByName(formName);
                if (formInstance == null)
                {
                    formInstance = _formFactory.Create(formName);
                    _view.ShowForm(formInstance);
                }
                else
                {
                    _view.ActivateForm(formInstance);
                }
            }
        }

        /// <summary>
        /// Обработчик для таймера, который отвечает за запуск анимации панелей - кнопок (1 - 5 задание и т.п.)
        /// </summary>
        public void OnTimerTick(object sender, EventArgs e)
        {
            _commandContext.Execute();
        }

        /// <summary>
        /// Обработчик для таймера, который отвечает за смену состояния слайдера. 
        /// Начинается таймер -> меняется состояние слайдера. Здесь реализован паттерн "Состояние" у бокового меню. 
        /// </summary>
        public void OnTimerTransitionTick(object sender, EventArgs e)
        {
            _sideBarContext.Handle();
        }

        /// <summary>
        /// Обработчик события нажатия на любую из кнопок - панелей. 
        /// Здесь устанавливаются состояния (раскрыта или свернуто) для какой-то из кнопок.
        /// Обратите внимание, что тут используется рефликсия для поиска кнопки исходя из тэга кнопки. 
        /// У меня метод предназначен для 5 кнопок - панелей, а должен их как-то различать. 
        /// </summary>
        public void OnButtonClick(object sender, EventArgs e)
        {
            var button = sender as Button;
            var panelTag = button.Tag.ToString();
            _commandContext.SetCommand(panelTag);
        }
    }
}
