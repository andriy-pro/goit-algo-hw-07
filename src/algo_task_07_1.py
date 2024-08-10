class AVLNode:
    def __init__(self, key=None):
        self.left = None
        self.right = None
        self.key = key
        self.height = 1

    def __str__(self):
        return f"({self.left})<-{self.key}->{self.right}"

    def get_height(self, node=None):
        if not node:
            return 0
        return node.height

    def get_balance(self):
        if not self:
            return 0
        return self.get_height(self.left) - self.get_height(self.right)

    def left_rotate(self):
        y = self.right
        self.right = y.left
        y.left = self

        # Update heights
        self.height = 1 + max(self.get_height(self.left), self.get_height(self.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def right_rotate(self):
        """Виконує праве обертання дерева."""
        x = self.left
        T3 = x.right

        x.right = self
        self.left = T3

        self.height = 1 + max(self.get_height(self.left), self.get_height(self.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        return x

    def insert(self, key):
        """Метод для вставки нового ключа в дерево з урахуванням балансування."""
        if self.key is None:
            self.key = key
            return self

        if key < self.key:
            if self.left is None:
                self.left = AVLNode(key)
            else:
                self.left = self.left.insert(key)
        else:
            if self.right is None:
                self.right = AVLNode(key)
            else:
                self.right = self.right.insert(key)

        self.height = 1 + max(self.get_height(self.left), self.get_height(self.right))

        balance = self.get_balance()

        # Лівий лівий випадок
        if balance > 1 and key < self.left.key:
            return self.right_rotate()

        # Правий правий випадок
        if balance < -1 and key > self.right.key:
            return self.left_rotate()

        # Лівий правий випадок
        if balance > 1 and key > self.left.key:
            self.left = self.left.left_rotate()
            return self.right_rotate()

        # Правий лівий випадок
        if balance < -1 and key < self.right.key:
            self.right = self.right.right_rotate()
            return self.left_rotate()

        return self

    def max(self):
        """Метод для знаходження найбільшого значення в дереві."""
        current = self
        while current.right is not None:
            current = current.right
        return current.key

    def min(self):
        """Метод для знаходження найменшого значення в дереві."""
        current = self
        while current.left is not None:
            current = current.left
        return current.key


# Приклад використання
if __name__ == "__main__":
    avl_tree = AVLNode()
    keys = [10, 20, 30, 40, 50, 25]

    for key in keys:
        avl_tree.insert(key)

    # Виведення дерева
    print("Дерево:", avl_tree)

    # Виведення висоти дерева
    print("Висота дерева:", avl_tree.get_height())

    # Виведення балансу дерева
    print("Баланс дерева:", avl_tree.get_balance())

    # Виведення лівого піддерева
    print("Ліве піддерево:", avl_tree.left)

    # Виведення правого піддерева
    print("Праве піддерево:", avl_tree.right)

    # Виведення висоти лівого піддерева
    print("Висота лівого піддерева:", avl_tree.get_height(avl_tree.left))

    # Виведення висоти правого піддерева
    print("Висота правого піддерева:", avl_tree.get_height(avl_tree.right))

    # Виведення максимального значення
    print("Максимальне значення:", avl_tree.max())

    # Виведення мінімального значення
    print("Мінімальне значення:", avl_tree.min())
