using System.Collections.Generic;
using DoAnPaint.Graphs.Core.Abstract;
using DoAnPaint.Graphs.Core.Interfaces;
using DoAnPaint.Graphs.Models.FourthQuestion;

namespace DoAnPaint.Graphs.Views
{
    public partial class FormFourthQuestion : BaseForm
    {
        public FormFourthQuestion() : base(new List<IModel> { new FirstModel(), new SecondModel(), new ThirdModel() })
        {
            InitializeComponent();
        }
    }
}
