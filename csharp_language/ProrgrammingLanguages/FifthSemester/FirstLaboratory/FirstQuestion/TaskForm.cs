using System.Drawing.Drawing2D;

namespace FirstLaboratory.FirstQuestion
{
    public partial class TaskForm : Form
    {
        private readonly Pen borderPen = new(Color.Black, 3);
        private readonly EllipseRegion ellipseRegion;

        public TaskForm()
        {
            InitializeComponent();
            BackColor = Color.Red;
            ellipseRegion = new EllipseRegion(this);
        }

        /// <summary>
        /// Обрабатывает событие изменения размера формы.
        /// </summary>
        private void TaskForm_Resize(object sender, EventArgs e)
        {
            ellipseRegion?.Draw();
        }

        /// <summary>
        /// Обрабатывает событие перерисовки формы.
        /// </summary>
        /// <param name="e">Объект <see cref="PaintEventArgs"/>, содержащий данные события.</param>
        private void TaskForm_Paint(object sender, PaintEventArgs e)
        {
            e.Graphics.DrawEllipse(borderPen, 0, 0, Width - 1, Height - 1);
        }

        /// <summary>
        /// Закрытие приложения
        /// </summary>
        private void ExitButton_Click(object sender, EventArgs e)
        {
            Close();
        }

        
    }

    /// <summary>
    /// Управляет эллиптическим регионом формы.
    /// </summary>
    class EllipseRegion(Form form)
    {
        private readonly Form form = form ?? throw new ArgumentNullException(nameof(form));
        private readonly GraphicsPath path = new();

        /// <summary>
        /// Обновляет регион формы до эллипса. 
        /// </summary>
        public void Draw()
        {
            path.Reset();
            path.AddEllipse(0, 0, form.Width, form.Height);
            form.Region = new Region(path);
        }
    }
}
