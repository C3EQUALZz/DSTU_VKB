using System;
using System.Drawing;
using System.Linq;
using System.Windows.Forms;
using DoAnPaint.Graphs.Core;
using DoAnPaint.Graphs.Core.Helpers;
using DoAnPaint.Graphs.Core.Interfaces;
using DoAnPaint.Graphs.Presenters;

namespace DoAnPaint
{
    public partial class MainForm : Form, IMainView
    {
        private readonly IMainPresenter _presenter;

        public MainForm()
        {
            _presenter = new MainPresenter(this, new FormFactory(this));

            InitializeComponent();
            this.SetBevel(false);
            Controls.OfType<MdiClient>().FirstOrDefault().BackColor = Color.FromArgb(232, 234, 237);
        }

        public void QuestionButton_Click(object sender, EventArgs e)
        {
            _presenter.OnButtonClick(sender, e);
        }

        /// <summary>
        /// После нажатия определенной кнопки задания открывается View, который был привязан. 
        /// Здесь идут визуальные изменения, поэтому делается на стороне View, а не Presenter, как я понимаю
        /// </summary>
        /// <param name="form">класс формы, который хотим показывать пользователю</param>
        public void ShowForm(Form form)
        {
            form.Show();
        }

        /// <summary>
        /// Если форма была загружена в память, то открывается заново (мое предположение, это взял из гайда в README.md).
        /// Опять-таки визуальное изменение, но тут на стороне View это, что тоже смущает...
        /// </summary>
        /// <param name="form">класс формы, который хотим показывать пользователю</param>
        public void ActivateForm(Form form)
        {
            form.Activate();
        }

        /// <summary>
        /// MDI приложение знает свои дочерние формы, которые я использую. 
        /// Здесь можно получить каждую форму чисто по имени, опять-таки идет поиск тегов с кнопки. 
        /// </summary>
        /// <param name="formName">имя формы, который мы получили с тэга кнопки</param>
        /// <returns>возвращает форму, если она была созана до этого, в ином случае null</returns>
        public Form GetOpenFormByName(string formName)
        {
            return MdiChildren.FirstOrDefault(f => f.GetType().Name == formName);
        }

        
    }
}
