import random
from hash_table import HashTable


#3. возвращает индекс первого найденного элемента или -1
def linear_search(numbers, target):
    for index, value in enumerate(numbers):
        if value == target:
            return index
    return -1

#5.Многократный замер: возвращает (результат, среднее время в секундах)
import time

def measure(func, *args, repeats=10):
    t0 = time.perf_counter()
    for _ in range(repeats):
        result = func(*args)
    t1 = time.perf_counter()
    return result, (t1 - t0) / repeats

#1. список из 100 000 случайных целых чисел
numbers = [random.randint(0, 1_000_000) for _ in range(100_000)]

print("list size:", len(numbers))
print("first 5 elements:", numbers[:5])
print("last 5  elements:", numbers[-5:])

#2. доступ к элементам по индексам
n = len(numbers)

print("\naccess by index")
print("start:  numbers[0]      =", numbers[0])
print("middle: numbers[n // 2] =", numbers[n // 2])
print("end:    numbers[n - 1]  =", numbers[n - 1])

#проверка линейного поиска
print("\nlinear search:")
print("  find numbers[0]:      index =", linear_search(numbers, numbers[0]))
print("  find numbers[n//2]:   index =", linear_search(numbers, numbers[n // 2]))
print("  find numbers[n-1]:    index =", linear_search(numbers, numbers[n - 1]))
print("  find missing (-1):    index =", linear_search(numbers, -1))

#6. замеры времени
print("\ntiming: index access")
for name, idx in [("start", 0), ("middle", n // 2), ("end", n - 1)]:
    _, t = measure(lambda i=idx: numbers[i], repeats=100_000)
    print(f"  {name:6s}: {t * 1e9:6.1f} ns")

print("\ntiming: linear search")
for name, target in [
    ("start",   numbers[0]),
    ("middle",  numbers[n // 2]),
    ("end",     numbers[-1]),
    ("missing", -1),
]:
    _, t = measure(linear_search, numbers, target, repeats=10)
    print(f"  {name:8s}: {t * 1e3:7.3f} ms")

#задание 3
#1. список из 10 000 записей (id, value)
records = [(i, f"value_{i}") for i in range(10_000)]
print("records count:", len(records))
print("first 3:", records[:3])

#2. поиск по id перебором списка
def find_in_list(records, target_id):
    for rid, value in records:
        if rid == target_id:
            return value
    return None

#3. словарь с теми же данными ---
records_dict = {rid: value for rid, value in records}
print("dict size:", len(records_dict))

#4-5. сравнение на большом количестве запросов
# Готовим 1000 случайных id для поиска — одних и тех же для обоих случаев
import random as _random
query_ids = [_random.randint(0, 9_999) for _ in range(1000)]

#поиск в списке
t0 = time.perf_counter()
for qid in query_ids:
    _ = find_in_list(records, qid)
t1 = time.perf_counter()
time_list = t1 - t0

#поиск в словаре
t0 = time.perf_counter()
for qid in query_ids:
    _ = records_dict.get(qid)
t1 = time.perf_counter()
time_dict = t1 - t0

print(f"\n1000 queries in list: {time_list:.4f} s")
print(f"1000 queries in dict: {time_dict:.6f} s")
print(f"dict is ~{time_list / time_dict:.0f}x faster")

#проверка
sample_id = 5000
print(f"\nsanity check for id={sample_id}:")
print("  list:", find_in_list(records, sample_id))
print("  dict:", records_dict.get(sample_id))

#задание 4
#1. хеши чисел и строк
print("\nhash() для чисел и строк:")
for key in [0, 1, 42, 205, -7, 10**18]:
    print(f"  hash({key!r:>20}) = {hash(key)}")

for key in ["student_205", "ivanov", "hello", "python", "a"]:
    print(f"  hash({key!r:>20}) = {hash(key)}")

#2. одинаковые ключи дают одинаковый хеш
print("\nidentical keys -> оsame hesh:")
print("  hash(205) == hash(205):", hash(205) == hash(205))
print("  hash('abc') == hash('abc'):", hash("abc") == hash("abc"))
print("  hash(205) == hash(206):", hash(205) == hash(206))

#3. функция bucket_index
def bucket_index(key, table_size):
    return hash(key) % table_size

print("\nbucket_index for table_size=10:")
test_keys = [0, 1, 2, 5, 10, 15, 20, 100, 205, 317, 999,
             "a", "b", "c", "abc", "xyz", "hello", "world",
             "student_1", "student_2", "student_3",
             "ivanov", "petrov", "sidorova", "kuznetsov",
             "key1", "key2", "key3", "key4", "key5",
             "test", "data", "python", "code", "lab"]

buckets = {}
for key in test_keys:
    idx = bucket_index(key, 10)
    buckets.setdefault(idx, []).append(key)

for idx in sorted(buckets):
    print(f"  bucket[{idx}]: {buckets[idx]}")

#5. примеры коллизий
print("\nkeys in one basket:")
for idx, keys in buckets.items():
    if len(keys) > 1:
        print(f"  bucket[{idx}] <- {keys}")


#задание 5
ht2 = HashTable(size=10)
for k in [0, 10, 20, 30, 40]:
    ht2.set(k, f"v_{k}")
print(ht2)

#задание 6
import random as _random
random.seed(42)  # фиксируем seed — чтобы результаты воспроизводились

N_KEYS = 500  # одинаковое количество ключей для всех таблиц
keys = [_random.randint(0, 10**9) for _ in range(N_KEYS)]

print(f"\n{'size':>6} | {'count':>6} | {'load_factor':>12} | "
      f"{'collisions':>10} | {'max_chain':>9}")

for size in (10, 100, 1000):
    ht = HashTable(size=size)
    for k in keys:
        ht.set(k, f"v_{k}")

    print(f"{size:>6} | {ht.count:>6} | {ht.load_factor:>12.2f} | "
          f"{ht.collision_count():>10} | {ht.max_chain_length():>9}")

          
from binary_heap import MinHeap

# Готовый список 
data = [2, 5, 7, 9, 11, 10, 15]
heap = MinHeap()
heap.data = data[:]   # копирует в кучу

print("\nheap in from of array:", heap.data)
print(f"size: {len(heap.data)}")

print("\nanalysis of nodes:")
print(f"{'i':>3} | {'values':>6} | {'parent':>10} | {'left':>10} | {'right':>10}")
print("-" * 55)

n = len(heap.data)
for i in range(n):
    value = heap.data[i]

    # родитель
    if i == 0:
        parent_str = "—"
    else:
        p = MinHeap.parent(i)
        parent_str = f"[{p}]={heap.data[p]}"

    # левый потомок
    l = MinHeap.left(i)
    left_str = f"[{l}]={heap.data[l]}" if l < n else "—"

    # правый потомок
    r = MinHeap.right(i)
    right_str = f"[{r}]={heap.data[r]}" if r < n else "—"

    print(f"{i:>3} | {value:>6} | {parent_str:>10} | {left_str:>10} | {right_str:>10}")

#задание 8
from binary_heap import MinHeap

heap8 = MinHeap()

values = [10, 4, 7, 1, 9, 3]
print(f"\nadds one: {values}\n")

for v in values:
    heap8.push(v)
    print(f"  push({v:>2}) -> data = {heap8.data}, "
          f"min = {heap8.data[0]}")

# Проверка свойства min-heap
def is_min_heap(heap): 
    n = len(heap)
    for i in range(n):
        l = MinHeap.left(i)
        r = MinHeap.right(i)
        if l < n and heap[l] < heap[i]:
            return False
        if r < n and heap[r] < heap[i]:
            return False
    return True

print(f"\nmin-heap ready: {is_min_heap(heap8.data)}")
print(f"min at root: {heap8.data[0]}")

#задание 9
from binary_heap import MinHeap

heap9 = MinHeap()
values9 = [10, 4, 7, 1, 9, 3]
for v in values9:
    heap9.push(v)

print(f"\nfirst heap: {heap9.data}")

print("\ntake one:")
extracted = []
while heap9.data:
    m = heap9.pop()
    extracted.append(m)
    print(f"  pop() -> {m:>2}, data = {heap9.data}")

print(f"\nextraction order: {extracted}")

# извлекает отсортировано по возрастанию
print(f"ascending order sorting: {extracted == sorted(extracted)}")

# Сравненивает с heapq
print("\ncomparison heapq.heappop:")
import heapq
h_std = [10, 4, 7, 1, 9, 3]
heapq.heapify(h_std)
extracted_std = []
while h_std:
    extracted_std.append(heapq.heappop(h_std))
print(f"  heapq: {extracted_std}")
print(f"  my:  {extracted}")
print(f"  coincide: {extracted == extracted_std}")

#задание 11

import time

#1. список из 100 000 случайных чисел
N = 100_000
data11 = [random.randint(0, 1_000_000) for _ in range(N)]
print(f"\narray size: {N}")

#2-5. Top-K для разных K
def top_k_sort(data, k):#Top-K через полную сортировку всего массива
    return sorted(data, reverse=True)[:k]

print(f"\n{'K':>6} | {'time, мс':>12} | {'first three':>20}")

for k in (10, 100, 1000):
    t0 = time.perf_counter()
    top = top_k_sort(data11, k)
    t1 = time.perf_counter()
    dt_ms = (t1 - t0) * 1000

    preview = top[:3]
    print(f"{k:>6} | {dt_ms:>12.3f} | {str(preview):>20}")

#сколько по времени занимает сама сортировка при разных n
print("\ndependence on size (K = 10):")
print(f"{'n':>8} | {'time, мс':>12}")

for n in (10_000, 50_000, 100_000, 200_000):
    d = [random.randint(0, 1_000_000) for _ in range(n)]
    t0 = time.perf_counter()
    _ = sorted(d, reverse=True)[:10]
    t1 = time.perf_counter()
    print(f"{n:>8} | {(t1 - t0) * 1000:>12.3f}")

#задание 12
import heapq

def top_k_heap(data, k):#Возвращает K наибольших элементов через min-heap размера K.
    if k <= 0:
        return []

    heap = []  # min-heap размера <= k

    for value in data:
        if len(heap) < k:
            heapq.heappush(heap, value)
        elif value > heap[0]:
            # выкидывает минимум из Top-K, добавляется новый кандидат
            heapq.heapreplace(heap, value)
        # иначе — игнорируем

    #внутри heap элементы не отсортированы.
    #для сравнения с полной сортировкой везвращаем их по убыванию.
    return sorted(heap, reverse=True)


#3. сравнение с полной сортировкой
print("\ncomparison of results for one array")
N12 = 100_000
data12 = [random.randint(0, 1_000_000) for _ in range(N12)]

for k in (10, 100, 1000):
    top_sort = sorted(data12, reverse=True)[:k]
    top_heap = top_k_heap(data12, k)
    equal = top_sort == top_heap
    print(f"  K={k:>4}: совпадают = {equal}")

#4. замеры времени
print(f"\ntime (n = {N12}):")
print(f"{'K':>6} | {'sort, мс':>12} | {'heap, мс':>12} | {'выигрыш':>10}")

def time_it(func, *args, repeats=5):
    t0 = time.perf_counter()
    for _ in range(repeats):
        result = func(*args)
    t1 = time.perf_counter()
    return (t1 - t0) / repeats * 1000, result

for k in (10, 100, 1000, 10_000):
    t_sort, _ = time_it(lambda: sorted(data12, reverse=True)[:k])
    t_heap, _ = time_it(lambda: top_k_heap(data12, k))
    speedup = t_sort / t_heap if t_heap > 0 else float("inf")
    print(f"{k:>6} | {t_sort:>12.3f} | {t_heap:>12.3f} | {speedup:>9.2f}x")

#5. зависимость от n при фиксированном K
print(f"\ndependence on array (K = 10):")
print(f"{'n':>8} | {'sort, мс':>12} | {'heap, мс':>12}")

for n in (10_000, 50_000, 100_000, 200_000):
    d = [random.randint(0, 1_000_000) for _ in range(n)]
    t_sort, _ = time_it(lambda: sorted(d, reverse=True)[:10], repeats=3)
    t_heap, _ = time_it(lambda: top_k_heap(d, 10), repeats=3)
    print(f"{n:>8} | {t_sort:>12.3f} | {t_heap:>12.3f}")

#задание 12

import heapq
import itertools


class ContestSystem: #cистема обработки результатов соревнования
    def __init__(self):
        # dict: O(1) в среднем на get/set по id
        self.participants = {}

        # min-heap: O(log n) на push/pop
        # seq нужен, чтобы при равном приоритете сохранялся FIFO-порядок
        self.check_queue = []
        self._seq = itertools.count()

    # Участники (dict)

    def add_or_update(self, pid, name, score):
        """Добавить или обновить участника. Структура: dict."""
        self.participants[pid] = {"name": name, "score": score}
        print(f"  [dict] set participant id={pid} name={name!r} score={score}")

    def get_participant(self, pid):
        """Получить участника по id. Структура: dict."""
        result = self.participants.get(pid)
        print(f"  [dict] get participant id={pid} -> {result}")
        return result

    #Очередь проверки (heapq) 

    def enqueue_check(self, pid, priority): #ставит результат участника в очередь проверки (меньший priority = срочнее)
        entry = (priority, next(self._seq), pid)
        heapq.heappush(self.check_queue, entry)
        print(f"  [heap] enqueue check: id={pid} priority={priority}")

    def process_next(self): #извлечь самый срочный результат
        if not self.check_queue:
            print("  [heap] queue is empty")
            return None
        priority, _, pid = heapq.heappop(self.check_queue)
        print(f"  [heap] process check: id={pid} priority={priority}")
        return pid

    #Top-K участников по score без полной сортировки. Возвращает список (score, id, name), отсортированный по убыванию score

    def top_k(self, k):
        print(f"  [heap] computing top-{k} via min-heap of size K")

        heap = []
        for pid, info in self.participants.items():
            item = (info["score"], pid, info["name"])
            if len(heap) < k:
                heapq.heappush(heap, item)
            elif item[0] > heap[0][0]:
                heapq.heapreplace(heap, item)

        return sorted(heap, reverse=True)


# ---------- Демонстрация ----------

print("\n-- 1. Добавление и обновление участников --")
cs = ContestSystem()
cs.add_or_update(101, "Иванов",   85)
cs.add_or_update(102, "Петров",   92)
cs.add_or_update(103, "Сидорова", 78)
cs.add_or_update(104, "Кузнецов", 95)
cs.add_or_update(105, "Смирнова", 88)

print("\n-- 2. Обновление результата --")
cs.add_or_update(101, "Иванов", 91)  # обновили score

print("\n-- 3. Получение по id --")
cs.get_participant(104)
cs.get_participant(999)  # несуществующий

print("\n-- 4. Очередь проверки (меньший priority = срочнее) --")
cs.enqueue_check(103, priority=3)
cs.enqueue_check(101, priority=1)
cs.enqueue_check(105, priority=2)
cs.enqueue_check(102, priority=2)  # тот же приоритет, что 105 — но придёт позже
cs.enqueue_check(104, priority=1)  # тот же приоритет, что 101 — но придёт позже

print("\nобработка очереди:")
while cs.check_queue:
    cs.process_next()

print("\n-- 5. Top-3 участников по score --")
top3 = cs.top_k(3)
for rank, (score, pid, name) in enumerate(top3, start=1):
    print(f"    #{rank}: id={pid} {name!r} score={score}")

print("\n-- 6. Top-5 (все участники) --")
top5 = cs.top_k(5)
for rank, (score, pid, name) in enumerate(top5, start=1):
    print(f"    #{rank}: id={pid} {name!r} score={score}")