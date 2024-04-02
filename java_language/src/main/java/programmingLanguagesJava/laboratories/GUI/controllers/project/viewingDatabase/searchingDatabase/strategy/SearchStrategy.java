package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.searchingDatabase.strategy;

import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;

public interface SearchStrategy {
    boolean matches(PersonInfo personInfo, String keyword);
}
