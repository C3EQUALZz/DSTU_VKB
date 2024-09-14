using System.Linq;
using ThirdLaboratory.Core.Interfaces.ThirteenthQuestion;

namespace ThirdLaboratory.Presenters
{
    internal class ThirteenthQuestionPresenter : IThirteenthQuestionPresenter
    {
        private readonly IThirteenthQuestionView _view;
        private readonly IThirteenthQuestionModel _model;

        public ThirteenthQuestionPresenter(IThirteenthQuestionView view, IThirteenthQuestionModel model)
        {
            _view = view;
            _model = model;
        }

        /// <summary>
        /// Обработчик, который создает матрицу
        /// </summary>
        public void OnCreateMatrix(int rows, int columns)
        {
            _model.Initialize(rows, columns);
            _view.RowCount = rows;
            _view.ColumnCount = columns;

            _view.RowHeaders = Enumerable.Range(1, rows).Select(i => i.ToString()).ToArray();
            _view.ColumnHeaders = Enumerable.Range(1, columns).Select(i => i.ToString()).ToArray();
            _view.Matrix = _model.Matrix;
        }

        /// <summary>
        /// Точка запуска для удаления матрицы
        /// </summary>
        /// <param name="index">номер столбца, который хотим удалить</param>
        public void OnExecute(int index)
        {
            _view.OutputText = $"Строка под номером {index} " + string.Join(", ", _model.Execute(index));
        }

    }
}
