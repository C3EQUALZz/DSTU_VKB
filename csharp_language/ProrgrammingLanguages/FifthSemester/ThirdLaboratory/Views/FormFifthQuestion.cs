using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Windows.Forms;
using ThirdLaboratory.Core.Interfaces.FifthQuestion;
using ThirdLaboratory.Models;
using ThirdLaboratory.Presenters;

namespace ThirdLaboratory.forms
{
    public partial class FormFifthQuestion : Form, IFifthQuestionView
    {
        private readonly IFifthQuestionPresenter _presenter;

        public FormFifthQuestion()
        {
            _presenter = new FifthQuestionPresenter(this, new FifthQuestionModel());

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

        public void ClearButton_Click(object sender, EventArgs e)
        {
            resultListBox.Items.Clear();

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
            _presenter.OnExecute(sender, e);
        }

        public void DataGridView_CellValidating(object sender, DataGridViewCellValidatingEventArgs e)
        {
            _presenter.OnCellValidate(sender, e);
        }
    }
}
