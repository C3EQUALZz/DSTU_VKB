using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Drawing;

using DoAnPaint.Model;
using DoAnPaint.Utils;


/*
 * Created by Nguyen Hoang Thinh 17110372 at 19/04/2019
 */
namespace DoAnPaint.Model
{
    /// <summary>
    /// Lớp quản lý các đối tượng hỗ trợ để vẽ hình
    /// </summary>
    public class DataManager
    {
        public static DataManager instance;

        //TODO: chứa danh sách các hình vẽ
        public List<Shape> shapeList { get; set; }

        //TODO: chứa hình được chọn hiện tại
        public Shape shapeToMove { get; set; }

        //TODO: vẽ vùng được chọn có kích thước như đối tượng này 
        public System.Drawing.Rectangle rectangleRegion;

        //TODO: thiết lập trạng thái click chuột xuống của người dùng
        public bool isMouseDown { get; set; }

        //TODO: thiết lập trạng thái di chuyển hình của người dùng
        public bool isMovingShape { get; set; }

        //TODO: thiết lập trạng thái di chuyển chuột của người dùng
        public bool isMovingMouse { get; set; }

        //TODO: thiết lập trạng thái cho biết có phải người dùng đang vẽ đường cong hay không
        public bool isDrawingCurve { get; set; }

        //TODO: thiết lập trạng thái cho biết có phải người dùng đang vẽ đa giác hay không
        public bool isDrawingPolygon { get; set; }

        //TODO: thiết lập trạng thái cho biết có phải người dùng đang vẽ pencil hay không
        public bool isDrawingPen { get; set; }

        //TODO: thiết lập trạng thái cho biết có phải người dùng đang chọn chế độ eraser hay không
        public bool isDrawingEraser { get; set; }

        //TODO: thiết lập trạng thái cho biết có phải người dùng đang chọn chế độ fill hay không
        public bool isFill { get; set; }

        //TODO: thiết lập trạng thái cho biết có phải người dùng đã lưu hình hay chưa
        public bool isSave{ get; set; }

        //TODO: thiết lập trạng thái cho biết có background hiện tại được vẽ hay là chưa
        public bool isNotNone{ get; set; }

        //TODO: thiết lập trạng thái cho biết có phải người dùng chọn tất cả các hình hay là không
        public bool isSelectAll { get; set; }

        //TODO: cho biết điểm điều khiển nào người dùng muốn resize kích thước
        public int pointToResize { get; set; }

        //TODO: cho biết trạng thái hình hiện tại là hình nào
        public CurrentShapeStatus currentShape { get; set; }

        //TODO: cho biết vị trí con trỏ chuột hiện tại
        public Point cursorCurrent { get; set; }

        //TODO: chứa danh sách các hình
        public Color colorCurrent { get; set; }

        //TODO: chứa danh sách các hình
        public int lineSize { get; set; }

        private DataManager()
        {
            shapeList = new List<Shape>();
            pointToResize = -1;
        }

        public static DataManager getInstance()
        {
            if (instance == null) instance = new DataManager();
            return instance;
        }

        /// <summary>
        /// Phương thức cập nhật điểm cuối của hình vẽ
        /// </summary>
        /// <param name="p">cập nhật điểm cuối = p</param>
        public void updatePointTail(Point p)
        {
            shapeList[shapeList.Count - 1].pointTail = p;
        }

        /// <summary>
        /// Thêm đối tượng line vào danh sách
        /// </summary>
        /// <param name="line">đối tượng line</param>
        public void addEntity(Shape shape)
        {
            shapeList.Add(shape);
        }

        /// <summary>
        /// Phương thức đặt trạng thái được chọn của tất cả các hình về false
        /// </summary>
        public void offAllShapeSelected()
        {
            shapeList.ForEach(shape => shape.isSelected = false);
        }

        /// <summary>
        /// Phương thức tính khoảng cách giữa điểm y và x
        /// </summary>
        /// <param name="x">điểm x</param>
        /// <param name="y">điểm y</param>
        /// <returns></returns>
        public Point distanceXY(Point x, Point y)
        {
            return new Point(y.X - x.X, y.Y - x.Y);
        }

        /// <summary>
        /// Phương thức cập nhật lại một vùng là hình chữ nhật bao quanh hình vẽ
        /// ở chế độ chọn hình
        /// </summary>
        /// <param name="p"></param>
        public void updateRectangleRegion(Point p)
        {         
            rectangleRegion.Width = p.X - rectangleRegion.X;
            rectangleRegion.Height = p.Y - rectangleRegion.Y;
        }
    }
}
