package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.tableViewStart;

import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.scene.control.TableCell;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;
import lombok.RequiredArgsConstructor;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.ElementDatabaseView;

import java.util.List;

/**
 * Данный класс реализует паттерн строитель, используя библиотеку Lombok
 * Здесь как раз реализуется само добавление в таблицу из базы данных.
 */
@RequiredArgsConstructor
public class TableViewManager implements ElementDatabaseView {



    @FXML private final TableView<PersonInfo> customersTableView;
    @FXML private final TableColumn<PersonInfo, String> surnameColumn, nameColumn, patronymicColumn;
    @FXML private final TableColumn<PersonInfo, Image> planColumn, pactColumn;

    private final ObservableList<PersonInfo> personInfos;

    private enum IMAGES {
        ;
        private static final Image WORD_PNG = new Image("/projectFiles/images/file-extension.png");
        private static final Image RVT_JPG = new Image("/projectFiles/images/file.png");
    }

    /**
     * Метод для загрузки данных из базы данных и установки их в таблицу.
     */
    @Override
    public void event() {

        // Установка значений для столбцов таблицы
        surnameColumn.setCellValueFactory(new PropertyValueFactory<>("lastName"));
        nameColumn.setCellValueFactory(new PropertyValueFactory<>("firstName"));
        patronymicColumn.setCellValueFactory(new PropertyValueFactory<>("patronymic"));

        // Установка изображений для столбцов таблицы
        planColumn.setCellFactory(column -> createImageCell(personInfos, IMAGES.RVT_JPG));
        pactColumn.setCellFactory(column -> createImageCell(personInfos, IMAGES.WORD_PNG));

        // Установка данных в таблицу
        customersTableView.setItems(personInfos);
    }

    /**
     * Метод для создания ячейки с изображением.
     *
     * @param personInfos Список информации о людях.
     * @param image Изображение для отображения в ячейке.
     * @return TableCell - ячейка таблицы с изображением.
     */
    private TableCell<PersonInfo, Image> createImageCell(List<PersonInfo> personInfos,
                                                         Image image) {
        return new TableCell<>() {
            private final ImageView imageView = new ImageView();

            @Override
            protected void updateItem(Image item, boolean empty) {
                super.updateItem(item, empty);
                if (empty || getIndex() >= personInfos.size()) {

                    setGraphic(null);

                } else {

                    imageView.setImage(image);
                    imageView.setFitHeight(50);
                    imageView.setFitWidth(50);
                    setGraphic(imageView);

                }
            }
        };
    }

}
