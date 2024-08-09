using ThirdLaboratory.models;

namespace ThirdLaboratory.controllers
{
    public class FirstQuestionController<T> where T : struct
    {
        private readonly FirstQuestionModel<T> _model;

        public FirstQuestionController(T[] array, int startIndex, int endIndex)
        {
            _model = new FirstQuestionModel<T>(array, startIndex, endIndex);
        }

        public dynamic CalculateSum()
        {
            return _model.Sum();
        }

    }
}
