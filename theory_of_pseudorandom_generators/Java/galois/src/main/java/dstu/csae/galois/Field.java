package dstu.csae.galois;

import lombok.NonNull;

public interface Field<T> {

    int getCharacteristic();

    T findFirstPrimitive();

    T add(@NonNull T first,
            @NonNull T second);

    T subtract(@NonNull T reduced,
               @NonNull T subtracted);

    T multiply(@NonNull T first,
               @NonNull T second);

    T divide(@NonNull T divisible,
             @NonNull T divisor);

    T zero();

    T one();
}
