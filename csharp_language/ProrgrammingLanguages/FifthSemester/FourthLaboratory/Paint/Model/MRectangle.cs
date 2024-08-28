using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Windows.Forms;

using DoAnPaint.Utils;


/*
 * Created by Nguyen Hoang Thinh 17110372 at 19/04/2019
 */
namespace DoAnPaint.Model
{
    /// <summary>
    /// Lớp dại diện cho hình chữ nhật
    /// </summary>
    public class MRectangle:Shape
    {       
        public MRectangle()
        {
            name = "Rectangle";
        }

        public MRectangle(Color color)
        {
            name = "Rectangle";
            this.color = color;
        }

        public override object Clone()
        {
            return new MRectangle
            {
                pointHead = pointHead,
                pointTail = pointTail,
                contourWidth = contourWidth,
                isSelected = isSelected,
                color = color,
                name = name
            };
        }

        public override void drawShape(System.Drawing.Graphics g)
        {
            using (GraphicsPath path = graphicsPath)
            {
                if (isFill)
                {
                    using (Brush b = new SolidBrush(color))
                    {
                        g.FillPath(b, path);
                    }
                }
                else
                {
                    using (Pen p = new Pen(color, contourWidth))
                    {
                        g.DrawPath(p, path);
                    }
                }
            }
        }

        public override bool isHit(System.Drawing.Point p)
        {
            bool inside = false;
            using (GraphicsPath path = graphicsPath)
            {
                if (isFill)
                {
                    inside = path.IsVisible(p);                  
                }
                else
                {
                    using (Pen pen = new Pen(color, contourWidth+3))
                    {
                        inside = path.IsOutlineVisible(p, pen);
                    }
                }
            }

            return inside;
        }
        
        protected override GraphicsPath graphicsPath
        {
            get
            {
                GraphicsPath path = new GraphicsPath();

                if (pointTail.X < pointHead.X && pointTail.Y < pointHead.Y)
                {
                    path.AddRectangle(new System.Drawing.Rectangle(pointTail,
                        new Size(pointHead.X - pointTail.X, pointHead.Y - pointTail.Y)));
                }
                else if (pointHead.X > pointTail.X && pointHead.Y < pointTail.Y)
                {
                    path.AddRectangle(new System.Drawing.Rectangle(new Point(pointTail.X, pointHead.Y), 
                        new Size(pointHead.X - pointTail.X, pointTail.Y - pointHead.Y)));
                }
                else if (pointHead.X < pointTail.X && pointHead.Y > pointTail.Y)
                {
                    path.AddRectangle(new System.Drawing.Rectangle(new Point(pointHead.X, pointTail.Y), 
                        new Size(pointTail.X - pointHead.X, pointHead.Y - pointTail.Y)));
                }
                else
                {
                    path.AddRectangle(new System.Drawing.Rectangle(pointHead, 
                        new Size(pointTail.X - pointHead.X, pointTail.Y - pointHead.Y)));
                }

                return path;
            }
        }
       
        
    }
}
