using System.Linq;
using ThirdLaboratory.core.interfaces.nineteenthQuestion;

namespace ThirdLaboratory.presenters
{
    internal class NineteenthQuestionPresenter : INineteenthQuestionPresenter
    {
        private readonly INineteenthQuestionView _view;
        private readonly INineteenthQuestionModel _model;

        /// <summary>
        /// Презентер для 19 задания
        /// </summary>
        /// <param name="view">вьюшка 19 задания</param>
        /// <param name="model">модель 19 задания</param>
        public NineteenthQuestionPresenter(INineteenthQuestionView view, INineteenthQuestionModel model)
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
            _model.Execute(index);
            _view.ColumnCount = _model.Columns;
            _view.Matrix = _model.Matrix;
        }
    }
}
