package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.searchingDatabase.strategy;

import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;

public class LastNameSearchStrategy implements SearchStrategy {
    @Override
    public boolean matches(PersonInfo personInfo, String keyword) {
        return personInfo.getLastName().toLowerCase().contains(keyword.toLowerCase());
    }
}
