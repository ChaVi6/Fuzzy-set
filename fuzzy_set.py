# равенство
def equal(set_a, set_b):
    for element in set_a.get_set():
        if element[0] not in set_b.get_elements():
            return False
        else:
            if element[1] != set_b.get_membership_value(element[0]):
                return False

    for element in set_b.get_set():
        if element[0] not in set_a.get_elements():
            return False
        else:
            if element[1] != set_a.get_membership_value(element[0]):
                return False
    return True


# объединение
def union(set_a, set_b):
    union_set = []
    for element in set_a.get_set():
        if element[0] in set_b.get_elements():
            if element[1] > set_b.get_membership_value(element[0]):
                union_set.append(element)
            else:
                union_set.append([element[0], set_b.get_membership_value(element[0])])
        else:
            union_set.append(element)

    for element in set_b.get_set():
        if element[0] not in [elem[0] for elem in union_set]:
            if element[0] in set_a.get_elements():
                if element[1] > set_a.get_membership_value(element[0]):
                    union_set.append(element)
                else:
                    union_set.append([element[0], set_a.get_membership_value(element[0])])
            else:
                union_set.append(element)

    return FuzzySet(union_set)


# пересечение
def intersection(set_a, set_b):
    intersection_set = []
    elements_b = set_b.get_elements()
    for element in set_a.get_set():
        if element[0] in elements_b:
            if element[1] < set_b.get_set()[elements_b.index(element[0])][1]:
                intersection_set.append(element)
            else:
                intersection_set.append(set_b.get_set()[elements_b.index(element[0])])
    return FuzzySet(intersection_set)


# дополнение
def complement(set_):
    complement_set = []
    for element in set_.get_set():
        complement_set.append([element[0], round(1 - element[1], 6)])
    return FuzzySet(complement_set)


# разность
def difference(set_a, set_b):
    difference_set = []
    comp_b = complement(set_b)
    for element in set_a.get_set():
        if element[0] in comp_b.get_elements():
            difference_set.append(
                [element[0], min(element[1], comp_b.get_set()[comp_b.get_elements().index(element[0])][1])])
        else:
            difference_set.append(element)
    for element in set_b.get_set():
        if element[0] not in set_a.get_elements():
            difference_set.append([element[0], 0])
    return FuzzySet(difference_set)


# симметрическая разность
def symmetrical_difference(set_a, set_b):
    s_difference_set = []
    for element in set_a.get_set():
        if element[0] in set_b.get_elements():
            s_difference_set.append([element[0], round(abs(element[1]
                                                           - set_b.get_set()[set_b.get_elements().index(element[0])][
                                                               1]), 6)])
        else:
            s_difference_set.append(element)
    for element in set_b.get_set():
        if element[0] not in set_a.get_elements():
            s_difference_set.append(element)
    return FuzzySet(s_difference_set)


# дизъюнктивная сумма
def disjunctive_sum(set_a, set_b):
    return union(intersection(set_a, complement(set_b)), intersection(complement(set_a), set_b))


class FuzzySet:
    # создание
    def __init__(self, elements):
        self._set = elements
        self.fuzzy_sort()

    # множество
    def get_set(self):
        return self._set

    # список элементов множества
    def get_elements(self):
        return [elem[0] for elem in self.get_set()]

    # значение принадлежности элемента
    def get_membership_value(self, element):
        elements = self.get_set()
        s = [e[0] for e in elements]
        if element in s:
            return self.get_set()[s.index(element)][1]
        else:
            print("Element not found")
            return 0

    # удаление
    def delete_set(self):
        del self._set

    # добавление элемента(ов)
    def add_elements(self, elements):
        for element in elements:
            self._set.append(element)
        self.fuzzy_sort()

    # изменение степени принадлежности элемента
    def set_membership_value(self, element, value):
        if element in self.get_elements():
            self._set[self.get_elements().index(element)][1] = value
            self.fuzzy_sort()
        else:
            print("Element not found")

    # свойства

    # высота
    def get_height(self):
        max_membership_value = max(self.get_set(), key=lambda x: x[1])[1]
        return max_membership_value

    # пустота
    def is_empty(self):
        for element in self.get_set():
            if element[1] != 0:
                return False
        return True

    # унимодальность
    def is_unimodal(self):
        set_ = self.get_set()
        count_ones = 0

        for pair in set_:
            key, value = pair
            if value == 1:
                count_ones += 1

        return count_ones == 1

    # точечность
    def is_point_set(self):
        set_ = self.get_set()
        count_ = 0

        for pair in set_:
            key, value = pair
            if value != 0:
                count_ += 1

        return count_ == 1

    # ядро
    def find_core(self):
        set_ = self.get_set()
        core = []

        for pair in set_:
            key, value = pair[0], pair[1]
            if value == 1:
                core.append(key)

        return core

    # вывод носителя нечёткого множества
    def support(self):
        return [elem[0] for elem in self.get_set() if self.get_membership_value(elem[0]) > 0]

    # проверка множества на субнормальность
    def is_subnormal(self):
        for elem in self.get_set():
            if self.get_membership_value(elem[0]) == 1:
                return False
        return True

    # рефлизация нечёткого среза
    def fuzzy_slice(self, a):
        return [elem[0] for elem in self.get_set() if self.get_membership_value(elem[0]) >= a]

    # вывод точек перехода
    def transition_point(self):
        return [elem[0] for elem in self.get_set() if self.get_membership_value(elem[0]) == 0.5]

    # проверка точек перехода
    def is_transition_point(self, point):
        for elem in self.get_set():
            if self.get_membership_value(elem[0]) == 0.5 and elem[0] == point:
                return True
        return False

    # проверка на корректность данных
    def fuzzy_sort(self):
        sorted_set = []
        seen = set()
        for element in self.get_set():
            if not isinstance(element[1], (int, float)):
                print("Error for element ", element, ": membership value is not a number. Aborting element\n")
            elif element[0] in seen:
                print("Warning for element ", element, ": duplicate encountered. Aborting element\n")
            elif element[1] > 1:
                print("Warning for element ", element, ": membership value of higher than 1 encountered. Setting "
                                                       "membership value to 1\n")
                element[1] = 1
                sorted_set.append(element)
                seen.add(element[0])
            elif element[1] < 0:
                print("Warning for element ", element, ": membership value of lower than 0 encountered. Setting "
                                                       "membership value to 0\n")
                element[1] = 0
                sorted_set.append(element)
                seen.add(element[0])
            elif element[0] not in seen:
                sorted_set.append(element)
                seen.add(element[0])
        self._set = sorted_set


if __name__ == "__main__":
    A = FuzzySet([[30, .2], [6, .9], [3333, .0000001], [9, .3]])
    B = FuzzySet([[30, .8], [7, .6], [44, .68], [9, .99]])

    print("A: ", A.get_set())
    print("B: ", B.get_set())
    print("Height A: ", A.get_height())
    print("Height B:  ", B.get_height())
    B.add_elements([[10, 0], [9, 1]])
    B.add_elements([[8, .88], [12, .5]])
    B.add_elements([])
    B.set_membership_value(10, 11)
    print("B after adding and changing elements:  ", B.get_set())
    print("Union: ", union(A, B).get_set())
    print("Intersection: ", intersection(A, B).get_set())
    print("Complement A: ", complement(A).get_set())
    print("Difference A - B: ", difference(A, B).get_set())
    print("Difference B - A: ", difference(B, A).get_set())
    print("Symmetrical difference: ", symmetrical_difference(A, B).get_set())
    print("Disjunctive sum: ", disjunctive_sum(A, B).get_set())
    print("Support:", A.support())
    print("Support:", B.support())
    print("Is subnormal:", A.is_subnormal())
    print("Is subnormal:", B.is_subnormal())
    print("Fuzzy slice:", A.fuzzy_slice(1))
    print("Fuzzy slice:", A.fuzzy_slice(0.5))
    print("Fuzzy slice:", A.fuzzy_slice(0.2))
    print("Fuzzy slice:", B.fuzzy_slice(1))
    print("Fuzzy slice:", B.fuzzy_slice(0.7))
    print("List transition points: ", A.transition_point())
    print("List transition points: ", B.transition_point())
    print("Is transition point: ", A.is_transition_point(5))
    print("Is transition point: ", B.is_transition_point(12))
