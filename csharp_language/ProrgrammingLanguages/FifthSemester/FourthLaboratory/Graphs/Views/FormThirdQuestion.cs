using System.Collections.Generic;
using DoAnPaint.Graphs.Core.Abstract;
using DoAnPaint.Graphs.Core.Interfaces;
using DoAnPaint.Graphs.Models.ThirdQuestion;

namespace DoAnPaint.Graphs.Views
{
    public partial class FormThirdQuestion : BaseForm
    {
        public FormThirdQuestion()
        {
            InitializeComponent();
            InitializeModels(new List<IModel> { new FirstModel(), new SecondModel(), new ThirdModel() });
        }
    }
}
