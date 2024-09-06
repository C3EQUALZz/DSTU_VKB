using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Drawing;
using System.Windows.Forms;

using DoAnPaint.Model;
using DoAnPaint.Utils;
using DoAnPaint.View;


/*
 * Created by Nguyen Hoang Thinh 17110372 at 19/04/2019
 */
namespace DoAnPaint.Presenter.Alter
{
    class PresenterAlterImp : IPresenterAlter
    {
        IViewPaint viewPaint;

        DataManager dataManager;

        public PresenterAlterImp(IViewPaint viewPaint)
        {
            this.viewPaint = viewPaint;
            dataManager = DataManager.getInstance();
        }

        public void OnClickDrawGroup()
        {
            //TODO: tìm ra những hình được chọn, đếm số lượng lớn hơn 1 thì nhóm lại với nhau
            if (dataManager.ShapeList.Count(shape => shape.isSelected) > 1)
            {
                GroupShape group = new GroupShape();
                for (int i = 0; i < dataManager.ShapeList.Count; i++)
                {
                    if (dataManager.ShapeList[i].isSelected)
                    {
                        group.addShape(dataManager.ShapeList[i]);
                        dataManager.ShapeList.RemoveAt(i--);
                    }
                }
                FindRegion.SetPointHeadTail(group);
                group.isSelected = true;
                dataManager.ShapeList.Add(group);
                viewPaint.RefreshDrawing();
            }
        }

        public void OnClickDrawUnGroup()
        {
            //TODO: tìm ra những hình được chọn mà là hình GroupShape
            if (dataManager.ShapeList.Find(shape => shape.isSelected) is GroupShape)
            {
                GroupShape group = (GroupShape)dataManager.ShapeList.Find(shape => shape.isSelected);
                foreach (Shape shape in group)
                {
                    dataManager.ShapeList.Add(shape);
                }
                dataManager.ShapeList.Remove(group);
            }

            viewPaint.RefreshDrawing();
        }

        public void OnClickDeleteShape()
        {
            for (int i = 0; i < dataManager.ShapeList.Count; i++)
            {
                if (dataManager.ShapeList[i].isSelected)
                {
                    dataManager.ShapeList.RemoveAt(i--);
                }
            }
            viewPaint.RefreshDrawing();
        }

        public void OnClickClearAll(PictureBox picturebox)
        {
            picturebox.Image = null;
            dataManager.ShapeList.Clear();
            dataManager.IsNotNone = false;
            viewPaint.RefreshDrawing();
        }

        public void OnClickSaveImage(PictureBox picturebox)
        {
            SaveFileDialog saveFile = new SaveFileDialog();
            Bitmap bitmap = new Bitmap(picturebox.Width, picturebox.Height);
            Rectangle rect = new Rectangle(0, 0, picturebox.Width, picturebox.Height);
            picturebox.DrawToBitmap(bitmap, rect);
            saveFile.Filter = "Image Files(*.png;*.jpg; *.jpeg; *.gif; *.bmp)|*.png;*.jpg; *.jpeg; *.gif; *.bmp";
            saveFile.CheckPathExists = true;
            saveFile.OverwritePrompt = true;
            if (saveFile.ShowDialog() == DialogResult.OK)
            {
                bitmap.Save(saveFile.FileName);
                dataManager.IsSave = true;
            }
        }

        public void OnClickOpenImage(PictureBox picturebox)
        {
            OpenFileDialog openFile = new OpenFileDialog();
            openFile.Filter = "Image Files(*.png;*.jpg; *.jpeg; *.gif; *.bmp)|*.png;*.jpg; *.jpeg; *.gif; *.bmp";
            openFile.CheckFileExists = true;
            openFile.CheckPathExists = true;
            if (openFile.ShowDialog() == DialogResult.OK)
            {
                picturebox.Image = new Bitmap(openFile.FileName);
            }
        }

        public void OnClickNewImage(PictureBox picturebox)
        {

            if (dataManager.IsNotNone)
            {
                if (MessageBox.Show("You have not saved this image. Do you want to save it ?",
                     "Notification",
                     MessageBoxButtons.YesNo,
                     MessageBoxIcon.Question) == DialogResult.Yes)
                {
                    OnClickSaveImage(picturebox);
                }
            }
            OnClickClearAll(picturebox);
        }

        public void OnClickShutdown(PictureBox picturebox)
        {
            if (!dataManager.IsSave)
            {
                if (MessageBox.Show("You have not saved this image. Do you want to save it ?",
                     "Notification",
                     MessageBoxButtons.YesNo,
                     MessageBoxIcon.Question) == DialogResult.Yes)
                {
                    OnClickSaveImage(picturebox);
                }
            }
            Application.Exit();
        }

        public void OnUseKeyStrokes(PictureBox picturebox, Keys key)
        {
            if (key == Keys.A && Control.ModifierKeys.HasFlag(Keys.Control))
            {
                for (int i = 0; i < dataManager.ShapeList.Count; ++i)
                    dataManager.ShapeList[i].isSelected = true;
                viewPaint.RefreshDrawing();
            }
            if (key == Keys.Delete)
            {
                OnClickClearAll(picturebox);
            }
        }
    }
}
