using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Drawing;
using System.Windows.Forms;

using DoAnPaint.Utils;
using DoAnPaint.Model;


/*
 * Created by Nguyen Hoang Thinh 17110372 at 19/04/2019
 */
namespace DoAnPaint.Presenter
{
    /// <summary>
    /// Interface xử lý yêu cầu thao tác dữ liệu từ người dùng
    /// </summary>
    interface PresenterDraw
    {
        /// <summary>
        /// Phương thức vẽ một hình lên graphic g
        /// </summary>
        /// <param name="g"></param>
        void getDrawing(Graphics g);

        /// <summary>
        /// Phương thức xử lý hạ chuột từ người dùng
        /// </summary>
        /// <param name="p"></param>
        void onClickMouseDown(Point p);

        /// <summary>
        /// Phương thức xử di chuyển chuột từ người dùng
        /// </summary>
        /// <param name="p"></param>
        void onClickMouseMove(Point p);

        /// <summary>
        /// Phương thức xử thả chuột từ người dùng
        /// </summary>
        void onClickMouseUp();

        /// <summary>
        /// Phương thức gọi vẽ đường thẳng
        /// </summary>
        void onClickDrawLine();

        /// <summary>
        /// Phương thức gọi vẽ hình chữ nhật
        /// </summary>
        void onClickDrawRectangle();

        /// <summary>
        /// Phương thức gọi vẽ hình ellipse
        /// </summary>
        void onClickDrawEllipse();

        /// <summary>
        /// Phương thức gọi vẽ đường cong
        /// </summary>
        void onClickDrawBezier();

        /// <summary>
        /// Phương thức gọi vẽ polygon
        /// </summary>
        void onClickDrawPolygon();

        /// <summary>
        /// Phương thức gọi vẽ pen
        /// </summary>
        void onClickDrawPen();

        /// <summary>
        /// Phương thức gọi vẽ xóa
        /// </summary>
        void onClickDrawEraser();

        /// <summary>
        /// Phương thức xử lý chuột phải từ người dùng
        /// </summary>
        /// <param name="mouse"></param>
        void onClickStopDrawing(MouseButtons mouse);

    }
}
