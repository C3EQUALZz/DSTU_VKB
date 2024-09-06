using System.Drawing;
using System.Windows.Forms;
using DoAnPaint.View;
using DoAnPaint.Utils;
using DoAnPaint.Model;

namespace DoAnPaint.Presenter.Updates
{
    class PresenterUpdateImp : IPresenterUpdate
    {
        private readonly IViewPaint viewPaint;
        private readonly DataManager dataManager;

        public PresenterUpdateImp(IViewPaint viewPaint)
        {
            this.viewPaint = viewPaint;
            dataManager = DataManager.getInstance();
        }

        public void OnClickSelectMode()
        {
            dataManager.OffAllShapeSelected();
            viewPaint.RefreshDrawing();
            dataManager.CurrentShape = CurrentShapeStatus.Void;
            viewPaint.SetCursor(Cursors.Default);
        }

        public void OnClickSelectColor(Color color, Graphics g)
        {
            dataManager.ColorCurrent = color;
            viewPaint.SetColor(color);
            foreach (Shape item in dataManager.ShapeList)
            {
                if (item.isSelected)
                {
                    item.color = color;
                    viewPaint.SetDrawing(item, g);
                }
            }
        }

        public void OnClickSelectSize(int size)
        {
            dataManager.LineSize = size;
        }

        public void OnClickSelectFill(Button btn, Graphics g)
        {
            dataManager.IsFill = !dataManager.IsFill;
            if (btn.BackColor.Equals(Color.LightCyan))
                viewPaint.SetColor(btn, SystemColors.Control);
            else
                viewPaint.SetColor(btn, Color.LightCyan);
        }

    }
}
