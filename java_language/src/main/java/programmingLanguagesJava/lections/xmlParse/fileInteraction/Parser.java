package programmingLanguagesJava.lections.xmlParse.fileInteraction;

import programmingLanguagesJava.lections.xmlParse.DAO.Students;

import java.io.File;

public interface Parser {
    Students parse(File file);
}
