package programmingLanguagesJava.laboratories.thirdLaboratory;

class Student {

    private final String surname;
    private final String grade;
    private final String lesson;

    Student(String surname, String grade, String lesson) {
        this.surname = surname.substring(0, 15);
        this.grade = grade.substring(0, 3);
        this.lesson = lesson.substring(0, 10);
    }

    @Override
    public String toString() {
        return String.format("Студент %s получил %s по %s", this.surname, this.grade, this.lesson);
    }
}
