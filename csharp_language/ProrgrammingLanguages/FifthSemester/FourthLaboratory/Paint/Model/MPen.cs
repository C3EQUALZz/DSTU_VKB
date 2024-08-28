using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Drawing;


/*
 * Created by Nguyen Hoang Thinh 17110372 at 19/04/2019
 */
namespace DoAnPaint.Model
{
    /// <summary>
    /// Lớp dại diện cho đường vẽ bằng pencil
    /// </summary>
    public class MPen:MCurve
    {
        //TODO: cho biết chọn chế độ xóa hay là không
        public bool isEraser { get; set; }

        public MPen()
        {
            name = "Pen";
        }

        public MPen(Color color)
        {
            name = "Pen";
            this.color = color;
        }

    }
}
