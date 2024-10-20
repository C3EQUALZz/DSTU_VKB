using System;
using System.Windows.Forms;
using ThirdLaboratory.core.interfaces;
using ThirdLaboratory.presenters;
using ThirdLaboratory.models;
using ThirdLaboratory.core.interfaces.secondQuestion;

namespace ThirdLaboratory.forms
{
    public partial class FormSecondQuestion : Form, ISecondQuestionView
    {
        private readonly ISecondQuestionPresenter _presenter;
        
        public FormSecondQuestion()
        {
            InitializeComponent();
            _presenter = new SecondQuestionPresenter(this, new SecondQuestionModel());
        }
        
        /// <summary>
        /// Свойство, которое позволяет обращаться и использовать staffInput (в Designer 1 строка, там фамилии сотрудников)
        /// </summary>
        public string StaffInput
        {
            get => staffInput.Texts;
            set => staffInput.Texts = value;
        }

        /// <summary>
        /// Свойство, которое позволяет обращаться и использовать requestInput (в Designer 2 строка, там мы вводим заявки)
        /// </summary>
        public string RequestsInput
        {
            get => requestsInput.Texts;
            set => requestsInput.Texts = value;
        }

        /// <summary>
        /// Свойство, которое позволяет обращаться и использоваться resultOutput (в Designer самое последнее поле с выводом, там написано "Результат")
        /// </summary>
        public string ResultOutput
        {
            get => resultLabel.Text;
            set => resultLabel.Text = value;
        }

        /// <summary>
        /// Обработчик событий, который установлен через Designer для обновления ввода сотрудников
        /// </summary>
        public void StaffInput__TextChanged(object sender, EventArgs e)
        {
            _presenter.Update(StaffInput, RequestsInput);
        }

        /// <summary>
        /// Обработчик событий, который установлен через Designer для обновления ввода заявок
        /// </summary>
        public void RequestsInput__TextChanged(object sender, EventArgs e)
        {
            _presenter.Update(StaffInput, RequestsInput);
        }

        /// <summary>
        /// Обработчик событий, который установлен через Designer на кнопку "Очистить"
        /// </summary>
        public void ClearButton_Click(object sender, EventArgs e)
        {
            staffInput.Clear();
            requestsInput.Clear();
            resultLabel.Text = "Результат";
        }

        /// <summary>
        /// Обработчик событий, который установлен через Designer на кнопку "Запустить"
        /// </summary>
        public void ExecuteButton_Click(object sender, EventArgs e)
        {
            _presenter.OnExecute();
        }
    }
}
