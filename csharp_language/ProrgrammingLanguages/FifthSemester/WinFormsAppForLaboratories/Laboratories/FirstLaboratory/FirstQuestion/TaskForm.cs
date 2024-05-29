namespace WinFormsAppForLaboratories.Laboratories.FirstLaboratory.FirstQuestion;

using System.Drawing.Drawing2D;

/// <summary>
/// Создайте пользовательскую форму, которая во время выполнения 
/// будет иметь овальное очертание.Данная форма должна содержать
/// функциональность, дающую возможность пользователю закрывать ее во время
/// выполнения. Рекомендация: при разработке формы в виде эллипса используйте
/// следующий код: myPath.AddEllipse(0, 0, this.Width, this.Height);
/// </summary>
public partial class TaskForm : Form
{
    private readonly Pen borderPen = new(Color.Black, 3);
    private readonly EllipseRegion ellipseRegion;

    /// <summary>
    /// Инициализирует новый экземпляр класса <see cref="TaskForm"/>.
    /// </summary>
    public TaskForm()
    {
        InitializeComponent();
        BackColor = Color.Red;
        ellipseRegion = new EllipseRegion(this);
    }

    /// <summary>
    /// Обрабатывает событие загрузки формы.
    /// </summary>
    /// <param name="e">Объект <see cref="EventArgs"/>, содержащий данные события.</param>
    protected override void OnLoad(EventArgs e)
    {
        base.OnLoad(e);
        ellipseRegion.Draw();
    }

    /// <summary>
    /// Обрабатывает событие изменения размера формы.
    /// </summary>
    /// <param name="e">Объект <see cref="EventArgs"/>, содержащий данные события.</param>
    protected override void OnResize(EventArgs e)
    {
        base.OnResize(e);
        ellipseRegion?.Draw();
    }

    /// <summary>
    /// Обрабатывает событие перерисовки формы.
    /// </summary>
    /// <param name="e">Объект <see cref="PaintEventArgs"/>, содержащий данные события.</param>
    protected override void OnPaint(PaintEventArgs e)
    {
        base.OnPaint(e);
        e.Graphics.DrawEllipse(borderPen, 0, 0, Width - 1, Height - 1);
    }

    /// <summary>
    /// Закрытие приложения
    /// </summary>
    /// <param name="sender"></param>
    /// <param name="e"></param>
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


