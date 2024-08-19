using ThirdLaboratory.core.interfaces;
using ThirdLaboratory.core.interfaces.secondQuestion;

namespace ThirdLaboratory.presenters
{
    internal class SecondQuestionPresenter : ISecondQuestionPresenter
    {
        private readonly ISecondQuestionView _view;
        private readonly ISecondQuestionModel _model;

        /// <summary>
        /// Презентер, который отвечает за 2 задание
        /// </summary>
        /// <param name="formSecondQuestion">View на второе задание, который я создал через Designer</param>
        /// <param name="secondQuestionModel">Model на второе задание, которая реализует логику задания</param>
        public SecondQuestionPresenter(ISecondQuestionView formSecondQuestion, ISecondQuestionModel secondQuestionModel)
        {
            _view = formSecondQuestion;
            _model = secondQuestionModel;
        }

        /// <summary>
        /// Точка запуска презентера, которая взаимодействует и с View, и с Model
        /// </summary>
        public void OnExecute()
        {
            var result = _model.Execute();

            if (result == "Все заявки содержат корректные фамилии")
                _view.ResultOutput = $"{result}\nМассив 'Заявки': {string.Join(", ", _view.RequestsInput)}";
            else
                _view.ResultOutput = _model.Execute();
        }

        /// <summary>
        /// Метод, который обновляет значения в модели при измении каких-то данных в View
        /// </summary>
        /// <param name="staffInput">строка с вводом фамилий сотрудников</param>
        /// <param name="requestInput">строка с вводом заявок</param>
        public void Update(string staffInput, string requestInput)
        {
            _model.SetStaffers(staffInput);
            _model.SetRequests(requestInput);
        }
    }
}
