using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Windows.Forms;

using DoAnPaint.View;
using DoAnPaint.Utils;
using DoAnPaint.Model;


/*
 * Created by Nguyen Hoang Thinh 17110372 at 19/04/2019
 */
namespace DoAnPaint.Presenter
{
    class PresenterDrawImp : IPresenterDraw
    {
        IViewPaint viewPaint;

        DataManager dataManager;

        public PresenterDrawImp(IViewPaint viewPaint)
        {
            this.viewPaint = viewPaint;
            dataManager = DataManager.getInstance();
        }

        public void OnClickMouseDown(Point p)
        {
            dataManager.IsSave = false;
            dataManager.IsNotNone = true;
            if (dataManager.CurrentShape.Equals(CurrentShapeStatus.Void))
            {
                if (!(Control.ModifierKeys == Keys.Control))
                    dataManager.OffAllShapeSelected();
                viewPaint.RefreshDrawing();
                handleClickToSelect(p);
            }
            else
            {
                handleClickToDraw(p);
            }
        }

        public void handleClickToSelect(Point p)
        {
            for (int i = 0; i < dataManager.ShapeList.Count; ++i)
            {
                if (!(dataManager.ShapeList[i] is MPen))
                    dataManager.PointToResize = dataManager.ShapeList[i].isHitControlsPoint(p);
                if (dataManager.PointToResize != -1)
                {
                    dataManager.ShapeList[i].changePoint(dataManager.PointToResize);
                    dataManager.ShapeToMove = dataManager.ShapeList[i];
                    break;
                }
                else if (dataManager.ShapeList[i].isHit(p))
                {
                    dataManager.ShapeToMove = dataManager.ShapeList[i];
                    dataManager.ShapeList[i].isSelected = true;
                    if (dataManager.ShapeList[i] is MPen)
                    {
                        if (((MPen)dataManager.ShapeList[i]).isEraser)
                        {
                            dataManager.ShapeList[i].isSelected = false;
                            dataManager.ShapeToMove = null;
                        }
                    }
                    break;
                }
            }

            if (dataManager.PointToResize != -1)
            {
                dataManager.CursorCurrent = p;
            }
            else if (dataManager.ShapeToMove != null)
            {
                dataManager.IsMovingShape = true;
                dataManager.CursorCurrent = p;
            }
            else
            {
                dataManager.IsMovingMouse = true;
                dataManager.rectangleRegion = new Rectangle(p, new Size(0, 0));
            }
        }

        private void handleClickToDraw(Point p)
        {
            dataManager.IsMouseDown = true;
            dataManager.OffAllShapeSelected();
            if (dataManager.CurrentShape.Equals(CurrentShapeStatus.Line))
            {
                dataManager.AddEntity(new MLine
                {
                    pointHead = p,
                    pointTail = p,
                    contourWidth = dataManager.LineSize,
                    color = dataManager.ColorCurrent,
                    isFill = dataManager.IsFill
                });
            }
            else if (dataManager.CurrentShape.Equals(CurrentShapeStatus.Rectangle))
            {
                dataManager.AddEntity(new MRectangle
                {
                    pointHead = p,
                    pointTail = p,
                    contourWidth = dataManager.LineSize,
                    color = dataManager.ColorCurrent,
                    isFill = dataManager.IsFill
                });
            }
            else if (dataManager.CurrentShape.Equals(CurrentShapeStatus.Ellipse))
            {
                dataManager.AddEntity(new MEllipse
                {
                    pointHead = p,
                    pointTail = p,
                    contourWidth = dataManager.LineSize,
                    color = dataManager.ColorCurrent,
                    isFill = dataManager.IsFill
                });
            }

            else if (dataManager.CurrentShape.Equals(CurrentShapeStatus.Curve))
            {
                if (!dataManager.IsDrawingCurve)
                {
                    dataManager.IsDrawingCurve = true;
                    MCurve bezier = new MCurve
                    {
                        color = dataManager.ColorCurrent,
                        contourWidth = dataManager.LineSize,
                        isFill = dataManager.IsFill
                    };
                    bezier.points.Add(p);
                    bezier.points.Add(p);
                    dataManager.ShapeList.Add(bezier);
                }
                else
                {
                    MCurve bezier = dataManager.ShapeList[dataManager.ShapeList.Count - 1] as MCurve;
                    bezier.points[bezier.points.Count - 1] = p;
                    bezier.points.Add(p);
                }
                dataManager.IsMouseDown = false;
            }
            else if (dataManager.CurrentShape.Equals(CurrentShapeStatus.Polygon))
            {
                if (!dataManager.IsDrawingPolygon)
                {
                    dataManager.IsDrawingPolygon = true;
                    MPolygon polygon = new MPolygon
                    {
                        color = dataManager.ColorCurrent,
                        contourWidth = dataManager.LineSize,
                        isFill = dataManager.IsFill

                    };
                    polygon.points.Add(p);
                    polygon.points.Add(p);
                    dataManager.ShapeList.Add(polygon);
                }
                else
                {
                    MPolygon polygon = dataManager.ShapeList[dataManager.ShapeList.Count - 1] as MPolygon;
                    polygon.points[polygon.points.Count - 1] = p;
                    polygon.points.Add(p);
                }
                dataManager.IsMouseDown = false;
            }
            else if (dataManager.CurrentShape.Equals(CurrentShapeStatus.Pen))
            {
                dataManager.IsDrawingPen = true;
                MPen pen = new MPen
                {
                    color = dataManager.ColorCurrent,
                    contourWidth = dataManager.LineSize,
                    isFill = dataManager.IsFill
                };
                pen.points.Add(p);
                pen.points.Add(p);
                dataManager.ShapeList.Add(pen);
            }
            else if (dataManager.CurrentShape.Equals(CurrentShapeStatus.Eraser))
            {
                dataManager.IsDrawingEraser = true;
                MPen pen = new MPen
                {
                    color = Color.White,
                    contourWidth = dataManager.LineSize
                };
                pen.isEraser = true;
                pen.points.Add(p);
                pen.points.Add(p);
                dataManager.ShapeList.Add(pen);
            }
        }

        public void OnClickMouseMove(Point p)
        {
            if (dataManager.IsMouseDown)
            {
                dataManager.UpdatePointTail(p);
                viewPaint.RefreshDrawing();
            }
            else if (dataManager.PointToResize != -1)
            {
                if (!(dataManager.ShapeToMove is GroupShape) && !(dataManager.ShapeToMove is MPen))
                {
                    viewPaint.MovingControlPoint(dataManager.ShapeToMove,
                        p, dataManager.CursorCurrent,
                        dataManager.PointToResize);
                    dataManager.CursorCurrent = p;
                }

            }
            else if (dataManager.IsMovingShape)
            {
                viewPaint.MovingShape(dataManager.ShapeToMove, dataManager.DistanceXY(dataManager.CursorCurrent, p));
                dataManager.CursorCurrent = p;
            }
            else if (dataManager.CurrentShape.Equals(CurrentShapeStatus.Void))
            {
                if (dataManager.IsMovingMouse)
                {
                    dataManager.UpdateRectangleRegion(p);
                    viewPaint.RefreshDrawing();
                }
                else
                {

                    //TODO: Kiếm tra xem trong danh sách tồn tại hình nào chứa điểm p không
                    if (dataManager.ShapeList.Exists(shape => isInside(shape, p)))
                    {
                        viewPaint.SetCursor(Cursors.SizeAll);
                    }
                    else
                    {
                        viewPaint.SetCursor(Cursors.Default);
                    }

                }
            }

            if (dataManager.IsDrawingCurve)
            {
                MCurve bezier = dataManager.ShapeList[dataManager.ShapeList.Count - 1] as MCurve;
                bezier.points[bezier.points.Count - 1] = p;
                viewPaint.RefreshDrawing();
            }
            else if (dataManager.IsDrawingPolygon)
            {
                MPolygon polygon = dataManager.ShapeList[dataManager.ShapeList.Count - 1] as MPolygon;
                polygon.points[polygon.points.Count - 1] = p;
                viewPaint.RefreshDrawing();
            }
            else if (dataManager.IsDrawingPen)
            {
                MPen pen = dataManager.ShapeList[dataManager.ShapeList.Count - 1] as MPen;
                pen.points.Add(p);
                FindRegion.SetPointHeadTail(pen);
                viewPaint.RefreshDrawing();
            }
            else if (dataManager.IsDrawingEraser)
            {
                MPen pen = dataManager.ShapeList[dataManager.ShapeList.Count - 1] as MPen;
                pen.points.Add(p);
                FindRegion.SetPointHeadTail(pen);
                viewPaint.RefreshDrawing();
            }
        }

        private bool isInside(Shape shape, Point p)
        {
            if (shape is MPen)
            {
                MPen pen = shape as MPen;
                if (pen.isEraser) return false;
                return true;
            }
            return shape.isHit(p);
        }

        public void OnClickMouseUp()
        {
            dataManager.IsMouseDown = false;
            if (dataManager.PointToResize != -1)
            {
                dataManager.PointToResize = -1;
                dataManager.ShapeToMove = null;
            }
            else if (dataManager.IsMovingShape)
            {
                dataManager.IsMovingShape = false;
                dataManager.ShapeToMove = null;
            }
            else if (dataManager.IsMovingMouse)
            {
                dataManager.IsMovingMouse = false;
                dataManager.OffAllShapeSelected();

                //TODO: kiểm tra khi kéo chuột chọn một vùng thì có hình nào tồn tại bên
                //trong hay là không, nếu có thì hình đó được chọn
                for (int i = 0; i < dataManager.ShapeList.Count; ++i)
                {
                    if (dataManager.ShapeList[i].isInRegion(dataManager.rectangleRegion))
                    {
                        dataManager.ShapeList[i].isSelected = true;
                    }
                    if (dataManager.ShapeList[i] is MPen)
                    {
                        MPen pen = dataManager.ShapeList[i] as MPen;
                        if (pen.isEraser)
                            dataManager.ShapeList[i].isSelected = false;
                    }
                }
                viewPaint.RefreshDrawing();
            }
            if (dataManager.IsDrawingPen)
            {
                dataManager.IsDrawingPen = false;
            }
            else if (dataManager.IsDrawingEraser)
            {
                dataManager.IsDrawingEraser = false;
            }
        }

        public void GetDrawing(Graphics g)
        {
            dataManager.ShapeList.ForEach(shape =>
            {
                viewPaint.SetDrawing(shape, g);
                if (shape.isSelected)
                {
                    drawRegionForShape(shape, g);
                }

            });
            if (dataManager.IsMovingMouse)
            {
                using (Pen pen = new Pen(Color.DarkBlue, 1)
                {
                    DashPattern = new float[] { 3, 3, 3, 3 },
                    DashStyle = DashStyle.Custom
                })
                {
                    viewPaint.SetDrawingRegionRectangle(pen, dataManager.rectangleRegion, g);
                }

            }
            if (dataManager.PointToResize != -1)
            {
                if (dataManager.ShapeToMove is GroupShape) return;
                drawRegionForShape(dataManager.ShapeToMove, g);
            }
        }

        private void drawRegionForShape(Shape shape, Graphics g)
        {
            if (shape is MLine)
            {
                viewPaint.SetDrawingLineSelected(shape, new SolidBrush(Color.DarkBlue), g);

            }
            else if (shape is MPen)
            {
                if (!((MPen)shape).isEraser)
                {
                    using (Pen pen = new Pen(Color.DarkBlue, 1)
                    {
                        DashPattern = new float[] { 3, 3, 3, 3 },
                        DashStyle = DashStyle.Custom
                    })
                    {
                        viewPaint.SetDrawingRegionRectangle(pen, shape.getRectangle(), g);
                    }
                }
            }
            else if (shape is MCurve)
            {
                MCurve curve = (MCurve)shape;
                for (int i = 0; i < curve.points.Count; i++)
                {
                    viewPaint.SetDrawingCurveSelected(curve.points, new SolidBrush(Color.DarkBlue), g);
                }
            }
            else if (shape is MPolygon)
            {
                MPolygon polygon = (MPolygon)shape;
                for (int i = 0; i < polygon.points.Count; i++)
                {
                    viewPaint.SetDrawingCurveSelected(polygon.points, new SolidBrush(Color.DarkBlue), g);
                }
            }
            else
            {
                using (Pen pen = new Pen(Color.DarkBlue, 1)
                {
                    DashPattern = new float[] { 3, 3, 3, 3 },
                    DashStyle = DashStyle.Custom
                })
                {
                    viewPaint.SetDrawingRegionRectangle(pen, shape.getRectangle(shape.pointHead, shape.pointTail), g);
                    viewPaint.SetDrawingCurveSelected(FindRegion.GetControlPoints(shape),
                        new SolidBrush(Color.DarkBlue), g);
                }
            }
        }

        public void OnClickDrawLine()
        {
            setDefaultToDraw();
            dataManager.CurrentShape = CurrentShapeStatus.Line;
        }

        public void OnClickDrawRectangle()
        {
            setDefaultToDraw();
            dataManager.CurrentShape = CurrentShapeStatus.Rectangle;
        }

        public void OnClickDrawEllipse()
        {
            setDefaultToDraw();
            dataManager.CurrentShape = CurrentShapeStatus.Ellipse;
        }

        public void OnClickDrawBezier()
        {
            setDefaultToDraw();
            dataManager.CurrentShape = CurrentShapeStatus.Curve;
        }

        public void OnClickDrawPolygon()
        {
            setDefaultToDraw();
            dataManager.CurrentShape = CurrentShapeStatus.Polygon;
        }

        public void OnClickDrawPen()
        {
            setDefaultToDraw();
            dataManager.CurrentShape = CurrentShapeStatus.Pen;
        }

        public void OnClickDrawEraser()
        {
            setDefaultToDraw();
            dataManager.CurrentShape = CurrentShapeStatus.Eraser;
        }

        public void OnClickStopDrawing(MouseButtons mouse)
        {
            if (mouse == MouseButtons.Right)
            {
                if (dataManager.CurrentShape.Equals(CurrentShapeStatus.Polygon))
                {
                    MPolygon polygon = dataManager.ShapeList[dataManager.ShapeList.Count - 1] as MPolygon;
                    polygon.points.Remove(polygon.points[polygon.points.Count - 1]);
                    dataManager.IsDrawingPolygon = false;
                    FindRegion.SetPointHeadTail(polygon);
                }
                else if (dataManager.CurrentShape.Equals(CurrentShapeStatus.Curve))
                {
                    MCurve curve = dataManager.ShapeList[dataManager.ShapeList.Count - 1] as MCurve;
                    curve.points.Remove(curve.points[curve.points.Count - 1]);
                    dataManager.IsDrawingCurve = false;
                    FindRegion.SetPointHeadTail(curve);
                }
            }
        }

        private void setDefaultToDraw()
        {
            dataManager.OffAllShapeSelected();
            viewPaint.RefreshDrawing();
            viewPaint.SetCursor(Cursors.Default);
        }

    }
}
