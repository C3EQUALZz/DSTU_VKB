package programmingLanguagesJava.lections.xmlParse.fileInteraction;

import org.w3c.dom.Document;
import org.xml.sax.SAXException;
import programmingLanguagesJava.lections.xmlParse.DAO.Students;

import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import java.io.File;
import java.io.IOException;


/**
 * Класс, который является реализацией XML парсера. Здесь считывается документ, который потом в дальнейшем обрабатывается.
 */
public class XMLParser implements Parser {


    /**
     * Считывание файла
     * @param file экземпляр класса java.io.File для xml обработки
     * @return возвращает Document - интерфейс для работы с XML в нашем случае
     */
    private Document toDocument(File file) {
        try {
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            return builder.parse(file);
        } catch (ParserConfigurationException | SAXException | IOException e) {
            throw new RuntimeException("Не удалось обработать XML файл", e);
        }
    }

    /**
     * Обработка документа, здесь метод возвращает список студентов.
     * @param file XML файл, который нужно обработать
     * @return List с студентами
     */
    @Override
    public Students parse(File file) {
        var document = this.toDocument(file);

        try {
            var jaxbContext = JAXBContext.newInstance(Students.class);
            var jaxbUnmarshaller = jaxbContext.createUnmarshaller();
            return (Students) jaxbUnmarshaller.unmarshal(document);

        } catch (JAXBException e) {
            throw new RuntimeException("Нет студентов", e);
        }

    }
}
