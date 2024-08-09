using ThirdLaboratory.models;
using System;

namespace ThirdLaboratory.controllers
{
    public class FirstQuestionController<T> where T : struct
    {
        private FirstQuestionModel<T> _model;

        public string ValidateInputs(int? lengthOfArray, int? startIndex, int? endIndex)
        {
            if (lengthOfArray == null || startIndex == null || endIndex == null)
                return "Все поля должны быть заполнены";

            if (lengthOfArray <= 0)
                return "Длина массива должна быть больше нуля";

            if (startIndex <= 0 || startIndex >= lengthOfArray)
                return "Стартовый индекс должен быть больше нуля и меньше длины массива";

            if (endIndex <= 0 || endIndex <= startIndex || endIndex > lengthOfArray)
                return "Конечный индекс должен быть больше стартового индекса и не превышать длину массива";

            return null;
        }

        public double[] CreateArray(int length)
        {
            double[] array = new double[length];
            Random rand = new Random();
            for (int i = 0; i < array.Length; i++)
                array[i] = Math.Round(rand.NextDouble(), 2);

            return array;
        }

        public void InitializeModel(T[] array, int startIndex, int endIndex)
        {
            _model = new FirstQuestionModel<T>(array, startIndex, endIndex);
        }

        public dynamic CalculateSum()
        {
            return _model?.Sum();
        }
    }
}
