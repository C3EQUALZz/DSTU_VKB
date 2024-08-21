using System;

namespace ThirdLaboratory.models
{
    /// <summary>
    /// Модель, которая будет считать сумму нашего массива
    /// </summary>
    /// <typeparam name="T">параметр, который может хранится в стеке (целое число, вещественное число и т.п, не объекты)</typeparam>
    internal class FirstQuestionModel<T> where T : struct
    {
        private readonly T[] _array;
        private int? _startIndex;
        private int? _endIndex;

        public FirstQuestionModel(T[] array, int startIndex, int endIndex)
        {
            _array = array;
            StartIndex = startIndex;
            EndIndex = endIndex;
        }

        /// <summary>
        /// Свойство для доступа к начальному индексу среза
        /// </summary>
        public int StartIndex
        {
            get => (int) _startIndex;
            set
            {
                if (value < 0 || (_endIndex != null && value > _endIndex))
                {
                    throw new ArgumentOutOfRangeException(nameof(StartIndex), "Начальный индекс должен быть в пределах допустимого диапазона.");
                }
                _startIndex = value;
            }
        }

        /// <summary>
        /// Свойство для доступа к конечному индексу среза
        /// </summary>
        public int EndIndex
        {
            get => (int) _endIndex;
            set
            {
                if ((_startIndex != null && value <= _startIndex) || value >= _array.Length)
                {
                    throw new ArgumentOutOfRangeException(nameof(EndIndex), "Конечный индекс должен быть в пределах допустимого диапазона.");
                }
                _endIndex = value;
            }
        }


        /// <summary>
        /// Метод для суммирования элементов массива c помощью среза
        /// </summary>
        /// <returns>возвращает сумму</returns>
        public dynamic Sum()
        {
            dynamic sum = 0;

            for (int i = StartIndex; i <= EndIndex; i++)
            {
                sum += (dynamic)_array[i];
            }

            return sum;
        }
    }
}
