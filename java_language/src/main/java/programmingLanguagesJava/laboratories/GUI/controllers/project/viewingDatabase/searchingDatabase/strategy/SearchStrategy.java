package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.searchingDatabase.strategy;

import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;

/**
 * Интерфейс SearchStrategy определяет общий метод для всех стратегий поиска.
 */
public interface SearchStrategy {

    /**
     * Метод matches определяет, соответствует ли информация о человеке заданному ключевому слову.
     *
     * @param personInfo Информация о человеке, которую нужно проверить.
     * @param keyword Ключевое слово, используемое для поиска.
     * @return Возвращает true, если информация о человеке соответствует ключевому слову. В противном случае возвращает false.
     */
    boolean matches(PersonInfo personInfo, String keyword);
}
