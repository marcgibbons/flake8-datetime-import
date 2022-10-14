import ast
import sys

if sys.version_info < (3, 8):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata


ERRORS = {
    "DTI100": (
        "`from datetime import ...` is not allowed. `datetime` must be "
        "imported as a module."
    ),
    "DTI101": (
        "`datetime` imported without aliasing as `dt`. "
        "Expected `import datetime as dt`."
    ),
    "DTI200": (
        "`from time import ...` is not allowed. `time` must be "
        "imported as a module."
    ),
    "DTI201": (
        "`time` imported without aliasing as `tm`. "
        "Expected `import time as tm`."
    ),
}


class Visitor(ast.NodeVisitor):
    def __init__(self):
        self.problems = []

    def visit_ImportFrom(self, node):
        if node.module == "datetime":
            self.problems.append((node.lineno, node.col_offset, "DTI100"))
        if node.module == "time":
            self.problems.append((node.lineno, node.col_offset, "DTI200"))

        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name == "datetime" and alias.asname != "dt":
                problem = (node.lineno, node.col_offset, "DTI101")
                self.problems.append(problem)
            if alias.name == "time" and alias.asname != "tm":
                problem = (node.lineno, node.col_offset, "DTI201")
                self.problems.append(problem)
        self.generic_visit(node)


class Plugin:
    name = __name__
    version = importlib_metadata.version(__name__)

    def __init__(self, tree):
        self.tree = tree

    def run(self):
        visitor = Visitor()
        visitor.visit(self.tree)
        for line, col, code in visitor.problems:
            msg = f"{code} {ERRORS[code]}"
            yield line, col, msg, type(self)
