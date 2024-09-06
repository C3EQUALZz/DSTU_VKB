using DoAnPaint.Graphs.Core.Abstract;
using DoAnPaint.Graphs.Core.Interfaces;
using System.Collections.Generic;
using DoAnPaint.Graphs.Models.FifthQuestion;

namespace DoAnPaint.Graphs.Views
{
    public partial class FormFifthQuestion : BaseForm
    {
        public FormFifthQuestion()
        {
            InitializeComponent();
            InitializeModels(new List<IModel> { new FirstModel(), new SecondModel(), new ThirdModel() });
        }
    }
}
