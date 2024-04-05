/**
 * Контроллер, который отвечает за окно с лабораторными работами.
 * Не совсем хорошо написан, можно было использовать паттерн наблюдатель, но я не хочу исправлять сильно.
 */

package programmingLanguagesJava.laboratories.GUI.controllers.laboratories;

import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.scene.layout.AnchorPane;
import programmingLanguagesJava.laboratories.GUI.controllers.BaseController;
import programmingLanguagesJava.laboratories.GUI.controllers.laboratories.strategy.*;
import programmingLanguagesJava.laboratories.GUI.controllers.laboratories.strategyContext.StrategyContextCombobox;
import programmingLanguagesJava.laboratories.GUI.controllers.laboratories.strategyContext.StrategyContextText;

import java.net.URL;
import java.util.ResourceBundle;
import java.util.stream.Stream;

public class Laboratories extends BaseController {

    @FXML
    private Button clearInput, startQuestion;
    @FXML
    private Button zeroButton, firstButton, firstDotFirstButton, secondButton, thirdButton, thirdDotFirstButton, fourthButton;
    @FXML
    private Label openSlider, closeSlider;
    @FXML
    private AnchorPane slider;
    @FXML
    private ComboBox<String> combobox;
    @FXML
    private TextArea condition, output;
    @FXML
    private TextField inputArgs;

    /**
     * Инициализация контроллера для окна с лабораторными работами
     */
    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        super.initialize(url, resourceBundle);

        var strategyContextCombobox = new StrategyContextCombobox(combobox);
        var strategyContextText = new StrategyContextText(inputArgs, condition, output);

        var buttonStream = Stream.of(
                zeroButton,
                firstButton,
                firstDotFirstButton,
                secondButton,
                thirdButton,
                thirdDotFirstButton,
                fourthButton
        );

        Stream.of(

                new SliderActionLaboratories(openSlider, closeSlider, slider),
                new ComboboxActionLaboratories(strategyContextCombobox, condition),
                new ButtonLabsActionLaboratories(strategyContextCombobox, buttonStream),
                new ClearButtonActionLaboratories(strategyContextText, clearInput),
                new StartQuestionActionLaboratories(strategyContextCombobox, strategyContextText, startQuestion)

        ).parallel().forEach(ActionLaboratories::execute);

    }


}
