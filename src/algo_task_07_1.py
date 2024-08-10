class AVLTree:
    class Node:  # Внутрішній клас для представлення вузлів дерева
        def __init__(self, key):
            self.key = key  # Значення, яке зберігається в вузлі
            self.left = None  # Лівий нащадок
            self.right = None  # Правий нащадок
            self.height = 1  # Висота нового вузла, початкове значення 1

    def __init__(self):
        self.root = None  # Корінь дерева, спочатку порожній

    def __str__(self):  # Метод для виводу дерева "у зрозумілому вигляді"

        levels = []  # Список для зберігання вузлів на кожному рівні
        self._fill_levels(self.root, 0, levels)  # Заповнюємо список
        return "\n".join(" ".join(str(node) for node in level) for level in levels)

    # Приватний метод для заповнення списку рівнів
    def _fill_levels(self, node, level, levels):
        if node:
            if len(levels) <= level:  # Якщо рівень ще не існує
                levels.append([])  # Додаємо новий рівень
            levels[level].append(node.key)  # Додаємо ключ вузла до рівня
            # Рекурсивно заповнюємо ліве піддерево
            self._fill_levels(node.left, level + 1, levels)
            # Рекурсивно заповнюємо праве піддерево
            self._fill_levels(node.right, level + 1, levels)

    def insert(self, key):  # Публічний метод для вставки ключа в дерево
        if not self.root:
            self.root = self.Node(key)  # Якщо дерево порожнє, створюємо кореневий вузол
        else:  # Інакше викликаємо метод для вставки
            self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        # Приватний метод для вставки ключа в піддерево з коренем `node`
        if not node:
            return self.Node(key)  # Якщо досягли пустого місця, створюємо новий вузол

        # Стандартна вставка для бінарного дерева пошуку
        if key < node.key:  # Якщо ключ менший, вставляємо в ліве піддерево
            node.left = self._insert(node.left, key)
        elif key > node.key:  # Якщо ключ більший, вставляємо в праве піддерево
            node.right = self._insert(node.right, key)
        else:
            return node  # Дублікати не допускаються

        # Оновлюємо висоту вузла
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        # Отримуємо баланс для перевірки, чи вузол став незбалансованим
        balance = self.get_balance(node)

        # Виконуємо обертання, якщо вузол став незбалансованим
        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)  # Лівий лівий випадок (LL)
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)  # Правий правий випадок (RR)
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)  # Лівий правий випадок (LR)
            return self.right_rotate(node)
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)  # Правий лівий випадок (RL)
            return self.left_rotate(node)

        return node  # Повертаємо (можливо, оновлений) вузол

    def left_rotate(self, node):  # Метод для лівого обертання
        new_root = node.right  # Правий нащадок стає новим коренем
        node.right = new_root.left  # Зберігаємо лівого нащадка нового кореня
        new_root.left = node  # Виконуємо обертання

        # Оновлюємо висоти
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        new_root.height = 1 + max(
            self.get_height(new_root.left), self.get_height(new_root.right)
        )

        return new_root  # Повертаємо новий корінь

    def right_rotate(self, node):  # Метод для правого обертання

        new_root = node.left  # Лівий нащадок стає новим коренем
        node.left = new_root.right  # Зберігаємо правого нащадка нового кореня
        new_root.right = node  # Виконуємо обертання

        # Оновлюємо висоти
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        new_root.height = 1 + max(
            self.get_height(new_root.left), self.get_height(new_root.right)
        )

        return new_root  # Повертаємо новий корінь

    def get_height(self, node):  # Метод для отримання висоти вузла
        return node.height if node else 0  # Якщо вузол None, висота 0

    def get_balance(self, node):  # Метод для отримання балансу вузла
        return self.get_height(node.left) - self.get_height(node.right)

    def max(self):  # Повертає максимальний ключ у дереві
        if not self.root:
            return None  # Якщо дерево порожнє, повертаємо None
        current = self.root
        while current.right:  # Проходимо правими нащадками
            current = current.right
        return current.key if current else None  # Якщо дерево порожнє, повертаємо None

    def min(self):
        # Повертає мінімальний ключ у дереві
        if not self.root:
            return None  # Якщо дерево порожнє, повертаємо None
        current = self.root
        while current.left:  # Проходимо лівими нащадками
            current = current.left
        return current.key  # Повертаємо ключ найменшого вузла

    # Метод "sum" викликає приватний метод "_sum", уникаючи прямого
    # рекурсивного виклику "sum" -> "sum", що призвело б до нескінченної рекурсії.
    def sum(self):
        # Публічний метод для обчислення суми всіх значень у дереві
        return self._sum(self.root)  # Викликаємо приватний метод для обчислення суми

    def _sum(self, node):
        # Приватний метод для обчислення суми значень у піддереві з коренем `node`
        if not node:
            return 0  # Якщо вузол None, повертаємо 0
        # Рекурсивно обчислюємо суму лівого та правого піддерев,
        # додаємо значення поточного вузла
        return node.key + self._sum(node.left) + self._sum(node.right)


if __name__ == "__main__":
    avl_tree = AVLTree()
    keys = [10, 20, 30, 40, 50, 25]

    for key in keys:
        avl_tree.insert(key)

    print("Дерево:\n", avl_tree)

    print("Максимальний ключ:", avl_tree.max())  # 50
    print("Мінімальний ключ:", avl_tree.min())  # 10
    print("Сума всіх значень:", avl_tree.sum())  # 175

    # # Тестування на порожньому дереві
    # empty_AVL_tree = AVLTree()
    # keys = []
    # for key in keys:
    #     avl_tree.insert(key)
    # print("Дерево:\n", empty_AVL_tree)
    # print("Максимальний ключ:", empty_AVL_tree.max())  # 50
    # print("Мінімальний ключ:", empty_AVL_tree.min())  # 10
    # print("Сума всіх значень:", empty_AVL_tree.sum())  # 175
