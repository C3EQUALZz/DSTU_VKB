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
    class PresenterAlterImp : PresenterAlter
    {
        ViewPaint viewPaint;

        DataManager dataManager;

        public PresenterAlterImp(ViewPaint viewPaint)
        {
            this.viewPaint = viewPaint;
            dataManager = DataManager.getInstance();
        }

        public void onClickDrawGroup()
        {
            //TODO: tìm ra những hình được chọn, đếm số lượng lớn hơn 1 thì nhóm lại với nhau
            if (dataManager.shapeList.Count(shape => shape.isSelected) > 1)
            {
                GroupShape group = new GroupShape();
                for (int i = 0; i < dataManager.shapeList.Count; i++)
                {
                    if (dataManager.shapeList[i].isSelected)
                    {
                        group.addShape(dataManager.shapeList[i]);
                        dataManager.shapeList.RemoveAt(i--);
                    }
                }
                FindRegion.setPointHeadTail(group);
                group.isSelected = true;
                dataManager.shapeList.Add(group);
                viewPaint.refreshDrawing();
            }
        }

        public void onClickDrawUnGroup()
        {
            //TODO: tìm ra những hình được chọn mà là hình GroupShape
            if (dataManager.shapeList.Find(shape => shape.isSelected) is GroupShape)
            {
                GroupShape group = (GroupShape)dataManager.shapeList.Find(shape => shape.isSelected);
                foreach (Shape shape in group)
                {
                    dataManager.shapeList.Add(shape);
                }
                dataManager.shapeList.Remove(group);
            }

            viewPaint.refreshDrawing();
        }

        public void onClickDeleteShape()
        {
            for (int i = 0; i < dataManager.shapeList.Count; i++)
            {
                if (dataManager.shapeList[i].isSelected)
                {
                    dataManager.shapeList.RemoveAt(i--);
                }
            }
            viewPaint.refreshDrawing();
        }

        public void onClickClearAll(PictureBox picturebox)
        {
            picturebox.Image = null;
            dataManager.shapeList.Clear();
            dataManager.isNotNone = false;
            viewPaint.refreshDrawing();
        }

        public void onClickSaveImage(PictureBox picturebox)
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
                dataManager.isSave = true;
            }
        }

        public void onClickOpenImage(PictureBox picturebox)
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

        public void onClickNewImage(PictureBox picturebox)
        {

            if (dataManager.isNotNone)
            {
                if (MessageBox.Show("You have not saved this image. Do you want to save it ?",
                     "Notification",
                     MessageBoxButtons.YesNo,
                     MessageBoxIcon.Question) == DialogResult.Yes)
                {
                    onClickSaveImage(picturebox);
                }
            }
            onClickClearAll(picturebox);
        }

        public void onClickShutdown(PictureBox picturebox)
        {
            if (!dataManager.isSave)
            {
                if (MessageBox.Show("You have not saved this image. Do you want to save it ?",
                     "Notification",
                     MessageBoxButtons.YesNo,
                     MessageBoxIcon.Question) == DialogResult.Yes)
                {
                    onClickSaveImage(picturebox);
                }
            }
            Application.Exit();
        }

        public void onUseKeyStrokes(PictureBox picturebox, Keys key)
        {
            if (key == Keys.A && Control.ModifierKeys.HasFlag(Keys.Control))
            {
                for (int i = 0; i < dataManager.shapeList.Count; ++i)
                    dataManager.shapeList[i].isSelected = true;
                viewPaint.refreshDrawing();
            }
            if (key == Keys.Delete)
            {
                onClickClearAll(picturebox);
            }
        }
    }
}
