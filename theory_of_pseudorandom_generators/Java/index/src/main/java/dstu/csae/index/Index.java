package dstu.csae.index;



import dstu.csae.constants.AlphabetConstants;

import java.util.TreeMap;

public class Index implements AlphabetConstants {
    private static final TreeMap<Character, Character> SUPERSCRIPT_ALPHABET = new TreeMap<>();
    private static final TreeMap<Character, Character> SUBSCRIPT_ALPHABET = new TreeMap<>();

    static {
        for (int i = 0; i < ALPHABET.length(); i++) {
            SUPERSCRIPT_ALPHABET.put(ALPHABET.charAt(i), AlphabetConstants.SUPERSCRIPT_ALPHABET.charAt(i));
            SUBSCRIPT_ALPHABET.put(ALPHABET.charAt(i), AlphabetConstants.SUBSCRIPT_ALPHABET.charAt(i));
        }
    }

    public static String toSuperscript(String text) {
        return convert(text, SUPERSCRIPT_ALPHABET);
    }

    public static String toSubscript(String text) {
        return convert(text, SUBSCRIPT_ALPHABET);
    }

    private static String convert(String text, TreeMap<Character, Character> alphabet) {
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < text.length(); i++) {
            char ch = ' ';
            if (alphabet.containsKey(text.charAt(i))) {
                ch = alphabet.get(text.charAt(i));
            }
            builder.append(ch);
        }
        return builder.toString();
    }


    public static void main(String[] args) {
        System.out.println("12345678");
        System.out.println(Index.toSuperscript("12345678"));
        System.out.println(Index.toSubscript("12345678"));
    }
}