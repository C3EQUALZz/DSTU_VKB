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

/*
 * Created by Nguyen Hoang Thinh 17110372 at 19/04/2019
 */
namespace DoAnPaint
{
    public partial class PaintView : Form, ViewPaint
    {
        private PresenterDraw presenterDraw;

        private PresenterAlter presenterAlter;

        private PresenterUpdate presenterUpdate;

        private Graphics gr;


        public PaintView()
        {
            InitializeComponent();

            presenterDraw = new PresenterDrawImp(this);
            presenterAlter = new PresenterAlterImp(this);
            presenterUpdate = new PresenterUpdateImp(this);
            presenterUpdate.onClickSelectColor(ptbColor.BackColor, gr);
            presenterUpdate.onClickSelectSize(btnLineSize.Value + 1);

            gr = ptbDrawing.CreateGraphics();

        }

        //Sự kiện click chuột, gửi yêu cầu xử lý nhấn chuột đến presenter
        private void mouseDown_Event(object sender, MouseEventArgs e)
        {
            presenterDraw.onClickMouseDown(e.Location);
        }

        //Sự kiện di chuyển chuột, gửi yêu cầu xử lý di chuyển chuột đến presenter
        private void mouseMove_Event(object sender, MouseEventArgs e)
        {
            lbLocation.Text = e.Location.X + ", " + e.Location.Y + "px";
            presenterDraw.onClickMouseMove(e.Location);
        }

        //Callback gọi vẽ lại hình
        public void refreshDrawing()
        {
            ptbDrawing.Invalidate();
        }

        //Xử lý sự kiện click chuột vẽ hình, gửi yêu vẽ hình
        //theo trạng thái hiện tại đến presenter
        private void onPaint_Event(object sender, PaintEventArgs e)
        {
            e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;
            presenterDraw.getDrawing(e.Graphics);

        }

        //Callback để tiến hành vẽ hình
        public void setDrawing(Shape shape, Graphics g)
        {
            shape.drawShape(g);
        }

        //Xử lý sự kiện click chuột vẽ đường thẳng, gửi yêu cầu đến presenter
        private void btnLine_Click(object sender, EventArgs e)
        {
            presenterDraw.onClickDrawLine();
        }

        //Sự kiện thả chuột, gửi yêu cầu xử lý thả chuột đến presenter
        private void mouseUp_Event(object sender, MouseEventArgs e)
        {
            presenterDraw.onClickMouseUp();
        }

        private void btnSelect_Click(object sender, EventArgs e)
        {
            presenterUpdate.onClickSelectMode();
        }

        public void setCursor(Cursor cursor)
        {
            ptbDrawing.Cursor = cursor;
        }

        public void setDrawingLineSelected(Shape shape, Brush brush, Graphics g)
        {
            g.FillRectangle(brush, new Rectangle(shape.pointHead.X - 4, shape.pointHead.Y - 4, 8, 8));
            g.FillRectangle(brush, new Rectangle(shape.pointTail.X - 4, shape.pointTail.Y - 4, 8, 8));
        }

        public void movingShape(Shape shape, Point distance)
        {
            shape.moveShape(distance);
            refreshDrawing();
        }

        private void btnRectangle_Click(object sender, EventArgs e)
        {
            presenterDraw.onClickDrawRectangle();
        }

        private void btnEllipse_Click(object sender, EventArgs e)
        {
            presenterDraw.onClickDrawEllipse();
        }

        public void setDrawingRegionRectangle(Pen p, Rectangle rectangle, Graphics g)
        {
            g.DrawRectangle(p, rectangle);
        }

        private void btnGroup_Click(object sender, EventArgs e)
        {
            presenterAlter.onClickDrawGroup();
        }

        private void btnUnGroup_Click(object sender, EventArgs e)
        {
            presenterAlter.onClickDrawUnGroup();
        }

        private void btnDelete_Click(object sender, EventArgs e)
        {
            presenterAlter.onClickDeleteShape();
        }

        private void btnBezier_Click(object sender, EventArgs e)
        {
            presenterDraw.onClickDrawBezier();
        }

        private void btnPolygon_Click(object sender, EventArgs e)
        {
            presenterDraw.onClickDrawPolygon();
        }

        public void setDrawingCurveSelected(List<Point> points, Brush brush, Graphics g)
        {
            for (int i = 0; i < points.Count; ++i)
            {
                g.FillRectangle(brush, new Rectangle(points[i].X - 4, points[i].Y - 4, 8, 8));
            }

        }

        private void btnPen_Click(object sender, EventArgs e)
        {
            presenterDraw.onClickDrawPen();
        }

        private void btnEraser_Click(object sender, EventArgs e)
        {
            presenterDraw.onClickDrawEraser();
        }

        private void ptbEditColor_Click(object sender, EventArgs e)
        {
            ColorDialog colorDialog = new ColorDialog();
            if (colorDialog.ShowDialog() == DialogResult.OK)
            {
                presenterUpdate.onClickSelectColor(colorDialog.Color, gr);
            }
        }

        public void setColor(Color color)
        {
            ptbColor.BackColor = color;
        }

        private void btnLineSize_Scroll(object sender, EventArgs e)
        {
            presenterUpdate.onClickSelectSize(btnLineSize.Value + 1);
        }

        private void exitToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void aboutToolStripMenuItem_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Nguyễn Hoàng Thịnh - 17110372");
        }

        private void btnChangeColor_Click(object sender, EventArgs e)
        {
            PictureBox ptb = sender as PictureBox;
            ptbColor.BackColor = ptb.BackColor;
            presenterUpdate.onClickSelectColor(ptb.BackColor, gr);
        }

        private void ptbDrawing_MouseClick(object sender, MouseEventArgs e)
        {
            presenterDraw.onClickStopDrawing(e.Button);
        }

        private void pictureBox31_Click(object sender, EventArgs e)
        {
            presenterAlter.onClickShutdown(ptbDrawing);
        }

        public void movingControlPoint(Shape shape, Point pointCurrent, Point previous, int indexPoint)
        {
            shape.moveControlPoint(pointCurrent, previous, indexPoint);
            refreshDrawing();
        }

        private void btnClear_Click(object sender, EventArgs e)
        {
            presenterAlter.onClickClearAll(ptbDrawing);
        }

        private void btnFill_Click(object sender, EventArgs e)
        {
            Button btn = sender as Button;
            presenterUpdate.onClickSelectFill(btn, gr);
        }

        public void setColor(Button btn, Color color)
        {
            btn.BackColor = color;
        }

        private void btnSave_Click(object sender, EventArgs e)
        {
            presenterAlter.onClickSaveImage(ptbDrawing);
        }

        private void btnOpen_Click(object sender, EventArgs e)
        {
            presenterAlter.onClickOpenImage(ptbDrawing);
        }

        private void btnNew_Click(object sender, EventArgs e)
        {
            presenterAlter.onClickNewImage(ptbDrawing);
        }

        private void Form1_KeyDown(object sender, KeyEventArgs e)
        {
            presenterAlter.onUseKeyStrokes(ptbDrawing, e.KeyCode);
        }

    }
}
