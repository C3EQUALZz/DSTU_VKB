/*
 * Точка запуска программы, здесь создаются окна нашего приложения (Scene) и происходит конфигурация приложения (Stage)
 */

package programmingLanguagesJava.laboratories.GUI;

import javafx.application.Application;
import javafx.stage.Stage;
import programmingLanguagesJava.laboratories.GUI.config.StageConfigurator;
import programmingLanguagesJava.laboratories.GUI.controllers.SceneController;
import programmingLanguagesJava.laboratories.GUI.controllers.project.fileObserver.FileWatcherService;

public class Main extends Application {

    /**
     * Данный класс является точкой входа в нашу программу, здесь происходит запуск приложения
     *
     * @param stage сущность нашего приложения.
     */
    @Override
    public void start(Stage stage) {

        var stageInitialized = StageConfigurator.configureStage(stage);

        SceneController.getInstance(stage).setStartMenu();

        stageInitialized.show();

        var consoleDemon = new FileWatcherService();
        consoleDemon.setDaemon(true);
        consoleDemon.start();

    }

}