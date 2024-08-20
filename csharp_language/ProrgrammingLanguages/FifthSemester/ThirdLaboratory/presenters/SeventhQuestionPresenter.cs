using System.Collections.Generic;
using ThirdLaboratory.core.interfaces.seventhQuestion;

namespace ThirdLaboratory.presenters
{
    internal class SeventhQuestionPresenter : ISeventhQuestionPresenter
    {
        private readonly ISeventhQuestionView _view;
        private readonly ISeventhQuestionModel _model;

        public SeventhQuestionPresenter(ISeventhQuestionView view, ISeventhQuestionModel model)
        {
            _view = view;
            _model = model;
        }

        public void OnGenerateMatrix()
        {
            var matrix = _model.Execute();

            _view.RowCount = matrix.GetLength(0);
            _view.ColumnCount = matrix.GetLength(1);

            _view.Matrix = matrix;
        }

        public void OnExecute()
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
