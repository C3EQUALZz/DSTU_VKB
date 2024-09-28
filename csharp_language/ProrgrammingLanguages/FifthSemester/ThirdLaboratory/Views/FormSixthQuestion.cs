using System;
using System.Windows.Forms;
using ThirdLaboratory.Core.Interfaces.SixthQuestion;
using ThirdLaboratory.Models;
using ThirdLaboratory.Presenters;

namespace ThirdLaboratory.forms
{
    public partial class FormSixthQuestion : Form, ISixthQuestionView
    {
        private readonly ISixthQuestionPresenter _presenter;

        public FormSixthQuestion()
        {
            InitializeComponent();
            _presenter = new SixthQuestionPresenter(this, new SixthQuestionModel());
        }

        public string StudentsTextBox
        {
            get { return studentsTextBox.Texts; }
            set { studentsTextBox.Texts = value; }
        }

        public string ScholarShipTextBox
        {
            get { return scholarShipTextBox.Texts; }
            set {  scholarShipTextBox.Texts = value; }
        }

        public string ScholarShipRangeTextBox
        {
           get { return scholarShipRangeTextBox.Texts; }
           set { scholarShipRangeTextBox.Texts = value; }
        }

        public string ResultLabel
        {
            get { return resultLabel.Text; }
            set { resultLabel.Text = value; }
        }


        public void StudentsTextBox__TextChanged(object sender, System.ComponentModel.CancelEventArgs e)
        {
            _presenter.OnStudentsTextBoxTextChanged(sender, e);    
        }

        public void ScholarShipTextBox__TextChanged(object sender, System.ComponentModel.CancelEventArgs e)
        {
            _presenter.OnScholarShipTextBoxTextChanged(sender, e);
        }

        public void ScholarShipRangeTextBox__TextChanged(object sender, System.ComponentModel.CancelEventArgs e)
        {
            _presenter.OnScholarShipRangeTextBoxTextChanged(sender, e);
        }

        public void ClearButton_Click(object sender, EventArgs e)
        {
            studentsTextBox.Clear();
            scholarShipRangeTextBox.Clear();
            scholarShipTextBox.Clear();
        }

        public void ExecuteButton_Click(object sender, EventArgs e)
        {
            _presenter.OnExecute(sender, e);
        }

    }
}
