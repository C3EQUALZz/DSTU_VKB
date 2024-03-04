package programmingLanguagesJava.lections.fifthLection;

import java.util.Arrays;

class ArrayOfObjects {
    public static void main(String[] args) {
        Book[] shelf = new Book[3];
        shelf[0] = new Book("RED");
        shelf[1] = new Book("BLUE");
        shelf[2] = new Book("PURPLE");
        System.out.println(Arrays.toString(shelf));
    }
}
