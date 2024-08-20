using System;
using System.Linq;
using System.Windows.Forms;
using ThirdLaboratory.core.helpers.questions;
using ThirdLaboratory.core.interfaces.nineteenthQuestion;
using ThirdLaboratory.models;
using ThirdLaboratory.presenters;

namespace ThirdLaboratory.forms
{
    public partial class FormNineteenthQuestion : Form, INineteenthQuestionView
    {
        private int? countOfRows;
        private int? countOfColumns;
        private int? deleteColumnNumber;
        private readonly INineteenthQuestionPresenter _presenter;

        public FormNineteenthQuestion()
        {
            InitializeComponent();
            _presenter = new NineteenthQuestionPresenter(
                this,
                new NineteenthQuestionModel()
            );
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
        /// Обработчик событий, установленный через Designer, на кнопку для создания матрицы
        /// </summary>
        public void CreateMatrixButton_Click(object sender, EventArgs e)
        {
            if (!(countOfColumns.HasValue && countOfRows.HasValue))
                return;

            _presenter.OnCreateMatrix(countOfRows.Value, countOfColumns.Value);
        }

        /// <summary>
        /// Обработчик событий, установленный через Designer, на поле с вводом количества строк
        /// </summary>
        private void CountOfRowsInput__TextChanged(object sender, EventArgs e)
        {
            Handlers.HandleTextChanged(countOfRowsInput.Texts, ref countOfRows);

            if (countOfRows < 0)
            {
                MessageBox.Show("Вы ввели отрицательное число - количество строк, это неправильно. ");
            }
        }

        /// <summary>
        /// Обработчик событий, установленный через Designer, на поле с вводом количества столбцов
        /// </summary>
        private void CountOfColumnsInput__TextChanged(object sender, EventArgs e)
        {
            Handlers.HandleTextChanged(countOfColumnsInput.Texts, ref countOfColumns);

            if (countOfColumns < 0)
            {
                MessageBox.Show("Вы ввели отрицательное число - количество столбцов, это неправильно. ");
            }
        }

        /// <summary>
        /// Обработчик событий, установленный через Designer, на поле с вводом удаляемого столбца
        /// </summary>
        private void NumberOfDeletingColumn__TextChanged(object sender, EventArgs e)
        {
            Handlers.HandleTextChanged(numberOfDeletingColumn.Texts, ref deleteColumnNumber);

            if (deleteColumnNumber <= 0 || deleteColumnNumber > countOfColumns)
            {
                MessageBox.Show("K находится в диапазоне от 1 до N ");
            }
        }

        /// <summary>
        /// Обработчик событий, установленный через Designer, на кнопку для удаления столбца
        /// </summary>
        public void ExecuteButton_Click(object sender, EventArgs e)
        {
            if (!(deleteColumnNumber.HasValue))
                return;

            _presenter.OnExecute(deleteColumnNumber.Value);
        }

        /// <summary>
        /// Обработчик событий, установленный через Designer, на кнопку для очистки всех значений на экране
        /// </summary>
        public void ClearButton_Click(object sender, EventArgs e)
        {
            dataGridView.Columns.Clear();
            numberOfDeletingColumn.Clear();
            countOfColumnsInput.Clear();
            countOfRowsInput.Clear();
        }
    }
}
