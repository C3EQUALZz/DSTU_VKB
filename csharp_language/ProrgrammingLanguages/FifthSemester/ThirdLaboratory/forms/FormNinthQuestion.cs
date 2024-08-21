using System;
using System.Linq;
using System.Windows.Forms;
using ThirdLaboratory.core.interfaces;
using ThirdLaboratory.models;
using ThirdLaboratory.presenters;
using ThirdLaboratory.core.helpers.questions;

namespace ThirdLaboratory.forms
{
    public partial class FormNinthQuestion : Form, INinthQuestionView
    {

        private int? countOfRows;
        private int? countOfColumns;
        private readonly NinthQuestionPresenter _presenter;

        public FormNinthQuestion()
        {
            InitializeComponent();

            _presenter = new NinthQuestionPresenter(this, new NinthQuestionModel());

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

        /// <summary>
        /// Свойство, которое позволяет получить количество строк в матрице или установить
        /// </summary>
        public int RowCount
        {
            get => dataGridView.RowCount;
            set => dataGridView.RowCount = value;
        }

        /// <summary>
        /// Свойство, которое позволяет получить количество столбцов в матрице или установить
        /// </summary>
        public int ColumnCount
        {
            get => dataGridView.ColumnCount;
            set => dataGridView.ColumnCount = value;
        }

        /// <summary>
        /// Свойство, которое позволяет получить все значения из dataGridView в виде матрицы int[rows, columns]
        /// Можно также установить значения в матрицы, подменив
        /// </summary>
        public int[,] Matrix
        {
            get
            {
                var matrix = new int[RowCount, ColumnCount];
                Enumerable.Range(0, RowCount).ToList().ForEach(i =>
                    Enumerable.Range(0, ColumnCount).ToList().ForEach(j =>
                    {
                        if (int.TryParse(dataGridView[j, i].Value?.ToString(), out int value))
                        {
                            matrix[i, j] = value;
                        }
                    })
                );
                return matrix;
            }
            set
            {
                Enumerable.Range(0, RowCount).ToList().ForEach(i =>
                    Enumerable.Range(0, ColumnCount).ToList().ForEach(j =>
                    {
                        dataGridView[j, i].Value = value[i, j];
                    })
                );
            }
        }

        /// <summary>
        /// Свойство для установки или получения значения хедеров - строк.
        /// Я использую, чтобы можно было установить значения, подписав все. 
        /// </summary>
        public string[] RowHeaders
        {
            get
            {
                var headers = new string[RowCount];
                for (int i = 0; i < RowCount; i++)
                {
                    headers[i] = dataGridView.Rows[i].HeaderCell.Value?.ToString();
                }
                return headers;
            }
            set
            {
                for (int i = 0; i < RowCount; i++)
                {
                    dataGridView.Rows[i].HeaderCell.Value = value[i];
                }
            }
        }

        /// <summary>
        /// Свойство для установки или получения значения хедеров - столбцов.
        /// Я использую, чтобы можно было установить значения, подписав все. 
        /// </summary>
        public string[] ColumnHeaders
        {
            get
            {
                var headers = new string[ColumnCount];
                for (int j = 0; j < ColumnCount; j++)
                {
                    headers[j] = dataGridView.Columns[j].HeaderCell.Value?.ToString();
                }
                return headers;
            }
            set
            {
                for (int j = 0; j < ColumnCount; j++)
                {
                    dataGridView.Columns[j].HeaderCell.Value = value[j];
                }
            }
        }

        /// <summary>
        /// Обработчик событий на изменение ввода для количества строк матрицы. Проверяет правильное ли там число. 
        /// </summary>
        public void CountOfMatrixRowsTextBox__TextChanged(object sender, EventArgs e)
        {
            Handlers.HandleTextChanged(countOfMatrixRowsTextBox.Texts, ref countOfRows);

            if (countOfRows < 0)
            {
                MessageBox.Show("Вы ввели отрицательное число - количество строк, это неправильно. ");
            }
        }

        /// <summary>
        /// Обработчик событий на изменение ввода для количества столбцов матрицы. Проверяет правильное ли там число. 
        /// </summary>
        public void CountOfMatrixColumnsTextBox__TextChanged(object sender, EventArgs e)
        {
            Handlers.HandleTextChanged(countOfMatrixColumnsTextBox.Texts, ref countOfColumns);

            if (countOfColumns < 0)
            {
                MessageBox.Show("Вы ввели отрицательное число - количество столбцов, это неправильно. ");
            }
        }

        /// <summary>
        /// Обработчик нажатия на кнопку, когда хотят создать матрицу
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        public void CreateMatrixButton_Click(object sender, EventArgs e)
        {
            if (!(countOfColumns.HasValue && countOfRows.HasValue))
                return;

            _presenter.OnCreateMatrix(countOfRows.Value, countOfColumns.Value);

        }

        /// <summary>
        /// Обработчик события, который определяет запуск задания
        /// </summary>
        private void ExecuteButton_Click(object sender, EventArgs e)
        {
            _presenter.OnExecute();

        }

    }
}
