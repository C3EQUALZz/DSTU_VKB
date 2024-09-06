using System.Collections.Generic;
using DoAnPaint.Graphs.Core.Interfaces;
using DoAnPaint.Graphs.Models.SecondQuestion;
using DoAnPaint.Graphs.Core.Abstract;

namespace DoAnPaint.Graphs.Views
{
    public partial class FormSecondQuestion : BaseForm
    {
        public FormSecondQuestion()
        {
            InitializeComponent();
            InitializeModels(new List<IModel> { new FirstModel(), new SecondModel(), new ThirdModel() });
        }
    }
}
