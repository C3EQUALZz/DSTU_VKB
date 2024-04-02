package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.searchingDatabase.strategy;

import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;

/**
 * Класс LastNameSearchStrategy реализует интерфейс SearchStrategy и предоставляет стратегию поиска по фамилии.
 */
public class LastNameSearchStrategy implements SearchStrategy {

    /**
     * Метод matches проверяет, соответствует ли информация о человеке заданному ключевому слову.
     * Он сравнивает фамилию человека (в нижнем регистре) с ключевым словом (также в нижнем регистре).
     *
     * @param personInfo Информация о человеке, которую нужно проверить.
     * @param keyword Ключевое слово, используемое для поиска.
     * @return Возвращает true, если фамилия человека содержит ключевое слово. В противном случае возвращает false.
     */
    @Override
    public boolean matches(PersonInfo personInfo, String keyword) {
        return personInfo.getLastName().toLowerCase().contains(keyword.toLowerCase());
    }
}
