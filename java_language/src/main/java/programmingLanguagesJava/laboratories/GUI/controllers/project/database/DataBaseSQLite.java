package programmingLanguagesJava.laboratories.GUI.controllers.project.database;

public class DataBaseSQLite implements DAO {
    private static DataBaseSQLite instance;

    private DataBaseSQLite() {

    }

    public static synchronized DataBaseSQLite getInstance() {
        if (instance == null) {
            instance = new DataBaseSQLite();
        }

        return instance;
    }

    @Override
    public void addAddress(String address) {

    }

    @Override
    public void addFullName(String fullName) {

    }

    @Override
    public void addMainPerson(String person) {

    }

    @Override
    public void addBuildingPlan(String pathToBuildingPlan) {

    }

    @Override
    public void addAllResponsiblePeople(String persons) {

    }

    @Override
    public void addContractDocument(String pathToDocument) {

    }

    @Override
    public String getAddress() {
        return null;
    }

    @Override
    public String getFullName() {
        return null;
    }

    @Override
    public String getMainPerson() {
        return null;
    }

    @Override
    public String getBuildingPlan() {
        return null;
    }

    @Override
    public String getAllResponsiblePeople() {
        return null;
    }

    @Override
    public String getContractDocument() {
        return null;
    }
}
