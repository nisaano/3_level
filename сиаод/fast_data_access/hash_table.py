class HashTable:

    def __init__(self, size=10):
        self.size = size
        self.buckets = [[] for _ in range(size)]
        self.count = 0

    def _index(self, key): # индекс корзины hash(key) % size
        return hash(key) % self.size

    def set(self, key, value): # добавление новой пары или обновить существующую
        idx = self._index(key)
        for i, (k, v) in enumerate(self.buckets[idx]):
            if k == key:
                self.buckets[idx][i] = (key, value)   # обновление
                return
        self.buckets[idx].append((key, value))        # вставка
        self.count += 1

    def get(self, key): # возврат значение по ключу или None
        idx = self._index(key)
        for k, v in self.buckets[idx]:
            if k == key:
                return v
        return None

    def remove(self, key): # удаление пары по ключу
        idx = self._index(key)
        for i, (k, v) in enumerate(self.buckets[idx]):
            if k == key:
                del self.buckets[idx][i]
                self.count -= 1
                return True
        return False

    def __repr__(self): #
        lines = [f"HashTable(size={self.size}, count={self.count})"]
        for i, bucket in enumerate(self.buckets):
            if bucket:
                lines.append(f"  bucket[{i}]: {bucket}")
        return "\n".join(lines)
    
#задание 6
    @property
    def load_factor(self): #Коэффициент заполнения
        return self.count / self.size

#Сколько элементов размещено в корзинах СВЕРХ первого
    def collision_count(self):
        return sum(max(0, len(bucket) - 1) for bucket in self.buckets)

    def max_chain_length(self): #Максимальная длина цепочки (сколько элементов в самой длинной корзине)
        return max((len(bucket) for bucket in self.buckets), default=0)
    

    