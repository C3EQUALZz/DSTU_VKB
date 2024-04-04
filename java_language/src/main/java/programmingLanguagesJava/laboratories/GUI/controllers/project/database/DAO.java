/**
 * Данный интерфейс нужен для взаимодействия с БД
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.database;

public interface DAO {
    void addAddress(String address);
    void addFullName(String fullName);
    void addMainPerson(String person);
    void addBuildingPlan(String pathToBuildingPlan);
    void addAllResponsiblePeople(String persons);
    void addContractDocument(String pathToDocument);

    String getAddress();
    String getFullName();
    String getMainPerson();
    String getBuildingPlan();
    String getAllResponsiblePeople();
    String getContractDocument();
}
