using System.Linq;
using ThirdLaboratory.core.interfaces;

namespace ThirdLaboratory.presenters
{
    internal class NinthQuestionPresenter
    {
        private readonly INinthQuestionView _view;
        private readonly INinthQuestionModel _model;

        public NinthQuestionPresenter(INinthQuestionView view, INinthQuestionModel model)
        {
            _view = view;
            _model = model;
        }

        public void OnCreateMatrix(int rows, int columns)
        {
            _model.Initialize(rows, columns);
            _view.RowCount = rows;
            _view.ColumnCount = columns;

            _view.RowHeaders = Enumerable.Range(1, rows).Select(i => i.ToString()).ToArray();
            _view.ColumnHeaders = Enumerable.Range(1, columns).Select(i => i.ToString()).ToArray();
        }

        public void OnExecute()
        {
            var matrix = _view.Matrix;
            for (int i = 0; i < _model.Rows; i++)
            {
                for (int j = 0; j < _model.Columns; j++)
                {
                    _model.SetCellValue(i, j, matrix[i, j]);
                }
            }

            _model.Execute();

            _view.Matrix = _model.Matrix;
        }


    }
}
