/**
 *
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.searchingDatabase.strategy;

import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;

/**
 * Класс FirstNameSearchStrategy реализует интерфейс SearchStrategy и предоставляет стратегию поиска по имени.
 */
public class FirstNameSearchStrategy implements SearchStrategy {

    /**
     * Метод matches проверяет, соответствует ли информация о человеке заданному ключевому слову.
     * Он сравнивает имя человека (в нижнем регистре) с ключевым словом (также в нижнем регистре).
     *
     * @param personInfo Информация о человеке, которую нужно проверить.
     * @param keyword Ключевое слово, используемое для поиска.
     * @return Возвращает true, если имя человека содержит ключевое слово. В противном случае возвращает false.
     */
    @Override
    public boolean matches(PersonInfo personInfo, String keyword) {
        return personInfo.getFirstName().toLowerCase().contains(keyword.toLowerCase());
    }
}
