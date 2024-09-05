using DoAnPaint.Graphs.Core.Abstract;
using DoAnPaint.Graphs.Core.Interfaces;
using System.Collections.Generic;
using DoAnPaint.Graphs.Models.SixthQuestion;


namespace DoAnPaint.Graphs.Views
{
    public partial class FormSixthQuestion : BaseForm
    {
        public FormSixthQuestion() : base(new List<IModel> { new FirstModel(), new SecondModel(), new ThirdModel() })
        {
            InitializeComponent();
        }
    }
}
