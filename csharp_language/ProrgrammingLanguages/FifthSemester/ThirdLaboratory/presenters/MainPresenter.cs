using System;
using ThirdLaboratory.core.helpers;
using ThirdLaboratory.core.interfaces;
using System.Windows.Forms;

namespace ThirdLaboratory.presenters
{
    /// <summary>
    /// Презентер для главного окна, реализован паттерн MVP
    /// </summary>
    internal class MainPresenter
    {
        private readonly IMainView _view;
        private readonly IFormFactory _formFactory;
        private readonly CommandContext _commandContext;
        private readonly SideBarContext _sideBarContext;

        public MainPresenter(
            IMainView view,
            IFormFactory formFactory,
            CommandContext commandContext,
            SideBarContext sideBarContext
            )
        {
            _view = view;
            _formFactory = formFactory;
            _commandContext = commandContext;
            _sideBarContext = sideBarContext;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        public void OnMenuButtonClick(object sender, EventArgs e)
        {
            _sideBarContext.StartAnimation();
        }

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

        public void OnTimerTick(object sender, EventArgs e)
        {
            _commandContext.Execute();
        }

        public void OnTimerTransitionTick(object sender, EventArgs e)
        {
            _sideBarContext.Handle();
        }

        public void OnButtonClick(object sender, EventArgs e)
        {
            var button = sender as Button;
            var panelTag = button.Tag.ToString();
            _commandContext.SetCommand(panelTag);
        }
    }
}
