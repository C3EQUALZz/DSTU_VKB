using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;
using ThirdLaboratory.core.interfaces.seventhQuestion;
using ThirdLaboratory.models;
using ThirdLaboratory.presenters;

namespace ThirdLaboratory.forms
{
    public partial class FormSeventhQuestion : Form, ISeventhQuestionView
    {
        private readonly ISeventhQuestionPresenter _presenter;

        public FormSeventhQuestion()
        {
            InitializeComponent();
            _presenter = new SeventhQuestionPresenter(this, new SeventhQuestionModel());
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
        /// Нужно использовать ListBox, как я понимаю, поэтому 
        /// </summary>
        public List<string> ResultListBoxItems
        {
            get => resultListBox.Items.Cast<string>().ToList();
            set
            {
                resultListBox.Items.Clear();
                foreach (var item in value)
                {
                    resultListBox.Items.Add(item);
                }
            }
        }

        /// <summary>
        /// Обработчик, установленный через Designer, на кнопку generateButton
        /// Здесь запускается создание случайной матрицы
        /// </summary>
        public void GenerateButton_Click(object sender, EventArgs e)
        {
            _presenter.OnGenerateMatrix();
        }

        /// <summary>
        /// Обработчик на очистку всех полей
        /// </summary>
        public void ClearButton_Click(object sender, EventArgs e)
        {
            resultListBox.Items.Clear();
            dataGridView.Columns.Clear();
        }

        /// <summary>
        /// Обработчик на вывод матрицы в ListBox
        /// </summary>
        public void ExecuteButton_Click(object sender, EventArgs e)
        {
            _presenter.OnExecute();
        }

        /// <summary>
        /// В паттерне MVP валидация происходит на View.
        /// Для DataGridView здесь написана валидация, чтобы были только числа
        /// </summary>
        public void DataGridView_CellValidating(object sender, DataGridViewCellValidatingEventArgs e)
        {
            var input = e.FormattedValue.ToString();

            if (!int.TryParse(input, out int _))
            {
                MessageBox.Show("Пожалуйста, введите только числовые значения.", "Некорректный ввод", MessageBoxButtons.OK, MessageBoxIcon.Warning);

                e.Cancel = true;
                dataGridView.CancelEdit();
                dataGridView[e.ColumnIndex, e.RowIndex].Value = string.Empty;
            }
        }
    }
}
