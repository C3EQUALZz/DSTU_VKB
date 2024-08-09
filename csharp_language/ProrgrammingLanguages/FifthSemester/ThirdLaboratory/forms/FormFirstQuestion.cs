using System;
using System.Windows.Forms;
using ThirdLaboratory.controllers;

namespace ThirdLaboratory.forms
{
    /// <summary>
    /// View для 1 задания
    /// </summary>
    public partial class FormFirstQuestion : Form
    {
        private readonly FirstQuestionController<double> _controller;
        private int? lengthOfArray = null;
        private int? startIndex = null;
        private int? endIndex = null;

        public FormFirstQuestion()
        {
            InitializeComponent();
            _controller = new FirstQuestionController<double>();
        }
      
        private void LengthOfArrayInput__TextChanged(object sender, EventArgs e)
        {
            HandleTextChanged(lengthOfArrayInput.Texts, ref lengthOfArray);
        }

        private void StartSliceOfArrayInput__TextChanged(object sender, EventArgs e)
        {
            HandleTextChanged(startSliceOfArrayInput.Texts, ref startIndex);
        }

        private void EndSliceOfArrayInput__TextChanged(object sender, EventArgs e)
        {
            HandleTextChanged(endSliceOfArrayInput.Texts, ref endIndex);
        }

        /// <summary>
        /// Общий обработчик событий для полей, когда текст изменился. 
        /// Здесь пару "костылей", чтобы не ломался при пустом тексте
        /// </summary>
        /// <param name="text">текст, взятый с inline </param>
        /// <param name="value">ссылка на значение, чтобы сохранить значение</param>
        private void HandleTextChanged(string text, ref int? value)
        {
            if (string.IsNullOrEmpty(text))
                return;

            if (int.TryParse(text, out var buffer))
            {
                value = buffer;
            }
            else
            {
                MessageBox.Show("Вы ввели не целое число");
            }
        }

        private void ClearButton_Click(object sender, EventArgs e)
        {
            lengthOfArrayInput.Clear();
            startSliceOfArrayInput.Clear();
            endSliceOfArrayInput.Clear();
            resultLabel.Text = string.Empty;
            arrayOfRandomNumbersLabel.Text = string.Empty;
        }

        private void ExecuteButton_Click(object sender, EventArgs e)
        {
            if (lengthOfArray == null || startIndex == null || endIndex == null)
            {
                MessageBox.Show("Все поля должны быть заполнены");
                return;
            }

            var errorMessage = _controller.ValidateInputs(lengthOfArray, startIndex, endIndex);

            if (errorMessage != null)
            {
                MessageBox.Show(errorMessage);
                return;
            }

            var array = _controller.CreateArray((int)lengthOfArray);
            _controller.InitializeModel(array, (int)startIndex, (int)endIndex);
            arrayOfRandomNumbersLabel.Text = $"[{string.Join(",", array)}]";
            resultLabel.Text = $"Результат: {_controller.CalculateSum()}";

        }
    }
}
