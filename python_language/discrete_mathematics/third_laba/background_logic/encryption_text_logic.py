"""
В этом файле осуществляется логика шифрования текста

"""
from ..config import BLOCK_SIZE, IV, KEY


def byte_enc_block(block: bytes):
    """
    Здесь запускается логика шифрования с использованием кубика Рубика
    """
    c = Cube(block)
    c.scramble(KEY)
    return c.get_block_bytes()


def xor_block_key(block_input: bytes, cypher_text: bytes) -> bytes:
    """
    Является вспомогательной функцией, которая делает шифрование между блоком данных ввода и шифр текстом.
    Каждый раз шифр текст у нас обновляется после взаимодействия с кубиком Рубика.
    :param block_input: Очередной блок с размером 54 символа, который мы шифруем.
    :param cypher_text: Шифрованный block_input[index - 1] на прошлом раунде.
    :return:
    """
    return bytes([b ^ k for b, k in zip(block_input, cypher_text)])


def byte_encryption_text(string_input: str) -> str:
    """
    Здесь происходит запуск функций для обработки данных.
    :param string_input: Входная строка от пользователя, которую он ввел.
    :return: Возвращает набор байт - зашифрованный текст
    """
    # Проверяется, кратна ли длина данных (data) размеру блока (BLOCK_SIZE).
    # Если нет, то к данным добавляются символы '#' до тех пор,
    # пока длина данных не станет кратной размеру блока.
    bytes_string = string_input.encode()
    padded_data: bytes = (bytes_string + (len(bytes_string) % BLOCK_SIZE == 0) *
                          (b"#" * (BLOCK_SIZE - len(bytes_string) % BLOCK_SIZE)))

    # Разделение данных на блоки размером BLOCK_SIZE
    blocks: list[bytes] = [padded_data[i:i + BLOCK_SIZE] for i in range(0, len(padded_data), BLOCK_SIZE)]

    # Создание списка cipher_blocks, начиная с IV (вектора инициализации) и пустых списков для каждого блока данных.
    cipher_blocks: list[bytes] = [IV]

    for index, plain_block in enumerate(blocks):
        # Выполняет операцию XOR между текущим блоком данных и предыдущим блоком шифр текста
        # (или IV, если это первая итерация).
        xor_block = xor_block_key(plain_block, cipher_blocks[index])
        # Полученный результат отправляется на шифрование с помощью вращений кубика Рубика
        # Зашифрованный блок после кубика добавляется, как шифр текст
        cipher_blocks.append(byte_enc_block(xor_block))

    return "".join(map(lambda x: x.decode(), cipher_blocks[1:]))
