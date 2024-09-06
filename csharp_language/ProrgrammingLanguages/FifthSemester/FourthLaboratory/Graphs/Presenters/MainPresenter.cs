using DoAnPaint.Graphs.Core.Interfaces;
using System;
using System.Windows.Forms;

namespace DoAnPaint.Graphs.Presenters
{
    internal class MainPresenter : IMainPresenter
    {
        private readonly IMainView _view;
        private readonly IFormFactory _formFactory;

        public MainPresenter(IMainView view, IFormFactory factory)
        {
            _view = view;
            _formFactory = factory;
        }

        public void OnButtonClick(object sender, EventArgs e)
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


    }
}
