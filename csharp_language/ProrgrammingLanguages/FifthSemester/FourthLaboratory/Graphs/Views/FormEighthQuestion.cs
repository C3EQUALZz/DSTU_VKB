using DoAnPaint.Graphs.Core.Abstract;
using DoAnPaint.Graphs.Core.Interfaces;
using System.Collections.Generic;
using DoAnPaint.Graphs.Models.EighthQuestion;

namespace DoAnPaint.Graphs.Views
{
    public partial class FormEighthQuestion : BaseForm
    {
        public FormEighthQuestion() : base(new List<IModel> { new FirstModel(), new SecondModel(), new ThirdModel() })
        {
            InitializeComponent();
        }
    }
}
