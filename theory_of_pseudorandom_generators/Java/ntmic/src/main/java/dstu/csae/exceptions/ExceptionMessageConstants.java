package dstu.csae.exceptions;

public interface ExceptionMessageConstants {
    String COMPARISON_IS_NOT_SOLVABLE = "Сравнение %s нерешаемо, так как НОД(%d, %d) не делит %d";
    String DIOPHANTINE_EQUATION_IS_NOT_SOLVABLE = "Дафантовое уравнение %s не решаемо, так как НОД(%d, %d) не делит %d";
    String NO_INVERSE_ELEM = "Обратного элемента для числа %d в поле %d не существует";
    String INVALID_ARGUMENTS_MESSAGE = "Заданы неверные аргументы. Повторите попытку";
    String NO_SOLUTION_MESSAGE = "%s не имеет решений";
    String ATTEMPT_DIVIDE_BY_ZERO = "Попытка деления на 0";
    String LAST_FRACTION_DENOMINATOR_IS_ZERO = "Знаменатель последнего коэффициента равен 0";
    String INDEX_OUT_OF_BOUNDS = "Индекс выходит за границы допустимых значений";
}
