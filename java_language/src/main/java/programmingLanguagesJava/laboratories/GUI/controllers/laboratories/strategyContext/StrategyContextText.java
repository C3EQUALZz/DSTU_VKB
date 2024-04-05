package programmingLanguagesJava.laboratories.GUI.controllers.laboratories.strategyContext;

import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;

/**
 * Класс, который объединяет элементы с текстом в одну общую сущность
 *
 * @param inputArgs место, в которое мы вводим данные для задания
 * @param condition место, в котором отображается условие
 * @param output    место, в котором отображается результат задания
 */

public record StrategyContextText(TextField inputArgs, TextArea condition, TextArea output) {}