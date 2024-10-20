using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;
using System.Drawing.Drawing2D;

using DoAnPaint.View;
using DoAnPaint.Model;
using DoAnPaint.Presenter;
using DoAnPaint.Presenter.Alter;
using DoAnPaint.Presenter.Updates;


namespace DoAnPaint
{
    public partial class PaintView : Form, IViewPaint
    {
        private readonly IPresenterDraw presenterDraw;

        private readonly IPresenterAlter presenterAlter;

        private readonly IPresenterUpdate presenterUpdate;

        private readonly Graphics gr;


        public PaintView()
        {
            InitializeComponent();

            presenterDraw = new PresenterDrawImp(this);
            presenterAlter = new PresenterAlterImp(this);
            presenterUpdate = new PresenterUpdateImp(this);
            presenterUpdate.OnClickSelectColor(ptbColor.BackColor, gr);
            presenterUpdate.OnClickSelectSize(btnLineSize.Value + 1);

            gr = ptbDrawing.CreateGraphics();
        }

        /// <summary>
        /// Событие щелчка мыши отправляет презентатору запрос на обработку.
        /// </summary>
        public void MouseDown_Event(object sender, MouseEventArgs e)
        {
            presenterDraw.OnClickMouseDown(e.Location);
        }

        /// <summary>
        /// Событие перемещения мыши отправляет презентатору запрос обработчика перемещения мыши.
        /// </summary>
        public void MouseMove_Event(object sender, MouseEventArgs e)
        {
            lbLocation.Text = e.Location.X + ", " + e.Location.Y + "px";
            presenterDraw.OnClickMouseMove(e.Location);
        }

        /// <summary>
        /// Вызов для перерисовки изображения
        /// </summary>
        public void RefreshDrawing()
        {
            ptbDrawing.Invalidate();
        }

        /// <summary>
        /// Обработка события щелчка мыши для рисования изображения,
        /// здесь происходит отправка презентатору запроса на рисование изображения в соответствии с текущим состоянием.
        /// </summary>
        public void OnPaint_Event(object sender, PaintEventArgs e)
        {
            e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;
            presenterDraw.GetDrawing(e.Graphics);
        }

        /// <summary>
        /// Вызов для продолжения рисования
        /// </summary>
        public void SetDrawing(Shape shape, Graphics g)
        {
            shape.drawShape(g);
        }

        /// <summary>
        /// Обработка событие щелчка мыши, чтобы нарисовать линию, отправляю запрос презентеру
        /// </summary>
        public void BtnLine_Click(object sender, EventArgs e)
        {
            presenterDraw.OnClickDrawLine();
        }

        /// <summary>
        /// Событие "отпускания мыши" отправляет презентатору запрос на обработку.
        /// </summary>
        public void MouseUp_Event(object sender, MouseEventArgs e)
        {
            presenterDraw.OnClickMouseUp();
        }

        /// <summary>
        /// Обработчик событий на кнопку, где есть режим "выбор" 
        /// </summary>
        public void BtnSelect_Click(object sender, EventArgs e)
        {
            presenterUpdate.OnClickSelectMode();
        }

        /// <summary>
        /// Сеттер для установки курсора, который выбрал пользователь
        /// </summary>
        public void SetCursor(Cursor cursor)
        {
            ptbDrawing.Cursor = cursor;
        }

        public void SetDrawingLineSelected(Shape shape, Brush brush, Graphics g)
        {
            g.FillRectangle(brush, new Rectangle(shape.pointHead.X - 4, shape.pointHead.Y - 4, 8, 8));
            g.FillRectangle(brush, new Rectangle(shape.pointTail.X - 4, shape.pointTail.Y - 4, 8, 8));
        }

        public void MovingShape(Shape shape, Point distance)
        {
            shape.moveShape(distance);
            RefreshDrawing();
        }

        public void BtnRectangle_Click(object sender, EventArgs e)
        {
            presenterDraw.OnClickDrawRectangle();
        }

        public void BtnEllipse_Click(object sender, EventArgs e)
        {
            presenterDraw.OnClickDrawEllipse();
        }

        public void SetDrawingRegionRectangle(Pen p, Rectangle rectangle, Graphics g)
        {
            g.DrawRectangle(p, rectangle);
        }

        public void BtnGroup_Click(object sender, EventArgs e)
        {
            presenterAlter.OnClickDrawGroup();
        }

        public void BtnUnGroup_Click(object sender, EventArgs e)
        {
            presenterAlter.OnClickDrawUnGroup();
        }

        public void BtnDelete_Click(object sender, EventArgs e)
        {
            presenterAlter.OnClickDeleteShape();
        }

        public void BtnBezier_Click(object sender, EventArgs e)
        {
            presenterDraw.OnClickDrawBezier();
        }

        public void BtnPolygon_Click(object sender, EventArgs e)
        {
            presenterDraw.OnClickDrawPolygon();
        }

        public void SetDrawingCurveSelected(List<Point> points, Brush brush, Graphics g)
        {
            for (int i = 0; i < points.Count; ++i)
            {
                g.FillRectangle(brush, new Rectangle(points[i].X - 4, points[i].Y - 4, 8, 8));
            }
        }

        public void BtnPen_Click(object sender, EventArgs e)
        {
            presenterDraw.OnClickDrawPen();
        }

        public void BtnEraser_Click(object sender, EventArgs e)
        {
            presenterDraw.OnClickDrawEraser();
        }

        public void PtbEditColor_Click(object sender, EventArgs e)
        {
            ColorDialog colorDialog = new ColorDialog();
            if (colorDialog.ShowDialog() == DialogResult.OK)
            {
                presenterUpdate.OnClickSelectColor(colorDialog.Color, gr);
            }
        }

        public void SetColor(Color color)
        {
            ptbColor.BackColor = color;
        }

        public void BtnLineSize_Scroll(object sender, EventArgs e)
        {
            presenterUpdate.OnClickSelectSize(btnLineSize.Value + 1);
        }

        public void BtnChangeColor_Click(object sender, EventArgs e)
        {
            PictureBox ptb = sender as PictureBox;
            ptbColor.BackColor = ptb.BackColor;
            presenterUpdate.OnClickSelectColor(ptb.BackColor, gr);
        }

        public void PtbDrawing_MouseClick(object sender, MouseEventArgs e)
        {
            presenterDraw.OnClickStopDrawing(e.Button);
        }

        public void MovingControlPoint(Shape shape, Point pointCurrent, Point previous, int indexPoint)
        {
            shape.moveControlPoint(pointCurrent, previous, indexPoint);
            RefreshDrawing();
        }

        public void BtnClear_Click(object sender, EventArgs e)
        {
            presenterAlter.OnClickClearAll(ptbDrawing);
        }

        public void BtnFill_Click(object sender, EventArgs e)
        {
            Button btn = sender as Button;
            presenterUpdate.OnClickSelectFill(btn, gr);
        }

        public void SetColor(Button btn, Color color)
        {
            btn.BackColor = color;
        }

        public void BtnSave_Click(object sender, EventArgs e)
        {
            presenterAlter.OnClickSaveImage(ptbDrawing);
        }

        public void BtnOpen_Click(object sender, EventArgs e)
        {
            presenterAlter.OnClickOpenImage(ptbDrawing);
        }

        public void BtnNew_Click(object sender, EventArgs e)
        {
            presenterAlter.OnClickNewImage(ptbDrawing);
        }

        public void Form_KeyDown(object sender, KeyEventArgs e)
        {
            presenterAlter.OnUseKeyStrokes(ptbDrawing, e.KeyCode);
        }

    }
}
