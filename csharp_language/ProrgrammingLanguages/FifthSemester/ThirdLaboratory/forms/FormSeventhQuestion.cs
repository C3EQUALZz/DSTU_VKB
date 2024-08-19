using System;
using System.Linq;
using System.Windows.Forms;
using ThirdLaboratory.core.interfaces.seventhQuestion;

namespace ThirdLaboratory.forms
{
    public partial class FormSeventhQuestion : Form, ISeventhQuestionView
    {
        public FormSeventhQuestion()
        {
            InitializeComponent();

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

        public void GenerateButton_Click(object sender, EventArgs e)
        {

        }

        public void ClearButton_Click(object sender, EventArgs e)
        {
            resultListBox.Items.Clear();
            dataGridView.ClearSelection();
        }

        public void ExecuteButton_Click(object sender, EventArgs e)
        {
           
        }
    }
}
