using System;
using System.Collections.Generic;
using System.Windows.Forms;
using ThirdLaboratory.Core.Interfaces.FifthQuestion;

namespace ThirdLaboratory.Presenters
{
    internal class FifthQuestionPresenter : IFifthQuestionPresenter
    {

        private readonly IFifthQuestionView _view;
        private readonly IFifthQuestionModel _model;

        public FifthQuestionPresenter(IFifthQuestionView view, IFifthQuestionModel model)
        {
            _view = view;
            _model = model;
        }

        public void OnCellValidate(object sender, DataGridViewCellValidatingEventArgs e)
        {
            var dataGridView = sender as DataGridView;
            var error = e as DataGridViewCellValidatingEventArgs;

            string columnName = dataGridView.Columns[error.ColumnIndex].Name;
            string value = error.FormattedValue.ToString();

            if (string.IsNullOrWhiteSpace(value))
            {
                dataGridView.Rows[error.RowIndex].ErrorText = "Поле не может быть пустым.";
                error.Cancel = true;
                MessageBox.Show("Поле не может быть пустым.", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            if (columnName == "Owner")
            {
                if (!_model.IsValidOwner(value))
                {
                    dataGridView.Rows[error.RowIndex].ErrorText = "Фамилия и имя должны начинаться с большой буквы и состоять только из букв.";
                    error.Cancel = true;
                    MessageBox.Show("Фамилия и имя должны начинаться с большой буквы и состоять только из букв.", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }

            else if (columnName == "Number")
            {
                if (!_model.IsValidCarNumber(value))
                {
                    dataGridView.Rows[error.RowIndex].ErrorText = "Номер машины должен соответствовать принятому формату.";
                    error.Cancel = true;
                    MessageBox.Show("Номер машины должен соответствовать принятому формату.", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }


        /// <summary>
        /// Здесь идет обработка вывода для ListBox
        /// </summary>
        public void OnExecute(object sender, EventArgs e)
        {
            var matrix = _view.Matrix;
            var rows = new List<string>();

            for (int i = 0; i < matrix.GetLength(0); i++)
            {
                var row = "";

                for (int j = 0; j < matrix.GetLength(1); j++)
                {
                    row += matrix[i, j] + "\t";
                }
                rows.Add(row);
            }

            _view.ResultListBoxItems = rows;
        }
    }
}
