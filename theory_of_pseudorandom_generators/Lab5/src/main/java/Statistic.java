import javax.swing.*;
import java.awt.*;

public class Statistic extends JFrame{

    public Statistic(JComponent component){
        super();
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
        setTitle("Статистика");
        setSize(640, 480);
        setLayout(new BorderLayout());
        getContentPane().add(new JScrollPane(component), BorderLayout.CENTER);
        setVisible(true);
    }


}
