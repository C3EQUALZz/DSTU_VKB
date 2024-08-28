using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Drawing.Drawing2D;
using System.Windows.Forms;


/*
 * Created by Nguyen Hoang Thinh 17110372 at 19/04/2019
 */
namespace DoAnPaint.Presenter.Alter
{
    /// <summary>
    /// Interface cập nhật ứng dụng từ yêu cầu người dùng
    /// </summary>
    interface PresenterAlter
    {
        /// <summary>
        /// Phương thức group một hình 
        /// </summary>
        void onClickDrawGroup();

        /// <summary>
        /// Phương thức ungroup một hình 
        /// </summary>
        void onClickDrawUnGroup();

        /// <summary>
        /// Phương thức xóa một hình 
        /// </summary>
        void onClickDeleteShape();

        /// <summary>
        /// Phương thức xóa tất cả các hình
        /// </summary>
        /// <param name="picturebox"><Picturebox cần xóa/param>
        void onClickClearAll(PictureBox picturebox);

        /// <summary>
        /// Phương thức lưu một hình
        /// </summary>
        /// <param name="picturebox"><Picturebox cần lưu/param>
        void onClickSaveImage(PictureBox picturebox);

        /// <summary>
        /// Phương thức mở một hình lên picturebox
        /// </summary>
        /// <param name="picturebox"><Picturebox cần xóa/param>
        void onClickOpenImage(PictureBox picturebox);

        /// <summary>
        /// Phương thức tạo một hình vẽ mới từ picturebox
        /// </summary>
        /// <param name="picturebox"><Picturebox cần xóa/param>
        void onClickNewImage(PictureBox picturebox);

        /// <summary>
        /// Phương thức gọi tắt ứng dụng từ picturebox
        /// </summary>
        /// <param name="picturebox"><Picturebox cần xóa/param>
        void onClickShutdown(PictureBox picturebox);

        /// <summary>
        /// Phương thức xử lý nhấn tổ hợp phím trên picturebox
        /// </summary>
        /// <param name="picturebox"><Picturebox cần xóa/param>
        void onUseKeyStrokes(PictureBox picturebox, Keys key);

    }
}
