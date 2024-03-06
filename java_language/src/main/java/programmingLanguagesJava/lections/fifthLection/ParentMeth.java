package programmingLanguagesJava.lections.fifthLection;

public class ParentMeth {
    public static void main(String[] args) {
        var ch = new ChildMeth();
        ch.PrintStr();
    }

    public void PrintStr() {
        System.out.println("Parent class");
    }
}

class ChildMeth extends ParentMeth {
    @Override
    public void PrintStr() {
        super.PrintStr();
        System.out.println("Child class");
    }
}
