using System;
using System.Text.RegularExpressions;
using System.Windows;
using ThirdLaboratory.Core.Interfaces.SixthQuestion;

namespace ThirdLaboratory.Presenters
{
    internal class SixthQuestionPresenter : ISixthQuestionPresenter
    {
        private readonly ISixthQuestionView _view;
        private readonly ISixthQuestionModel _model;

        public SixthQuestionPresenter(ISixthQuestionView view, ISixthQuestionModel model)
        {
            _view = view;
            _model = model;
        }

        public void OnStudentsTextBoxTextChanged(object sender, EventArgs e)
        {
            var students = _view.StudentsTextBox;
            var regex = new Regex(@"^[a-zA-Z]+(,[a-zA-Z]+)*$");

            if (!regex.IsMatch(students))
            {
                MessageBox.Show("Введите студентов через запятые");
                _view.StudentsTextBox = "";
            }

        }

        public void OnScholarShipTextBoxTextChanged(object sender, EventArgs e)
        {
            var sсholarShips = _view.ScholarShipTextBox;
            var regex = new Regex(@"^\d+(,\d+)*$");

            if (!regex.IsMatch(sсholarShips))
            {
                MessageBox.Show("Введите числа через запятую");
                _view.ScholarShipTextBox = "";
            }

        }

        public void OnScholarShipRangeTextBoxTextChanged(object sender, EventArgs e)
        {
            var rangeScholarShips = _view.ScholarShipRangeTextBox;
            var regex = new Regex(@"^\d+\-\d+$");

            if (!regex.IsMatch(rangeScholarShips))
            {
                MessageBox.Show("Введите два числа через тире");
                _view.ScholarShipRangeTextBox = "";
            }

        }

        public void OnExecute(object sender, EventArgs e)
        {

            if (string.IsNullOrEmpty(_view.ScholarShipRangeTextBox) || string.IsNullOrWhiteSpace(_view.ScholarShipRangeTextBox))
            {
                MessageBox.Show("Вы не заполнили поле с диапазаном стипендний");
                return;
            }

            if (string.IsNullOrEmpty(_view.ScholarShipTextBox) || string.IsNullOrWhiteSpace(_view.ScholarShipTextBox))
            {
                MessageBox.Show("Вы не заполнили поле со стипендиями");
                return;
            }

            if (string.IsNullOrEmpty(_view.StudentsTextBox) || string.IsNullOrWhiteSpace(_view.StudentsTextBox))
            {
                MessageBox.Show("Вы не заполнили поле со студентами");
                return;
            }


            _view.ResultLabel = _model.Execute(_view.ScholarShipTextBox, _view.ScholarShipRangeTextBox, _view.StudentsTextBox); 
        }

    }
}
