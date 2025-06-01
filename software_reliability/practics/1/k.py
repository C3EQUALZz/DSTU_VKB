import ast
import math
import os
import json
from collections import defaultdict
from typing import Dict, List, Tuple, Any, Union
from prettytable import PrettyTable


class DetailedCodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.operators = defaultdict(list)
        self.operands = defaultdict(list)
        self.stats = {
            "assignments": 0,
            "branches": 0,
            "loops": 0,
            "function_calls": 0,
            "imports": 0,
            "exceptions": 0,
            "operators_count": 0,
            "parameters": 0,
            "operands_count": 0
        }
        self.current_line = 0
        self.import_aliases = {}  # Для хранения алиасов импортов
        self.global_vars = set()

    def visit(self, node: ast.AST) -> Any:
        self.current_line = getattr(node, 'lineno', self.current_line)
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def get_full_name(self, node: Union[ast.Name, ast.Attribute]) -> str:
        """Рекурсивно получает полное имя функции/метода"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self.get_full_name(node.value)}.{node.attr}"
        return ""

    def visit_Assign(self, node: ast.Assign) -> Any:
        # Проверяем, не является ли это аннотацией типа
        if any(hasattr(target, 'annotation') for target in node.targets):
            self.generic_visit(node)
            return

        self.stats["assignments"] += 1
        self.operators["Присваивание"].append((self.current_line, node.col_offset))
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> Any:
        # Игнорируем аннотации типов
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> Any:
        op_type = type(node.op).__name__
        self.operators[f"Увеличение ({op_type})"].append((self.current_line, node.col_offset))
        self.stats["operators_count"] += 1
        self.generic_visit(node)

    def visit_BinOp(self, node: ast.BinOp) -> Any:
        op_type = type(node.op).__name__
        self.operators[op_type].append((self.current_line, node.col_offset))
        self.stats["operators_count"] += 1
        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare) -> Any:
        for op in node.ops:
            op_type = type(op).__name__
            self.operators[op_type].append((self.current_line, node.col_offset))
            self.stats["operators_count"] += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> Any:
        op_type = type(node.op).__name__
        self.operators[op_type].append((self.current_line, node.col_offset))
        self.stats["operators_count"] += 1
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> Any:
        self.stats["branches"] += 1
        self.operators["Условие (if)"].append((self.current_line, node.col_offset))
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> Any:
        self.stats["loops"] += 1
        self.operators["Цикл for"].append((self.current_line, node.col_offset))
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> Any:
        self.stats["loops"] += 1
        self.operators["Цикл while"].append((self.current_line, node.col_offset))
        self.generic_visit(node)

    def visit_Try(self, node: ast.Try) -> Any:
        self.stats["exceptions"] += 1
        self.operators["Обработка исключений (try)"].append((self.current_line, node.col_offset))
        self.generic_visit(node)

    def visit_Raise(self, node: ast.Raise) -> Any:
        self.stats["exceptions"] += 1
        self.operators["Генерация исключения (raise)"].append((self.current_line, node.col_offset))
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> Any:
        try:
            func_name = self.get_full_name(node.func)
            if func_name:
                self.stats["function_calls"] += 1
                self.operators[f"Вызов функции: {func_name}"].append((self.current_line, node.col_offset))
        except:
            pass
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> Any:
        for alias in node.names:
            self.stats["imports"] += 1
            module_name = alias.name
            asname = alias.asname or module_name
            self.import_aliases[asname] = module_name
            self.operands[f"Импорт: {module_name}"].append((self.current_line, node.col_offset))
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        for alias in node.names:
            self.stats["imports"] += 1
            module = f"{node.module}.{alias.name}" if node.module else alias.name
            asname = alias.asname or alias.name
            self.import_aliases[asname] = module
            self.operands[f"Импорт из {node.module}: {alias.name}"].append((self.current_line, node.col_offset))
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.stats["parameters"] += len(node.args.args)
        self.operands[f"Функция: {node.name}"].append((self.current_line, node.col_offset))
        self.stats["operands_count"] += 1
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self.operands[f"Класс: {node.name}"].append((self.current_line, node.col_offset))
        self.stats["operands_count"] += 1
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> Any:
        if isinstance(node.ctx, ast.Load):
            parent = getattr(node, 'parent', None)
            if isinstance(parent, (ast.AnnAssign, ast.Assign)):
                if hasattr(parent, 'annotation') or any(hasattr(target, 'annotation') for target in getattr(parent, 'targets', [])):
                    self.generic_visit(node)
                    return
            if node.id in ('List', 'Dict', 'Set', 'Tuple', 'Optional', 'Union', 'Type', 'Callable'):
                self.generic_visit(node)
                return
            if isinstance(parent, ast.Subscript):
                self.generic_visit(node)
                return
            name = node.id
            if name in self.import_aliases:
                name = self.import_aliases[name]
            self.operands[f"Переменная: {name}"].append((self.current_line, node.col_offset))
            self.stats["operands_count"] += 1
            # Определяем глобальные переменные
            if not hasattr(node, 'parent') or not isinstance(node.parent, ast.FunctionDef):
                self.global_vars.add(name)
        self.generic_visit(node)

    def calculate_holstead_metrics(self) -> dict:
        eta1 = len(self.operators)  # Уникальные операторы
        eta2 = len(self.operands)  # Уникальные операнды
        N1 = self.stats["operators_count"]  # Общее число операторов
        N2 = self.stats["operands_count"]  # Общее число операндов
        eta2_star = len(self.global_vars) + self.stats["parameters"]  # Входные/выходные параметры
        eta = eta1 + eta2
        N = N1 + N2
        V = N * math.log2(eta) if eta > 0 else 0
        V_star = (eta2_star + 2) * math.log2(eta2_star + 2) if eta2_star + 2 > 0 else 0
        L = V_star / V if V != 0 else 0
        lambda_ = L * V_star
        E = V / L if L != 0 else 0

        return {
            "η1": eta1,
            "η2": eta2,
            "N1": N1,
            "N2": N2,
            "η2*": eta2_star,
            "η": eta,
            "N": N,
            "V": V,
            "V*": V_star,
            "L": L,
            "λ": lambda_,
            "E": E
        }

    def visit_Attribute(self, node: ast.Attribute) -> Any:
        if isinstance(node.ctx, ast.Load):
            attr_name = f"{self.get_full_name(node.value)}.{node.attr}"
            self.operands[f"Атрибут: {attr_name}"].append((self.current_line, node.col_offset))
            self.stats["operands_count"] += 1
        self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant) -> Any:
        value = node.value
        if isinstance(value, (int, float, str, bool)):
            self.operands[f"Константа: {repr(value)}"].append((self.current_line, node.col_offset))
            self.stats["operands_count"] += 1
        self.generic_visit(node)


def analyze_file(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as source:
        try:
            tree = ast.parse(source.read(), filename=file_path)
        except SyntaxError as e:
            print(f"Ошибка синтаксиса в файле: {file_path}")
            print(f"Детали: {e}")
            return None

    # Установим родительские ссылки
    class ParentSetter(ast.NodeVisitor):
        def __init__(self):
            self.parent = None

        def visit(self, node):
            node.parent = self.parent
            prev_parent = self.parent
            self.parent = node
            super().visit(node)
            self.parent = prev_parent

    ParentSetter().visit(tree)

    analyzer = DetailedCodeAnalyzer()
    analyzer.visit(tree)

    holstead_metrics = analyzer.calculate_holstead_metrics()

    return {
        "file": os.path.basename(file_path),
        "path": os.path.abspath(file_path),
        "stats": analyzer.stats,
        "operators": analyzer.operators,
        "operands": analyzer.operands,
        "holstead": holstead_metrics
    }


def generate_tables(analysis_results: dict, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    # Таблица операторов
    operators_table = PrettyTable()
    operators_table.field_names = ["№ п/п", "Операторы, операции", "Номера строк", "Количество повторений"]

    sorted_ops = sorted(analysis_results['operators'].items(), key=lambda x: min(pos[0] for pos in x[1]))
    for idx, (op, positions) in enumerate(sorted_ops, 1):
        lines = sorted(set(pos[0] for pos in positions))
        operators_table.add_row([idx, op, ', '.join(map(str, lines)), len(positions)])

    # Таблица операндов
    operands_table = PrettyTable()
    operands_table.field_names = ["№ п/п", "Операнды", "Номера строк", "Количество повторений"]

    sorted_ops = sorted(analysis_results['operands'].items(), key=lambda x: min(pos[0] for pos in x[1]))
    for idx, (op, positions) in enumerate(sorted_ops, 1):
        lines = sorted(set(pos[0] for pos in positions))
        operands_table.add_row([idx, op, ', '.join(map(str, lines)), len(positions)])

    with open(os.path.join(output_dir, "tables.txt"), "w", encoding="utf-8") as f:
        f.write("Таблица 1.3 Операторы и операции, используемые в программе\n")
        f.write(str(operators_table))
        f.write("\n\nТаблица 1.4 Словарь операндов программы\n")
        f.write(str(operands_table))

    holstead_table = PrettyTable()
    holstead_table.field_names = ["Наименование характеристики", "Обозначение и формула", "Значение"]

    metrics = [
        ("Число простых (уникальных) операторов и операций", "η₁", analysis_results['holstead']['η1']),
        ("Число простых (уникальных) операндов", "η₂", analysis_results['holstead']['η2']),
        ("Общее число всех операторов и операций", "N₁", analysis_results['holstead']['N1']),
        ("Общее число всех операндов", "N₂", analysis_results['holstead']['N2']),
        ("Число входных и выходных переменных (параметров)", "η₂*", analysis_results['holstead']['η2*']),
        ("Словарь программы", "η = η₁ + η₂", analysis_results['holstead']['η']),
        ("Длина реализации программы", "N = N₁ + N₂", analysis_results['holstead']['N']),
        ("Объем программы (в битах)", "V = N · log₂(η)", analysis_results['holstead']['V']),
        ("Потенциальный объем программы", "V* = (η₂* + 2) · log₂(η₂* + 2)", analysis_results['holstead']['V*']),
        ("Уровень реализации программы", "L = V* / V", analysis_results['holstead']['L']),
        ("Уровень реализации языка", "λ = L · V*", analysis_results['holstead']['λ']),
        ("Работа программирования", "E = V / L", analysis_results['holstead']['E'])
    ]

    for row in metrics:
        holstead_table.add_row(row)

    with open(os.path.join(output_dir, "tables.txt"), "a", encoding="utf-8") as f:
        f.write("\n\nТаблица 1.6 Значения метрик Холстеда для программы\n")
        f.write(str(holstead_table))


if __name__ == "__main__":
    file_path = r"D:\Progrramming\PycharmProjects\DSTU_VKB\software_reliability\practics\1\first\main.py"
    output_dir = "result"

    if not os.path.isfile(file_path):
        print(f"Ошибка: Файл не найден - {file_path}")
        exit(1)

    results = analyze_file(file_path)
    if results is None:
        print("Не удалось проанализировать файл из-за ошибки синтаксиса")
        exit(1)

    generate_tables(results, output_dir)

    print(f"\nАнализ завершен для {file_path}")
    print(f"Таблицы сгенерированы в папку: {output_dir}")
    print("\nКраткая статистика:")
    print(f"Операторов: {results['stats']['operators_count']}")
    print(f"Операндов: {results['stats']['operands_count']}")
    print(f"Присваивания: {results['stats']['assignments']}")
    print(f"Ветвления: {results['stats']['branches']}")
    print(f"Циклы: {results['stats']['loops']}")
    print(f"Вызовы функций: {results['stats']['function_calls']}")
    print(f"Импорты: {results['stats']['imports']}")
    print(f"Обработка исключений: {results['stats']['exceptions']}")
