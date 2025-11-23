package dstu.csae.exceptions;

public interface ExceptionMessageConstants {
    String EMPTY_COEFFICIENTS = "Невозможно инициализировать полином из пустых коэффициентов";
    String POLYNOMIAL_IS_NULL = "Полином не задан";
    String POLYNOMIAL_INDEX_OUT_OF_BOUNDS = "В полиноме %s нет монома степени %d";
    String POLYNOMIAL_DIVIDE_BY_ZERO = "Невозможно выполнить деление на полином %s";
    String POLYNOMIAL_IS_REDUCIBLE = "Полином %s является приводимым над полем %s";
    String POLYNOMIAL_IS_NOT_NORMALIZED = "Полином %s не нормирован над полем %s";
    String DIVIDE_BY_ZERO = "Ошибка деления на 0";
    String NUMBER_DIVIDE_BY_ZERO = "Попытка деления числа %d на 0";
    String NUMBER_IS_NOT_PRIME = "Число %d не является простым";
    String FIELD_IS_NULL = "Поле не задано";
    String REVERSE_ELEMENT_DOES_NOT_EXIST = "Обратный элемент для элемента %s не существует";
}
