using System;
using System.Windows.Forms;

namespace ThirdLaboratory.forms
{
    public partial class FormNinthQuestion : Form
    {

        private int? countOfRows;
        private int? countOfColumns;

        public FormNinthQuestion()
        {
            InitializeComponent();

            // Костыль для установки двойной буферизации для панелей сверху, так как окрашиваются в черный
            // Не удалять, а то будет черное сзади, как артефакты. 
            // Через drag and drop не нашел для них свойства DoubleBuffered, поэтому такая затея. 
            // https://www.cyberforum.ru/windows-forms/thread1657275.html
            Panel[] array = { panelForButtonCreateMatrix, panelWithInputLineForN, panelWithInputLineForM };

            foreach (var panel in array)
            {
                typeof(Control).GetProperty("DoubleBuffered", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.SetProperty).SetValue(panel, true, null);
            }
        }

        private void CountOfMatrixRowsTextBox__TextChanged(object sender, EventArgs e)
        {
            HandleTextChanged(countOfMatrixRowsTextBox.Texts, ref countOfRows);
        }

        private void CountOfMatrixColumnsTextBox__TextChanged(object sender, EventArgs e)
        {
            HandleTextChanged(countOfMatrixColumnsTextBox.Texts, ref countOfColumns);
        }

        private void CreateMatrixButton_Click(object sender, EventArgs e)
        {
            if (!(countOfColumns.HasValue && countOfRows.HasValue))
                return;

            dataGridView.RowCount = countOfRows.Value;
            dataGridView.ColumnCount = countOfColumns.Value;

            for (int i = 0; i < countOfRows.Value; i++)
            {
                dataGridView.Rows[i].HeaderCell.Value = Convert.ToString(i + 1);
            }

            for (int j = 0; j < countOfColumns.Value; j++)
            {
                dataGridView.Columns[j].HeaderCell.Value = Convert.ToString(j + 1);
            }

        }

        private void ExecuteButton_Click(object sender, EventArgs e)
        {

        }

        /// <summary>
        /// Общий обработчик событий для полей, когда текст изменился. 
        /// Здесь пару "костылей", чтобы не ломался при пустом тексте
        /// </summary>
        /// <param name="text">текст, взятый с textbox </param>
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
    }
}
