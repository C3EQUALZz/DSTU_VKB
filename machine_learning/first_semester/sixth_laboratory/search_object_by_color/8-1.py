"""
Задание 8

1. Измените размер отображаемого кадра, используя функцию cv2.resize().
"""
import zipfile
from typing import Optional

import cv2
import numpy as np


def read_video_from_zip(zip_file_path: str, image_name: str) -> Optional[cv2.VideoCapture]:
    """Читает изображение из ZIP-файла.

    Args:
        zip_file_path (str): Путь к ZIP-файлу.
        image_name (str): Имя изображения внутри ZIP-файла.

    Returns:
        Optional[np.ndarray]: Декодированное изображение или None, если не удалось загрузить.
    """
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        with zip_ref.open(image_name) as file:
            video_data = file.read()
            video_array = np.frombuffer(video_data, np.uint8)
            res = cv2.VideoCapture(video_array, cv2.IMREAD_COLOR)
    return res


def process_video(video: cv2.VideoCapture) -> None:
    index = 0

    while video.isOpened():
        index += 1
        # получаем кадр из видеопотока файла
        # кадры по очереди считываются в переменную frame
        ret, frame = video.read()
        # если кадры закончились
        if frame is None:
            break  # прерываем работу цикла
        res = cv2.resize(frame, (int(frame.shape[1] / 2), int(frame.shape[0] / 2)), interpolation=cv2.INTER_AREA)
        cv2.imshow(f"Result {index}", res)
        # организуем выход из цикла по нажатию клавиши,
        # ждем 30 миллисекунд нажатия, записываем код нажатой клавиши
        key_press = cv2.waitKey(30)
        # если код нажатой клавиши совпадает с кодом «q»,
        if key_press == ord('q'):
            break  # то прервать цикл while
    # освобождаем память от переменной video
    video.release()
    # закрываем все окна opencv
    cv2.destroyAllWindows()


def main() -> None:
    zip_file_path = '../images_to_notebook.zip'
    image_name = 'DorZn.avi'
    image = read_video_from_zip(zip_file_path, image_name)
    process_video(image)


if __name__ == '__main__':
    main()
