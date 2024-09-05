using System;
using System.Windows.Forms;
using LiveCharts.WinForms;
using LiveCharts;
using System.Collections.Generic;
using DoAnPaint.Graphs.Core.Interfaces;
using DoAnPaint.Graphs.Models.SecondQuestion;
using DoAnPaint.Graphs.Presenters;

namespace DoAnPaint.Graphs.Views
{
    public partial class FormSecondQuestion : Form, IView
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

        public FormSecondQuestion()
        {
            _models = new List<IModel> { new FirstModel(), new SecondModel(), new ThirdModel() };
            _presenter = new BasePresenter(this, _models);
            InitializeComponent();
        }

        /// <summary>
        /// Обработчик событий на вписывание значений в textBox, где написано "(ось Ox) А (от) ="
        /// </summary>
        public void GraphStartTextBox_Validating(object sender, System.ComponentModel.CancelEventArgs e)
        {
            ValidateGraphInput(graphStartTextBox, value => Start = value, "Введите корректное значение для начала графика.");
        }

        /// <summary>
        /// Обработчик событий на вписывание значений в textBox, где написано "(ось Ox) B (до) ="
        /// </summary>
        public void GraphEndTextBox_Validating(object sender, System.ComponentModel.CancelEventArgs e)
        {
            ValidateGraphInput(graphEndTextBox, value => End = value, "Введите корректное значение для конца графика.");
        }

        /// <summary>
        /// Обработчик событий на вписывание значений в textBox, где написано "h (шаг) = "
        /// </summary>
        public void GraphStepTextBox_Validating(object sender, System.ComponentModel.CancelEventArgs e)
        {
            ValidateGraphInput(graphStepTextBox, value => Step = value, "Введите корректное значение для шага графика.");
        }

        /// <summary>
        /// Обработчик событий на выбор у 1 comboBox
        /// </summary>
        public void FirstChartCheckBox_CheckedChanged(object sender, EventArgs e)
        {
            ChartCheckBox_CheckedChanged(firstChartCheckBox, 0);
        }

        /// <summary>
        /// Обработчик событий на выбор у 2 comboBox
        /// </summary>
        public void SecondChartCheckBox_CheckedChanged(object sender, EventArgs e)
        {
            ChartCheckBox_CheckedChanged(secondChartCheckBox, 1);
        }

        /// <summary>
        /// Обработчик событий на выбор у 3 comboBox
        /// Честно говоря, понимаю, что тут можно было пойти через рефлексию и вписывание функции в тегах, но у меня времени нет, чтобы это писать. 
        /// Изляшняя масштабируемость - тоже плохо, когда мало времени. 
        /// </summary>
        public void ThirdChartCheckBox_CheckedChanged(object sender, EventArgs e)
        {
            ChartCheckBox_CheckedChanged(thirdChartCheckBox, 2);
        }

        /// <summary>
        /// Вспомогательный метод, который фиксиурет изменения в ComboBox и добавляет в Presenter необходимые функции для отображения и построения
        /// </summary>
        /// <param name="checkBox">checkBox, где пользователь выбрал галочку</param>
        /// <param name="modelIndex">Индекс, под которым находится нужный график</param>
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

        /// <summary>
        /// Валидация ввода от пользователя
        /// </summary>
        /// <param name="textBox">textBox, в котором пользователь ввел значение</param>
        /// <param name="setValueAction">что происходит, когда пользователь ввел значение, здесь я сделал лямба выражение такое</param>
        /// <param name="errorMessage">ошибка, которая выводится в MessageBox</param>
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
