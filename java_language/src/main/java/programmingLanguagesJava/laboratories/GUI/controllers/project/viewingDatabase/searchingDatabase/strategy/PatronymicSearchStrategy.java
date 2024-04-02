package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.searchingDatabase.strategy;

import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;

public class PatronymicSearchStrategy implements SearchStrategy {
    @Override
    public boolean matches(PersonInfo personInfo, String keyword) {
        return personInfo.getPatronymic().toLowerCase().contains(keyword.toLowerCase());
    }
}
