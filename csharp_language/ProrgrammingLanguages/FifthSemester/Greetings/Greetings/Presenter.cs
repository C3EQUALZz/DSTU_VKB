using Greetings.Core.Interfaces;
using System.Windows;
using System.Windows.Controls;

namespace Greetings
{
    internal class Presenter : IMainWindowPresenter
    {
        private readonly IMainWindow _view;

        public Presenter(IMainWindow view)
        {
            _view = view;
        }

        public void OnButtonClick(RadioButton button)
        {
            button.IsChecked = false;
            MessageBox.Show(button.Content.ToString());
        }
    }
}
