package programmingLanguagesJava.laboratories.fourthLaboratory.classes;

import org.jetbrains.annotations.NotNull;

import java.util.Comparator;

public class Book implements Comparator<Book>, Comparable<Book> {
    private final String name;
    private final String author;
    private final Integer year;

    public Book(String name, String author, int year) {
        this.name = name;
        this.author = author;
        this.year = year;
    }

    @Override
    public String toString() {
        return String.format("(%s, %s, %d)" ,name, author, year);
    }

    @Override
    public int compare(Book o1, Book o2) {
        int nameComparison = o1.name.compareTo(o2.name);
        if (nameComparison !=  0) {
            return nameComparison;
        }

        int authorComparison = o1.author.compareTo(o2.author);
        if (authorComparison !=  0) {
            return authorComparison;
        }

        return o1.year.compareTo(o2.year);
    }

    @Override
    public int compareTo(@NotNull Book o) {
        return this.compare(this, o);
    }
}
