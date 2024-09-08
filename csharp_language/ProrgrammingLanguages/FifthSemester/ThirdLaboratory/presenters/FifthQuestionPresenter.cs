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

            string columnName = dataGridView.Columns[e.ColumnIndex].Name;

            if (columnName == "Owner")
            {
                if (!_model.IsValidOwner(e.FormattedValue.ToString()))
                {
                    dataGridView.Rows[e.RowIndex].ErrorText = "Фамилия и имя должны начинаться с большой буквы и состоять из букв алфавита кириллицы.";
                    e.Cancel = true;
                }
            }

            else if (columnName == "Number")
            {
                if (!_model.IsValidCarNumber(e.FormattedValue.ToString()))
                {
                    dataGridView.Rows[e.RowIndex].ErrorText = "Номер машины должен соответствовать принятому формату.";
                    e.Cancel = true;
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
