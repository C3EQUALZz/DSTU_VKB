using System;
using System.Drawing;
using System.Linq;
using System.Windows.Forms;
using ThirdLaboratory.core;
using ThirdLaboratory.core.helpers;
using ThirdLaboratory.core.interfaces;
using ThirdLaboratory.presenters;

namespace ThirdLaboratory
{
    public partial class MainForm : Form, IMainView
    {
        private readonly MainPresenter _presenter;

        /// <summary>
        /// Главный View приложения, который агрегирует все остальные View с помощью MDI построения приложения. 
        /// </summary>
        public MainForm()
        {
            InitializeComponent();
            this.SetBevel(false);

            _presenter = new MainPresenter(
                this,
                new FormFactory(this),
                new CommandContext(this),
                new SideBarContext(this)
             );


            Controls.OfType<MdiClient>().FirstOrDefault().BackColor = Color.FromArgb(232, 234, 237);
        }

        /// <summary>
        /// Назначен через Designer (Drag and Drop в VS)
        /// Метод для панелей - кнопок (1 - 5 задание, 6 - 10 задание и т.п). 
        /// Здесь идет передача презентеру, который будет раскрывать панель, чтобы вы могли выбрать задание. 
        /// </summary>
        public void Button_Click(object sender, EventArgs e)
        {
            _presenter.OnButtonClick(sender, e);
        }

        /// <summary>
        /// Назначен через Designer (Drag and Drop в VS)
        /// У каждой из панелей - кнопок (1 - 5 задание, 6 - 10 задание и т.п) есть анимация раскрытия. 
        /// Так вот, данный метод нужен, чтобы началась анимация раскрытия через таймер.
        /// Данный подход был реализован в видео, который я приложил в README.md
        /// </summary>
        public void Timer_Tick(object sender, EventArgs e)
        {
            _presenter.OnTimerTick(sender, e);
        }

        /// <summary>
        /// Назначен через Designer (Drag and Drop в VS)
        /// Таймер для слайдера - боковое меню. Опять-таки нужен для анимации раскрытия. 
        /// Более подробно ознакомтесь в README.md с видео
        /// </summary>
        public void TimerTransition_Tick(object sender, EventArgs e)
        {
            _presenter.OnTimerTransitionTick(sender, e);
        }

        /// <summary>
        /// Назначен через Designer (Drag and Drop в VS)
        /// Обработчик события нажатия на кнопку меню, который открывает и закрывает меню 
        /// </summary>
        public void MenuButton_Click(object sender, EventArgs e)
        {
            _presenter.OnMenuButtonClick(sender, e);
        }

        /// <summary>
        /// Назначен через Designer (Drag and Drop в VS)
        /// Обработчик события нажатия на кнопку на каждое из заданий (1 задание, 2 задание, 3 задание и т.п.).
        /// Каждая кнопка, образно говоря, привязана к форме через тег (св-во в Designer). 
        /// Я использую рефликсию, чтобы достать форму в зависимости от значения в тэге.
        /// Например, в тэге стоит (FormFirstQuestion) => значит будет создан FormFirstQuestion класс
        /// </summary>
        public void QuestionButton_Click(object sender, EventArgs e)
        {
            _presenter.OnQuestionButtonClick(sender, e);
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
