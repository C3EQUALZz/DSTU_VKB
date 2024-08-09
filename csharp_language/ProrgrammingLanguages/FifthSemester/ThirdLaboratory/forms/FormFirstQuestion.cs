using System;
using System.Windows.Forms;
using ThirdLaboratory.controllers;

namespace ThirdLaboratory.forms
{
    public partial class FormFirstQuestion : Form
    {
        private FirstQuestionController<double> _controller;

        private int? lengthOfArray = null;
        private int? startIndex = null;
        private int? endIndex = null;

        public FormFirstQuestion()
        {
            InitializeComponent();
        }

        private void LengthOfArrayInput__TextChanged(object sender, EventArgs e)
        {

            if (lengthOfArrayInput.Texts == "")
                return;

            try
            {
                var buffer = int.Parse(lengthOfArrayInput.Texts);

                if (buffer == 0 || buffer < endIndex || buffer < startIndex)
                {
                    MessageBox.Show($"Длина массива (N = {lengthOfArray}) не может быть меньше, чем стартовый срез (K = {startIndex}) и конечный срез (L = {endIndex})");
                }
                lengthOfArray = buffer;
            }

            catch
            {
                MessageBox.Show($"Вы ввели не целое число");
            }
            
        }

        private void StartSliceOfArrayInput__TextChanged(object sender, EventArgs e)
        {
            if (startSliceOfArrayInput.Texts == "")
                return;

            try
            {
                var buffer = int.Parse(startSliceOfArrayInput.Texts);

                if (buffer == 0 || buffer > endIndex || buffer > lengthOfArray)
                {
                    MessageBox.Show($"Стартовый индекс не может равняться нулю, быть больше конечного индекса или больше длины массивы ");
                }

                startIndex = buffer;
            } 
            
            catch
            {
                MessageBox.Show($"Вы ввели не целое число");
            }
            
        }

        private void EndSliceOfArrayInput__TextChanged(object sender, EventArgs e)
        {
            if (endSliceOfArrayInput.Texts == "")
                return;

            try
            {
                var buffer = int.Parse(endSliceOfArrayInput.Texts);

                if (buffer == 0 || buffer < startIndex || buffer > lengthOfArray)
                {
                    MessageBox.Show($"Конечный индекс не может равняться нулю или быть меньше, чем стартовый индекс, а также не может быть больше длины массива");
                }
                endIndex = buffer;
            }

            catch
            {
                MessageBox.Show($"Вы ввели не целое число");
            }
            
        }

        private void ClearButton_Click(object sender, EventArgs e)
        {
            lengthOfArrayInput.Clear();
            startSliceOfArrayInput.Clear();
            endSliceOfArrayInput.Clear();
            resultLabel.Text = string.Empty;
        }

        private void ExecuteButton_Click(object sender, EventArgs e)
        {

            if (lengthOfArray == null || startIndex == null || endIndex == null)
            {
                return; 
            }

            try
            {
                double[] array = new double[(int) lengthOfArray];

                Random rand = new Random();
                for (int i = 0; i < array.Length; i++)
                    array[i] = Math.Round(rand.NextDouble(), 2);

                arrayOfRandomNumbersLabel.Text = "[" + string.Join(", ", array) + "]"; ;

                _controller = new FirstQuestionController<double>(array, (int) startIndex, (int) endIndex);

                var result = _controller.CalculateSum();

                resultLabel.Text = $"Результат: {result}";
                Console.WriteLine(result);
            }

            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка: {ex.Message}");
            }
        }
    }
}
