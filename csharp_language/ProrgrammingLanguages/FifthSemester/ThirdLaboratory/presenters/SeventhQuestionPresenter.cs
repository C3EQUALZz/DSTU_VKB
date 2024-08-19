using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
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
            _view.Matrix = _model.Execute();
        }

        public void OnExecute()
        {
            _model.Execute();
        }
    }
}
