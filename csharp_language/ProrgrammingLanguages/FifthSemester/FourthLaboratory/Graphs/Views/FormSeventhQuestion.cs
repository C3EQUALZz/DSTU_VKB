using DoAnPaint.Graphs.Core.Abstract;
using DoAnPaint.Graphs.Core.Interfaces;
using System.Collections.Generic;
using DoAnPaint.Graphs.Models.SeventhQuestion;

namespace DoAnPaint.Graphs.Views
{
    public partial class FormSeventhQuestion : BaseForm
    {
        public FormSeventhQuestion()
        {
            InitializeComponent();
            InitializeModels(new List<IModel> { new FirstModel(), new SecondModel(), new ThirdModel() });
        }

    }
}
