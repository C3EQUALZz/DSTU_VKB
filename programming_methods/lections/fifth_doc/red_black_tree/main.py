import tkinter as tk
from tkinter import messagebox
from typing import Optional
from rbtree import RBTree, RBNode, NodeColor  # Предполагается, что обновленный код в rbtree.py


class RBApp:
    def __init__(self, root: tk.Tk) -> None:
        self.tree = RBTree()
        self.root = root
        self.root.title("Red-Black Tree Visualization")

        # GUI elements
        self._setup_ui()

    def _setup_ui(self) -> None:
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        self.entry = tk.Entry(control_frame, font=("Arial", 12), width=15)
        self.entry.grid(row=0, column=0, padx=5)

        buttons = [
            ("Insert", self._insert_key),
            ("Delete", self._delete_key),
            ("Search", self._search_key),
            ("Preorder", self._show_preorder),
        ]

        for col, (text, command) in enumerate(buttons, start=1):
            btn = tk.Button(
                control_frame,
                text=text,
                command=command,
                font=("Arial", 10),
                width=12
            )
            btn.grid(row=0, column=col, padx=2)

        self.canvas = tk.Canvas(
            self.root,
            width=1000,
            height=600,
            bg="white",
            highlightthickness=0
        )
        self.canvas.pack(pady=10, expand=True, fill=tk.BOTH)

    def _validate_input(self) -> Optional[int]:
        try:
            return int(self.entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")
            self.entry.delete(0, tk.END)
            return None

    def _insert_key(self) -> None:
        if (key := self._validate_input()) is not None:
            self.tree.insert(key)
            self._refresh_ui(f"Key {key} inserted successfully")

    def _delete_key(self) -> None:
        if (key := self._validate_input()) is not None:
            self.tree.delete(key)
            self._refresh_ui(f"Key {key} deleted successfully")

    def _search_key(self) -> None:
        if (key := self._validate_input()) is not None:
            if node := self.tree.search(key):
                self._redraw_tree(highlight_node=node)
                messagebox.showinfo("Search", f"Key {key} found")
            else:
                messagebox.showinfo("Search", "Key not found")

    def _show_preorder(self) -> None:
        traversal = self.tree.preorder_traversal(self.tree.root)
        messagebox.showinfo(
            "Preorder Traversal",
            f"Preorder: {' '.join(traversal)}" if traversal else "Tree is empty"
        )

    def _refresh_ui(self, message: str) -> None:
        self.entry.delete(0, tk.END)
        self._redraw_tree()
        messagebox.showinfo("Operation Success", message)

    def _redraw_tree(self, highlight_node: Optional[RBNode] = None) -> None:
        self.canvas.delete("all")
        if self.tree.root != self.tree.sentinel:
            self._draw_subtree(
                self.tree.root,
                x=500,
                y=30,
                x_offset=300,
                highlight_node=highlight_node
            )

    def _draw_subtree(
            self,
            node: RBNode,
            x: int,
            y: int,
            x_offset: int,
            highlight_node: Optional[RBNode] = None
    ) -> None:
        if node == self.tree.sentinel:
            return

        # Calculate colors and outline
        fill_color = "red" if node.color == NodeColor.RED else "black"
        outline_color = "cyan" if node == highlight_node else "gray20"

        # Draw node
        self.canvas.create_oval(
            x - 20, y - 20, x + 20, y + 20,
            fill=fill_color,
            outline=outline_color,
            width=2
        )
        self.canvas.create_text(
            x, y,
            text=str(node.key),
            fill="white" if fill_color == "black" else "black",
            font=("Arial", 10, "bold")
        )

        # Draw connections to children
        new_offset = int(x_offset * 0.5)
        if node.left != self.tree.sentinel:
            self.canvas.create_line(
                x, y + 20,
                   x - x_offset, y + 80,
                fill="gray40",
                width=1
            )
            self._draw_subtree(
                node.left,
                x - x_offset,
                y + 80,
                new_offset,
                highlight_node
            )

        if node.right != self.tree.sentinel:
            self.canvas.create_line(
                x, y + 20,
                   x + x_offset, y + 80,
                fill="gray40",
                width=1
            )
            self._draw_subtree(
                node.right,
                x + x_offset,
                y + 80,
                new_offset,
                highlight_node
            )


def main() -> None:
    root = tk.Tk()
    app = RBApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
