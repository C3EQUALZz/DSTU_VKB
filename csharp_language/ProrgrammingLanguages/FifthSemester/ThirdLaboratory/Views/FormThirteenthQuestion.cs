using System;
using System.ComponentModel;
using System.Linq;
using System.Windows.Forms;
using ThirdLaboratory.Core.Interfaces.ThirteenthQuestion;

namespace ThirdLaboratory.forms
{
    public partial class FormThirteenthQuestion : Form, IThirteenthQuestionView
    {
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
        /// Свойство для установки и получения текста в Label
        /// </summary>
        public string OutputText
        {
            get => outputLabel.Text; 
            set => outputLabel.Text = value;
        }

        public FormThirteenthQuestion()
        {
            InitializeComponent();
        }

        public void CountOfRows_Validating(object sender, CancelEventArgs e)
        {
            if (int.Parse(countOfRows.Texts) < 1)
            {
                MessageBox.Show("Вы ввели неправильное значение, количество строк может быть только больше 1");
                countOfRows.Clear();
            }
                
        }

        public void CountOfColumns_Validating(object sender, CancelEventArgs e)
        {
            if (int.Parse(countOfColumns.Texts) < 1)
            {
                MessageBox.Show("Вы ввели неправильное значение, количество столбцов может быть только больше 1");
                countOfColumns.Clear();
            }
        }

        public void NumberOfRow_Validating(object sender, CancelEventArgs e)
        {
            var parsedNumber = int.Parse(numberOfRow.Texts);

            if (parsedNumber < 1 || parsedNumber > int.Parse(countOfRows.Texts))
            {
                MessageBox.Show("Вы ввели неправильное значение, количество столбцов может быть только больше 1");
                countOfColumns.Clear();
            }
        }

        public void GenerateRandomMatrixButton_Click(object sender, EventArgs e)
        {
            
        }

        public void ClearButton_Click(object sender, EventArgs e)
        {
            countOfRows.Clear();
            countOfColumns.Clear();
            numberOfRow.Clear();

            foreach (DataGridViewRow row in dataGridView.Rows)
            {
                foreach (DataGridViewCell cell in row.Cells)
                {
                    cell.Value = null;
                }
            }
        }

        public void ExecuteButton_Click(object sender, EventArgs e)
        {

        }
    }
}
