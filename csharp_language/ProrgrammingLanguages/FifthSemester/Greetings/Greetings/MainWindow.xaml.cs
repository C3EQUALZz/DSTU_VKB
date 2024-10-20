using Greetings.Core.Interfaces;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows;

namespace Greetings
{
    /// <summary>
    /// Логика взаимодействия для MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window, IMainWindow
    {
        private readonly IMainWindowPresenter _presenter;
        public MainWindow()
        {
            InitializeComponent();
            _presenter = new Presenter(this);
        }

        public void Button_Click(object sender, RoutedEventArgs e)
        {
            if (RadioButton1.IsChecked.Value)
            {
                _presenter.OnButtonClick(RadioButton1);
            }
            else if (RadioButton2.IsChecked.Value)
            {
                _presenter.OnButtonClick(RadioButton2);
            }

        }
    }
}
