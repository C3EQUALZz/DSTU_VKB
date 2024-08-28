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
    class PresenterDrawImp : PresenterDraw
    {
        ViewPaint viewPaint;

        DataManager dataManager;

        public PresenterDrawImp(ViewPaint viewPaint)
        {
            this.viewPaint = viewPaint;
            dataManager = DataManager.getInstance();
        }

        public void onClickMouseDown(Point p)
        {
            dataManager.isSave = false;
            dataManager.isNotNone = true;
            if (dataManager.currentShape.Equals(CurrentShapeStatus.Void))
            {
                if (!(Control.ModifierKeys == Keys.Control))
                    dataManager.offAllShapeSelected();
                viewPaint.refreshDrawing();
                handleClickToSelect(p);
            }
            else
            {
                handleClickToDraw(p);
            }
        }

        public void handleClickToSelect(Point p)
        {
            for (int i = 0; i < dataManager.shapeList.Count; ++i)
            {
                if (!(dataManager.shapeList[i] is MPen))
                    dataManager.pointToResize = dataManager.shapeList[i].isHitControlsPoint(p);
                if (dataManager.pointToResize != -1)
                {
                    dataManager.shapeList[i].changePoint(dataManager.pointToResize);
                    dataManager.shapeToMove = dataManager.shapeList[i];
                    break;
                }
                else if (dataManager.shapeList[i].isHit(p))
                {
                    dataManager.shapeToMove = dataManager.shapeList[i];
                    dataManager.shapeList[i].isSelected = true;
                    if (dataManager.shapeList[i] is MPen)
                    {
                        if (((MPen)dataManager.shapeList[i]).isEraser)
                        {
                            dataManager.shapeList[i].isSelected = false;
                            dataManager.shapeToMove = null;
                        }
                    }
                    break;
                }
            }

            if (dataManager.pointToResize != -1)
            {
                dataManager.cursorCurrent = p;
            }
            else if (dataManager.shapeToMove != null)
            {
                dataManager.isMovingShape = true;
                dataManager.cursorCurrent = p;
            }
            else
            {
                dataManager.isMovingMouse = true;
                dataManager.rectangleRegion = new Rectangle(p, new Size(0, 0));
            }
        }

        private void handleClickToDraw(Point p)
        {
            dataManager.isMouseDown = true;
            dataManager.offAllShapeSelected();
            if (dataManager.currentShape.Equals(CurrentShapeStatus.Line))
            {
                dataManager.addEntity(new MLine
                {
                    pointHead = p,
                    pointTail = p,
                    contourWidth = dataManager.lineSize,
                    color = dataManager.colorCurrent,
                    isFill = dataManager.isFill
                });
            }
            else if (dataManager.currentShape.Equals(CurrentShapeStatus.Rectangle))
            {
                dataManager.addEntity(new MRectangle
                {
                    pointHead = p,
                    pointTail = p,
                    contourWidth = dataManager.lineSize,
                    color = dataManager.colorCurrent,
                    isFill = dataManager.isFill
                });
            }
            else if (dataManager.currentShape.Equals(CurrentShapeStatus.Ellipse))
            {
                dataManager.addEntity(new MEllipse
                {
                    pointHead = p,
                    pointTail = p,
                    contourWidth = dataManager.lineSize,
                    color = dataManager.colorCurrent,
                    isFill = dataManager.isFill
                });
            }

            else if (dataManager.currentShape.Equals(CurrentShapeStatus.Curve))
            {
                if (!dataManager.isDrawingCurve)
                {
                    dataManager.isDrawingCurve = true;
                    MCurve bezier = new MCurve
                    {
                        color = dataManager.colorCurrent,
                        contourWidth = dataManager.lineSize,
                        isFill = dataManager.isFill
                    };
                    bezier.points.Add(p);
                    bezier.points.Add(p);
                    dataManager.shapeList.Add(bezier);
                }
                else
                {
                    MCurve bezier = dataManager.shapeList[dataManager.shapeList.Count - 1] as MCurve;
                    bezier.points[bezier.points.Count - 1] = p;
                    bezier.points.Add(p);
                }
                dataManager.isMouseDown = false;
            }
            else if (dataManager.currentShape.Equals(CurrentShapeStatus.Polygon))
            {
                if (!dataManager.isDrawingPolygon)
                {
                    dataManager.isDrawingPolygon = true;
                    MPolygon polygon = new MPolygon
                    {
                        color = dataManager.colorCurrent,
                        contourWidth = dataManager.lineSize,
                        isFill = dataManager.isFill

                    };
                    polygon.points.Add(p);
                    polygon.points.Add(p);
                    dataManager.shapeList.Add(polygon);
                }
                else
                {
                    MPolygon polygon = dataManager.shapeList[dataManager.shapeList.Count - 1] as MPolygon;
                    polygon.points[polygon.points.Count - 1] = p;
                    polygon.points.Add(p);
                }
                dataManager.isMouseDown = false;
            }
            else if (dataManager.currentShape.Equals(CurrentShapeStatus.Pen))
            {
                dataManager.isDrawingPen = true;
                MPen pen = new MPen
                {
                    color = dataManager.colorCurrent,
                    contourWidth = dataManager.lineSize,
                    isFill = dataManager.isFill
                };
                pen.points.Add(p);
                pen.points.Add(p);
                dataManager.shapeList.Add(pen);
            }
            else if (dataManager.currentShape.Equals(CurrentShapeStatus.Eraser))
            {
                dataManager.isDrawingEraser = true;
                MPen pen = new MPen
                {
                    color = Color.White,
                    contourWidth = dataManager.lineSize
                };
                pen.isEraser = true;
                pen.points.Add(p);
                pen.points.Add(p);
                dataManager.shapeList.Add(pen);
            }
        }

        public void onClickMouseMove(Point p)
        {
            if (dataManager.isMouseDown)
            {
                dataManager.updatePointTail(p);
                viewPaint.refreshDrawing();
            }
            else if (dataManager.pointToResize != -1)
            {
                if (!(dataManager.shapeToMove is GroupShape) && !(dataManager.shapeToMove is MPen))
                {
                    viewPaint.movingControlPoint(dataManager.shapeToMove,
                        p, dataManager.cursorCurrent,
                        dataManager.pointToResize);
                    dataManager.cursorCurrent = p;
                }

            }
            else if (dataManager.isMovingShape)
            {
                viewPaint.movingShape(dataManager.shapeToMove, dataManager.distanceXY(dataManager.cursorCurrent, p));
                dataManager.cursorCurrent = p;
            }
            else if (dataManager.currentShape.Equals(CurrentShapeStatus.Void))
            {
                if (dataManager.isMovingMouse)
                {
                    dataManager.updateRectangleRegion(p);
                    viewPaint.refreshDrawing();
                }
                else
                {

                    //TODO: Kiếm tra xem trong danh sách tồn tại hình nào chứa điểm p không
                    if (dataManager.shapeList.Exists(shape => isInside(shape, p)))
                    {
                        viewPaint.setCursor(Cursors.SizeAll);
                    }
                    else
                    {
                        viewPaint.setCursor(Cursors.Default);
                    }

                }
            }

            if (dataManager.isDrawingCurve)
            {
                MCurve bezier = dataManager.shapeList[dataManager.shapeList.Count - 1] as MCurve;
                bezier.points[bezier.points.Count - 1] = p;
                viewPaint.refreshDrawing();
            }
            else if (dataManager.isDrawingPolygon)
            {
                MPolygon polygon = dataManager.shapeList[dataManager.shapeList.Count - 1] as MPolygon;
                polygon.points[polygon.points.Count - 1] = p;
                viewPaint.refreshDrawing();
            }
            else if (dataManager.isDrawingPen)
            {
                MPen pen = dataManager.shapeList[dataManager.shapeList.Count - 1] as MPen;
                pen.points.Add(p);
                FindRegion.setPointHeadTail(pen);
                viewPaint.refreshDrawing();
            }
            else if (dataManager.isDrawingEraser)
            {
                MPen pen = dataManager.shapeList[dataManager.shapeList.Count - 1] as MPen;
                pen.points.Add(p);
                FindRegion.setPointHeadTail(pen);
                viewPaint.refreshDrawing();
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

        public void onClickMouseUp()
        {
            dataManager.isMouseDown = false;
            if (dataManager.pointToResize != -1)
            {
                dataManager.pointToResize = -1;
                dataManager.shapeToMove = null;
            }
            else if (dataManager.isMovingShape)
            {
                dataManager.isMovingShape = false;
                dataManager.shapeToMove = null;
            }
            else if (dataManager.isMovingMouse)
            {
                dataManager.isMovingMouse = false;
                dataManager.offAllShapeSelected();

                //TODO: kiểm tra khi kéo chuột chọn một vùng thì có hình nào tồn tại bên
                //trong hay là không, nếu có thì hình đó được chọn
                for (int i = 0; i < dataManager.shapeList.Count; ++i)
                {
                    if (dataManager.shapeList[i].isInRegion(dataManager.rectangleRegion))
                    {
                        dataManager.shapeList[i].isSelected = true;
                    }
                    if (dataManager.shapeList[i] is MPen)
                    {
                        MPen pen = dataManager.shapeList[i] as MPen;
                        if (pen.isEraser)
                            dataManager.shapeList[i].isSelected = false;
                    }
                }
                viewPaint.refreshDrawing();
            }
            if (dataManager.isDrawingPen)
            {
                dataManager.isDrawingPen = false;
            }
            else if (dataManager.isDrawingEraser)
            {
                dataManager.isDrawingEraser = false;
            }
        }

        public void getDrawing(Graphics g)
        {
            dataManager.shapeList.ForEach(shape =>
            {
                viewPaint.setDrawing(shape, g);
                if (shape.isSelected)
                {
                    drawRegionForShape(shape, g);
                }

            });
            if (dataManager.isMovingMouse)
            {
                using (Pen pen = new Pen(Color.DarkBlue, 1)
                {
                    DashPattern = new float[] { 3, 3, 3, 3 },
                    DashStyle = DashStyle.Custom
                })
                {
                    viewPaint.setDrawingRegionRectangle(pen, dataManager.rectangleRegion, g);
                }

            }
            if (dataManager.pointToResize != -1)
            {
                if (dataManager.shapeToMove is GroupShape) return;
                drawRegionForShape(dataManager.shapeToMove, g);
            }
        }

        private void drawRegionForShape(Shape shape, Graphics g)
        {
            if (shape is MLine)
            {
                viewPaint.setDrawingLineSelected(shape, new SolidBrush(Color.DarkBlue), g);

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
                        viewPaint.setDrawingRegionRectangle(pen, shape.getRectangle(), g);
                    }
                }
            }
            else if (shape is MCurve)
            {
                MCurve curve = (MCurve)shape;
                for (int i = 0; i < curve.points.Count; i++)
                {
                    viewPaint.setDrawingCurveSelected(curve.points, new SolidBrush(Color.DarkBlue), g);
                }
            }
            else if (shape is MPolygon)
            {
                MPolygon polygon = (MPolygon)shape;
                for (int i = 0; i < polygon.points.Count; i++)
                {
                    viewPaint.setDrawingCurveSelected(polygon.points, new SolidBrush(Color.DarkBlue), g);
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
                    viewPaint.setDrawingRegionRectangle(pen, shape.getRectangle(shape.pointHead, shape.pointTail), g);
                    viewPaint.setDrawingCurveSelected(FindRegion.getControlPoints(shape),
                        new SolidBrush(Color.DarkBlue), g);
                }
            }
        }

        public void onClickDrawLine()
        {
            setDefaultToDraw();
            dataManager.currentShape = CurrentShapeStatus.Line;
        }

        public void onClickDrawRectangle()
        {
            setDefaultToDraw();
            dataManager.currentShape = CurrentShapeStatus.Rectangle;
        }

        public void onClickDrawEllipse()
        {
            setDefaultToDraw();
            dataManager.currentShape = CurrentShapeStatus.Ellipse;
        }

        public void onClickDrawBezier()
        {
            setDefaultToDraw();
            dataManager.currentShape = CurrentShapeStatus.Curve;
        }

        public void onClickDrawPolygon()
        {
            setDefaultToDraw();
            dataManager.currentShape = CurrentShapeStatus.Polygon;
        }

        public void onClickDrawPen()
        {
            setDefaultToDraw();
            dataManager.currentShape = CurrentShapeStatus.Pen;
        }

        public void onClickDrawEraser()
        {
            setDefaultToDraw();
            dataManager.currentShape = CurrentShapeStatus.Eraser;
        }

        public void onClickStopDrawing(MouseButtons mouse)
        {
            if (mouse == MouseButtons.Right)
            {
                if (dataManager.currentShape.Equals(CurrentShapeStatus.Polygon))
                {
                    MPolygon polygon = dataManager.shapeList[dataManager.shapeList.Count - 1] as MPolygon;
                    polygon.points.Remove(polygon.points[polygon.points.Count - 1]);
                    dataManager.isDrawingPolygon = false;
                    FindRegion.setPointHeadTail(polygon);
                }
                else if (dataManager.currentShape.Equals(CurrentShapeStatus.Curve))
                {
                    MCurve curve = dataManager.shapeList[dataManager.shapeList.Count - 1] as MCurve;
                    curve.points.Remove(curve.points[curve.points.Count - 1]);
                    dataManager.isDrawingCurve = false;
                    FindRegion.setPointHeadTail(curve);
                }
            }
        }

        private void setDefaultToDraw()
        {
            dataManager.offAllShapeSelected();
            viewPaint.refreshDrawing();
            viewPaint.setCursor(Cursors.Default);
        }

    }
}
