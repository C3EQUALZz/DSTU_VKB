import lombok.NonNull;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.NumberAxis;
import org.jfree.chart.block.BlockBorder;
import org.jfree.chart.plot.CategoryPlot;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.renderer.category.BarRenderer;
import org.jfree.chart.title.TextTitle;
import org.jfree.data.category.DefaultCategoryDataset;
import org.jfree.data.category.SlidingCategoryDataset;
import org.jfree.ui.RectangleInsets;

import javax.swing.*;
import java.awt.*;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Objects;

public class StatsGenerator {

    public static SlidingCategoryDataset getDataSet(
            @NonNull ArrayList<Long> data){
        DefaultCategoryDataset dataset = new DefaultCategoryDataset();
        HashSet<Long> unique = new HashSet<>(data);
        unique.stream()
                .sorted()
                .forEach(x -> {
                    double count = data.stream()
                            .filter(y -> Objects.equals(x, y))
                            .count();
                    dataset.addValue(count, "", String.valueOf(x));
                 });
        return new SlidingCategoryDataset(dataset, 0, 200);
    }

    public static JFreeChart getJFreeChart(String title,
                                    String xTitle,
                                    String yTitle,
                                    String subTitle,
                                    SlidingCategoryDataset dataset){
        JFreeChart chart = ChartFactory.createBarChart(
                title,
                xTitle,
                yTitle,
                dataset,
                PlotOrientation.VERTICAL,
                true,
                true,
                false
        );
        chart.addSubtitle(new TextTitle(subTitle));
        chart.setBackgroundPaint(Color.white);
        CategoryPlot plot = (CategoryPlot) chart.getPlot();
        NumberAxis rangeAxis = (NumberAxis) plot.getRangeAxis();
        rangeAxis.setStandardTickUnits(NumberAxis.createIntegerTickUnits());
        BarRenderer renderer = (BarRenderer)plot.getRenderer();
        renderer.setDrawBarOutline(true);
        renderer.setSeriesPaint(0, Color.BLUE);
        renderer.setItemMargin(0.2);
        chart.getLegend().setFrame(BlockBorder.NONE);
        return chart;
    }

    public static JPanel getPanel(JFreeChart chart){
        chart.setPadding(new RectangleInsets(4, 8, 4, 2));
        ChartPanel panel = new ChartPanel(chart);
        panel.setFillZoomRectangle(true);
        panel.setMouseWheelEnabled(true);
        panel.setPreferredSize(new Dimension(600, 300));
        return panel;
    }

}
