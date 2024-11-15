"""
9. Как изменить размер цветовой панели Matplotlib в Python?
"""
import matplotlib.pyplot as plt
import numpy as np

# Создание графика
data = np.random.rand(10, 10)
plt.imshow(data, cmap='viridis')

# Добавление цветовой панели с настраиваемым размером
colorbar = plt.colorbar(pad=0.1)  # Настраиваем размер с помощью параметра pad

# Отображение графика
plt.show()