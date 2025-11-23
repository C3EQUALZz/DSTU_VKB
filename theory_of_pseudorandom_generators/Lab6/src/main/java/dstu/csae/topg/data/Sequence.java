package dstu.csae.topg.data;

import lombok.AllArgsConstructor;
import lombok.Getter;

import java.util.ArrayList;
import java.util.Collection;

@Getter
public class Sequence extends ArrayList<Integer> {

    private String title;

    public Sequence(int initialCapacity, String title) {
        super(initialCapacity);
        this.title = title;
    }

    public Sequence(String title) {
        super();
        this.title = title;
    }

    public Sequence(Collection<? extends Integer> c, String title) {
        super(c);
        this.title = title;
    }
}
