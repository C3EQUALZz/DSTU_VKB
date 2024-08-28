using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Drawing;
using System.Drawing.Drawing2D;

using DoAnPaint.Utils;


/*
 * Created by Nguyen Hoang Thinh 17110372 at 19/04/2019
 */
namespace DoAnPaint.Model
{
    public abstract class Shape:ICloneable
    {
        //TODO: cho biết tên của hình
        public string name { get; set; }

        //TODO: cho biết điểm đầu của hình
        public Point pointHead { get; set; }

        //TODO: cho biết điểm cuối của hình
        public Point pointTail { get; set;}

        //TODO: cho biết hình đang được chọn hay không
        public bool isSelected { get; set; }

        //TODO: cho biết độ dày đường viền hình vẽ
        public int contourWidth { get; set; }

        //TODO: cho biết hình vẽ có ở chế độ tô màu hay không
        public bool isFill { get; set; }

        //TODO: cho biết màu sắc của hình
        public Color color { get; set; }

        //TODO: tạo ra một đối tượng copy từ đối tượng này
        public abstract object Clone();

        /// <summary>
        /// Phương thức vẽ hình hiện tại lên graphics
        /// </summary>
        /// <param name="g">graphics</param>
        public abstract void drawShape(Graphics g);

        /// <summary>
        /// Phương thức di chuyển hình hiện tại với khoảng cách distance
        /// </summary>
        /// <param name="distance">khoảng cách</param>
        public virtual void moveShape(Point distance)
        {
            pointHead = new Point(pointHead.X + distance.X, pointHead.Y + distance.Y);
            pointTail = new Point(pointTail.X + distance.X, pointTail.Y + distance.Y);
        }

        /// <summary>
        /// Phương thức cho biết điểm p có thuộc hình này hay không
        /// </summary>
        /// <param name="p">điểm cần xét</param>
        /// <returns></returns>
        public abstract bool isHit(Point p);

        /// <summary>
        /// Phương thức tạo ra đối tượng graphicsPath của hình
        /// </summary>
        protected abstract GraphicsPath graphicsPath { get; }

        /// <summary>
        /// Phương thức cho biết một hình chữ nhật có bao bọc chính hình này hay không
        /// </summary>
        /// <param name="rectangle">Hình chữ nhật cần xét</param>
        /// <returns></returns>
        public virtual bool isInRegion(Rectangle rectangle)
        {
            return pointHead.X >= rectangle.X &&
                pointTail.X <= rectangle.X + rectangle.Width &&
                pointHead.Y >= rectangle.Y &&
                pointTail.Y <= rectangle.Y + rectangle.Height;
        }

        /// <summary>
        /// Phương thức nhận một hình chữ nhật từ điểm đầu và cuối của hình này
        /// </summary>
        /// <returns></returns>
        public Rectangle getRectangle()
        {
            return new Rectangle(pointHead.X,
                pointHead.Y,
                pointTail.X - pointHead.X,
                pointTail.Y - pointHead.Y);
        }

        /// <summary>
        /// Phương thức nhận một hình chữ nhật từ 2 điểm a và b
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public Rectangle getRectangle(Point a, Point b)
        {
            if (a.X > b.X)
            {
                int temp = a.X;
                a.X = b.X;
                b.X = temp;
            }
            if (a.Y > b.Y)
            {
                int temp = a.Y;
                a.Y = b.Y;
                b.Y = temp;
            }
            return new Rectangle(a.X, a.Y, b.X - a.X, b.Y - a.Y);
        }

        /// <summary>
        /// Cho biết điểm p có phải là điểm điều khiển hay là không
        /// </summary>
        /// <param name="p">Điểm cần xét</param>
        /// <returns></returns>
        public virtual int isHitControlsPoint(Point p)
        {
            List<Point> points = FindRegion.getControlPoints(this);
            for (int i = 0; i < 8; i++)
            {
                GraphicsPath path = new GraphicsPath();
                path.AddRectangle(new Rectangle(points[i].X - 4, points[i].Y - 4, 8, 8));

                if (path.IsVisible(p)) return i;
            }
            return -1;
        }

        /// <summary>
        /// Phương thức thay đổi lại điểm đầu và cuối của hình vẽ theo điểm điều khiển
        /// </summary>
        /// <param name="index">Điểm điều khiển</param>
        public virtual void changePoint(int index)
        {
            if (index == 0 || index == 1 || index == 3)
            {
                Point point = pointHead;
                pointHead = pointTail;
                pointTail = point;
            }
            if (index == 2)
            {
                int a = pointTail.X;
                int b = pointHead.Y;
                pointHead = new Point(pointHead.X, pointTail.Y);
                pointTail = new Point(a, b);
            }
            if (index == 5)
            {
                int a = pointHead.X;
                int b = pointTail.Y;
                pointHead = new Point(pointTail.X, pointHead.Y);
                pointTail = new Point(a, b);
            }
        }

        /// <summary>
        /// Phương thức di resize hình theo điểm điều khiển
        /// </summary>
        /// <param name="pointCurrent">Vị trí cần di chuyển tới</param>
        /// <param name="previous">Vị trí trước đó</param>
        /// <param name="index">Điểm điều khiển</param>
        public virtual void moveControlPoint(Point pointCurrent, Point previous, int index)
        {
            int deltaX = pointCurrent.X - previous.X;
            int deltaY = pointCurrent.Y - previous.Y;           
            if (index == 1 || index == 6)
            {
                pointTail = new Point(pointTail.X, pointTail.Y + deltaY);
            }
            else if (index == 3 || index == 4)
            {
                pointTail = new Point(pointTail.X + deltaX, pointTail.Y);
            }
            else
            {
                pointTail = pointCurrent;
            }
        }
    }
}
