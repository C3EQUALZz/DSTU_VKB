package programmingLanguagesJava.laboratories.fourthLaboratory.classes;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.stream.IntStream;

public class ListMerger {
    public static List<Integer> mergeSortedLists(List<Integer> list1, List<Integer> list2) {

        List<Integer> mergedList = new LinkedList<>();
        int i = 0, j = 0;

        while (i < list1.size() && j < list2.size()) {
            if (list1.get(i) <= list2.get(j)) {
                mergedList.add(list1.get(i++));
            } else {
                mergedList.add(list2.get(j++));
            }
        }

        while (i < list1.size()) {
            mergedList.add(list1.get(i++));
        }

        while (j < list2.size()) {
            mergedList.add(list2.get(j++));
        }

        return mergedList;
    }

    public static List<Integer> parser(String listString) {
        List<Integer> result = new ArrayList<>();

        String[] parts = listString.replaceAll("[{}]", "").split(",\\s*");

        IntStream.range(0, parts.length).forEach(i -> result.add(Integer.parseInt(parts[i])));

        return result;

    }
}
