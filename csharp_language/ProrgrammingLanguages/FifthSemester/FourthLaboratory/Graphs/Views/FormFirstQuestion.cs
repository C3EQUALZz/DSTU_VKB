using DoAnPaint.Graphs.Core.Interfaces.FirstQuestion;
using DoAnPaint.Graphs.Models;
using DoAnPaint.Graphs.Models.FirstQuestion;
using DoAnPaint.Graphs.Presenters;
using LiveCharts;
using System;
using System.Collections.Generic;
using System.Windows.Forms;
using LiveCharts.WinForms;

namespace DoAnPaint.Graphs.Views
{
    public partial class FormFirstQuestion : Form, IView
    {
        private readonly IPresenter _presenter;
        private readonly List<IModel> _models;

        public double Step { get; set; }
        public double Start { get; set; }
        public double End { get; set; }
        public bool IsAnimationEnabled => animationCheckBox.Checked;
        public CartesianChart CartesianChart => cartesianChart;
        public SeriesCollection ChartData
        {
            get => cartesianChart.Series;
            set
            {
                cartesianChart.Series.Clear();
                foreach (var series in value)
                {
                    cartesianChart.Series.Add(series);
                }
            }
        }

        public FormFirstQuestion()
        {
            _models = new List<IModel> { new FirstModel(), new SecondModel(), new ThirdModel() };
            _presenter = new FirstQuestionPresenter(this, _models);
            InitializeComponent();
        }

        public void GraphStartTextBox_Validating(object sender, System.ComponentModel.CancelEventArgs e)
        {
            ValidateGraphInput(graphStartTextBox, value => Start = value, "Введите корректное значение для начала графика.");
        }

        public void GraphEndTextBox_Validating(object sender, System.ComponentModel.CancelEventArgs e)
        {
            ValidateGraphInput(graphEndTextBox, value => End = value, "Введите корректное значение для конца графика.");
        }

        public void GraphStepTextBox_Validating(object sender, System.ComponentModel.CancelEventArgs e)
        {
            ValidateGraphInput(graphStepTextBox, value => Step = value, "Введите корректное значение для шага графика.");
        }
        public void FirstChartCheckBox_CheckedChanged(object sender, EventArgs e)
        {
            ChartCheckBox_CheckedChanged(firstChartCheckBox, 0);
        }

        public void SecondChartCheckBox_CheckedChanged(object sender, EventArgs e)
        {
            ChartCheckBox_CheckedChanged(secondChartCheckBox, 1);
        }

        public void ThirdChartCheckBox_CheckedChanged(object sender, EventArgs e)
        {
            ChartCheckBox_CheckedChanged(thirdChartCheckBox, 2);
        }

        private void ChartCheckBox_CheckedChanged(CheckBox checkBox, int modelIndex)
        {
            if (checkBox.Checked)
            {
                _presenter.SelectModel(_models[modelIndex]);
            }
            else
            {
                _presenter.DeselectModel(_models[modelIndex]);
            }

            _presenter.Draw();
        }

        private void ValidateGraphInput(TextBox textBox, Action<double> setValueAction, string errorMessage)
        {
            if (double.TryParse(textBox.Text, out double value))
            {
                setValueAction(value);

                if (
                    !string.IsNullOrWhiteSpace(graphStartTextBox.Text) &&
                    !string.IsNullOrWhiteSpace(graphEndTextBox.Text) &&
                    !string.IsNullOrWhiteSpace(graphStepTextBox.Text)
                )

                {
                    _presenter.Draw();
                }
            }
            else
            {
                MessageBox.Show(errorMessage);
                textBox.Clear();
            }
        }


    }
}
