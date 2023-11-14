from affine_cipher import Affine
from classic_ceasar import CaesarCipher
from key_caesar import CaesarWithWord


def clear_text_from_tabs(text: str) -> str:
    return "\n".join(line.lstrip() for line in text.split("\n"))


def ceaser_basically_interaction() -> None:
    word = input("Введите слово, которое вы хотите зашифровать ")
    cypher: CaesarCipher = CaesarCipher(int(input("Введите число шифрования - целое число ")))
    print(f"Результат шифрования - {(res := cypher.encode(word))}", f"Результат расшифровки: {cypher.decode(res)}")


def ceaser_word_interaction() -> None:
    word = input("Введите предложение, которое хотите зашифровать ")


def affine_interaction() -> None:
    word = input("Введите слово, которое вы хотите зашифровать ")
    tup: tuple[int, ...] = tuple(map(int, input("Введите два числовых ключа через пробел ").split()[:2]))
    affine = Affine(tup)
    print(f"Результат шифрования - {(res := affine.encrypt(word))}", f"Результат расшифровки {affine.decrypt(res)}")


def trisemus_interaction() -> None:
    word = input("Введите слово, которое вы хотите зашифровать ")


def main() -> None:
    input_str = clear_text_from_tabs("""
    Что вы хотите сделать?
    1. Система шифрования Цезаря классика; (1)
    2. Аффинная система подстановок Цезаря; (2)
    3. Система шифрования Цезаря с ключевым словом; (3) 
    4. Система шифрования Трисемуса; (4)
    
    """)
    match input(input_str).lower().strip():
        case "1" | "(1)" | "цезарь":
            ceaser_basically_interaction()
        case "2" | "(2)" | "афина":
            affine_interaction()
        case "3" | "(3)" | "цезарь с ключевым":
            ceaser_word_interaction()
        case "4" | "(4)" | "трисемус":
            trisemus_interaction()
        case _:
            print("Вы не выбрали нужное задание")


if __name__ == "__main__":
    main()
