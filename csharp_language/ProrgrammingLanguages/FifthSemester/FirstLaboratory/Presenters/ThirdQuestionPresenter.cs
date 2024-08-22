using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using FirstLaboratory.Core.Interfaces.ThirdQuestion;

namespace FirstLaboratory.Presenters
{
    internal class ThirdQuestionPresenter
    {
        private readonly IThirdQuestionView _view;
        private readonly IThirdQuestionModel _model;

        public ThirdQuestionPresenter(IThirdQuestionView view, IThirdQuestionModel model)
        {
            _view = view;
            _model = model;
        }




    }
}
