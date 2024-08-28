using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Drawing;
using System.Windows.Forms;

using DoAnPaint.Model;
using DoAnPaint.Utils;


/*
 * Created by Nguyen Hoang Thinh 17110372 at 19/04/2019
 */
namespace DoAnPaint.View
{
    /// <summary>
    /// Interface update giao diện
    /// </summary>
    interface ViewPaint
    {
        /// <summary>
        /// Gọi vẽ lại bản vẽ
        /// </summary>
        void refreshDrawing();

        /// <summary>
        /// Thiết lập hình dạng cho con trỏ chuột
        /// </summary>
        /// <param name="cursor">Hình dạng</param>
        void setCursor(Cursor cursor);

        /// <summary>
        /// Thiết lập màu sắc cho bachground
        /// </summary>
        /// <param name="color">Màu sắc</param>
        void setColor(Color color);

        /// <summary>
        /// Thiết lập hình nền cho button
        /// </summary>
        /// <param name="btn">Button cần thay đổi nền</param>
        /// <param name="color">Màu sắc</param>
        void setColor(Button btn, Color color);

        /// <summary>
        /// Phương thức vẽ một hình lên graphics
        /// </summary>
        /// <param name="shape">Hình cần vẽ</param>
        /// <param name="g">graphics</param>
        void setDrawing(Shape shape, Graphics g);

        /// <summary>
        /// Phương thức vẽ điểm điều khiển cho đường thẳng
        /// </summary>
        /// <param name="shape">Hình cần vẽ điểm điều khiển</param>
        /// <param name="brush"></param>
        /// <param name="g"></param>
        void setDrawingLineSelected(Shape shape, Brush brush,Graphics g);

        /// <summary>
        /// Phương thức vẽ điểm điều khiển cho đường cong
        /// </summary>
        /// <param name="points"></param>
        /// <param name="brush"></param>
        /// <param name="g"></param>
        void setDrawingCurveSelected(List<Point> points, Brush brush, Graphics g);

        /// <summary>
        /// Phương thức vẽ điểm điều khiển cho hình vẽ bởi pen
        /// </summary>
        /// <param name="p"></param>
        /// <param name="rectangle"></param>
        /// <param name="g"></param>
        void setDrawingRegionRectangle(Pen p, Rectangle rectangle, Graphics g);

        /// <summary>
        /// Phương thức di chuyển một hình
        /// </summary>
        /// <param name="shape">Hình cần di chuyển</param>
        /// <param name="distance">Khoảng cách</param>
        void movingShape(Shape shape, Point distance);

        /// <summary>
        /// Phương thức resize một hình theo điểm điều khiển
        /// </summary>
        /// <param name="shape">Hình cần resize</param>
        /// <param name="pointCurrent">Vị trí cần thay đổi</param>
        /// <param name="previous">Vị trí trước đó</param>
        /// <param name="indexPoint">Điểm điều khiển</param>
        void movingControlPoint(Shape shape, Point pointCurrent, Point previous, int indexPoint);
    }
}
