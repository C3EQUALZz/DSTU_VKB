# Найти высоту бинарного дерева
from programming_methods.lections.first_doc.sixth_block.core.binary_tree import BinaryTree


def main() -> None:
    tree = BinaryTree[int]()
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)
    tree.insert(40)
    print("Tree structure:\n", tree)
    print("Height:", tree.height)


if __name__ == "__main__":
    main()
