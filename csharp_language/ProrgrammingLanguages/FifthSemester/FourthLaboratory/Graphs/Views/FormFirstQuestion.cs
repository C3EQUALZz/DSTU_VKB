using DoAnPaint.Graphs.Core.Interfaces;
using DoAnPaint.Graphs.Models;
using DoAnPaint.Graphs.Models.FirstQuestion;
using System.Collections.Generic;
using DoAnPaint.Graphs.Core.Abstract;

namespace DoAnPaint.Graphs.Views
{
    public partial class FormFirstQuestion : BaseForm
    {
        public FormFirstQuestion() : base(new List<IModel> { new FirstModel(), new SecondModel(), new ThirdModel() })
        {
            InitializeComponent();
        }

    }
}
