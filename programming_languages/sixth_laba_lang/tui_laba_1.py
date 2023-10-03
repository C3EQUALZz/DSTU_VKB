from programming_languages.first_laba_lang.tutor import interact_with_user as interact_with_user_1
from programming_languages.second_laba_lang.main import main as main_2
from programming_languages.third_laba_lang.main import main as main_3
from programming_languages.fourth_laba_lang.main import main as main_4
from programming_languages.fifth_laba_lang.main import main as main_5


def interact_with_user():
    match input("Выберите лабораторную работу "):
        case "1":
            interact_with_user_1()
        case "2":
            main_2()
        case "3":
            main_3()
        case "4":
            main_4()
        case "5":
            main_5()
        case _:
            print("Вы ввели неправильный номер ")


if __name__ == "__main__":
    interact_with_user()
