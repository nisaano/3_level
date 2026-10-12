class MinHeap:
    #бинарная min-heap: значение родителя <= значений потомков

    def __init__(self):
        self.data = []  # элементы кучи хранятся в обычном списке

    @staticmethod
    def parent(i):
        #индекс родителя для узла i
        return (i - 1) // 2

    @staticmethod
    def left(i):
        #индекс левого потомка для узла i
        return 2 * i + 1

    @staticmethod
    def right(i):
        #индекс правого потомка для узла i
        return 2 * i + 2

    def __repr__(self):
        return f"MinHeap({self.data})"
    
#задание 8

    def _sift_up(self, index): #Поднять элемент с индексом index вверх, пока он меньше родителя
        while index > 0:
            parent = self.parent(index)
            if self.data[parent] <= self.data[index]:
                break   # свойство кучи восстановлено
            # меняет местами
            self.data[parent], self.data[index] = self.data[index], self.data[parent]
            index = parent

    def push(self, value): #Добавляет значение в кучу
        self.data.append(value)          # 1) кладёт в конец
        self._sift_up(len(self.data) - 1)  # 2) просеивает вверх


#задание 9
    def _sift_down(self, index): #Опускает элемент с индексом index вниз, пока он больше любого потомка
        n = len(self.data)
        while True:
            left = self.left(index)
            right = self.right(index)
            smallest = index

            # ищет наименьшего из трёх: текущий, левый, правый
            if left < n and self.data[left] < self.data[smallest]:
                smallest = left
            if right < n and self.data[right] < self.data[smallest]:
                smallest = right

            if smallest == index:
                break   # свойство кучи восстановлено

            # меняет с наименьшим потомком
            self.data[index], self.data[smallest] = (
                self.data[smallest], self.data[index]
            )
            index = smallest

    def pop(self): # Извлекает минимальный элемент (корень) из кучи
        if not self.data:
            return None

        root = self.data[0]              # запоминает минимум

        last = self.data.pop()           # забирает последний
        if self.data:                    # если ещё что-то осталось
            self.data[0] = last          # ставит его в корень
            self._sift_down(0)           # просеивает вниз

        return root
    
    