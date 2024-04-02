package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.searchingDatabase.strategy;

import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;

public class FirstNameSearchStrategy implements SearchStrategy {
    @Override
    public boolean matches(PersonInfo personInfo, String keyword) {
        return personInfo.getFirstName().toLowerCase().contains(keyword.toLowerCase());
    }
}
