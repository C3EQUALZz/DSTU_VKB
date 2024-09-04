using System;
using System.Collections.Generic;
using System.Linq;
using DoAnPaint.Graphs.Core.Interfaces.FirstQuestion;
using LiveCharts;
using LiveCharts.Wpf;

namespace DoAnPaint.Graphs.Presenters
{
    internal class FirstQuestionPresenter : IPresenter
    {
        private readonly IView _view;
        private readonly List<IModel> _models;
        private readonly List<IModel> _selectedModels;

        public FirstQuestionPresenter(IView view, List<IModel> models)
        {
            _view = view;
            _models = models;
            _selectedModels = new List<IModel>();
        }

        /// <summary>
        /// Данный метод нужен для реализации выбора графиков.
        /// Вот, например, вы нажали на 2 checkbox, значит в данном списке появится 2 модель 
        /// </summary>
        /// <param name="model">Модель функции</param>
        public void SelectModel(IModel model)
        {
            if (!_selectedModels.Contains(model))
            {
                _selectedModels.Add(model);
            }
        }

        /// <summary>
        /// Метод для отмены выбора модели. 
        /// Вот, например, вы нажали на 2 checkbox, где уже была галочка с целью убрать, значит в данном списке удалится 2 модель
        /// </summary>
        /// <param name="model"></param>
        public void DeselectModel(IModel model)
        {
            if (_selectedModels.Contains(model))
            {
                _selectedModels.Remove(model);
            }
        }

        /// <summary>
        /// Главный метод отрисовки, мне не совсем он тоже нравится, так как у него внутри много логики, что нарушает Solid
        /// С другой стороны, я здесь инкапсулирую внутреннию логику установки легенд и т.п.
        /// </summary>
        public void Draw()
        {
            var xValues = GenerateXValues();
            var series = GenerateSeriesCollection(xValues);
            _view.ChartData = series;

            SetAxisX(xValues);
            SetAxisY(series);
            SetLegent(_view);

            if (_view.IsAnimationEnabled)
            {
                _view.CartesianChart.DisableAnimations = false;
                _view.CartesianChart.AnimationsSpeed = TimeSpan.FromMilliseconds(300);
            }
            else
            {
                _view.CartesianChart.DisableAnimations = true;
            }
                
        }

        /// <summary>
        /// Генерирует список значений по оси X на основе заданных параметров.
        /// </summary>
        /// <returns>Список значений по оси X.</returns>
        private List<double> GenerateXValues()
        {
            var xValues = new List<double>();
            for (double x = _view.Start; x <= _view.End; x += _view.Step)
            {
                xValues.Add(x);
            }
            return xValues;
        }

        /// <summary>
        /// Создает коллекцию серий на основе выбранных моделей и значений по оси X.
        /// </summary>
        /// <param name="xValues">Список значений по оси X.</param>
        /// <returns>Коллекция серий для отображения на графике.</returns>
        private SeriesCollection GenerateSeriesCollection(List<double> xValues)
        {
            var series = new SeriesCollection();

            foreach (var model in _selectedModels)
            {
                var values = new ChartValues<double>();
                foreach (var x in xValues)
                {
                    values.Add(model.Calculate(x));
                }

                if (values.Count > 0)
                {
                    series.Add(CreateLineSeries(model, values));
                }
            }

            return series;
        }

        /// <summary>
        /// Создает линию графика для заданной модели и значений.
        /// </summary>
        /// <param name="model">Модель, для которой создается линия.</param>
        /// <param name="values">Значения, соответствующие модели.</param>
        /// <returns>Объект LineSeries, представляющий линию графика.</returns>
        private LineSeries CreateLineSeries(IModel model, ChartValues<double> values)
        {
            return new LineSeries
            {
                Title = model.Name,
                Values = values,
                PointGeometry = DefaultGeometries.Circle,
                PointGeometrySize = 10
            };
        }

        /// <summary>
        /// Настраивает ось X графика на основе заданных значений.
        /// </summary>
        /// <param name="xValues">Список значений по оси X.</param>
        private void SetAxisX(List<double> xValues)
        {
            var axisX = new Axis
            {
                MinValue = _view.Start,
                MaxValue = _view.End + 3, 
                Separator = new Separator
                {
                    Step = _view.Step
                    
                },
                Labels = xValues.ConvertAll(x => x.ToString("F2"))

            };

            _view.CartesianChart.AxisX.Clear();
            _view.CartesianChart.AxisX.Add(axisX);
        }

        /// <summary>
        /// Настраивает ось Y графика на основе значений серий.
        /// </summary>
        /// <param name="series">Коллекция серий, используемая для настройки оси Y.</param>
        private void SetAxisY(SeriesCollection series)
        {
            if (series.Any())
            {
                double maxValue = series.Max(s => s.Values.Cast<double>().Max());
                double minValue = series.Min(s => s.Values.Cast<double>().Min());

                _view.CartesianChart.AxisY[0].MaxValue = maxValue;
                _view.CartesianChart.AxisY[0].MinValue = minValue;
            }
            else
            {
                _view.CartesianChart.AxisY[0].MaxValue = 0;
                _view.CartesianChart.AxisY[0].MinValue = 0;
            }
        }


        /// <summary>
        /// Немного избыточный метод... Не спорю
        /// Здесь идет установка легенды справа
        /// </summary>
        /// <param name="view"></param>
        private void SetLegent(IView view)
        {
            view.CartesianChart.LegendLocation = LegendLocation.Right;
        }




    }
}
