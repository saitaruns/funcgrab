import tree_sitter_python as tspython
from tree_sitter import Language, Parser

PY_LANGUAGE = Language(tspython.language())

parser = Parser(PY_LANGUAGE)

def parse_code(code):
    tree = parser.parse(bytes(code, "utf8"))
    root_node = tree.root_node
    functions = []
    for node in root_node.children:
        if node.type == 'function_definition':
            function_name = node.child_by_field_name('name').text.decode('utf-8')
            start_byte = node.start_byte
            end_byte = node.end_byte
            functions.append({
                "name": function_name,
                "code": code[start_byte:end_byte]
            })
    return functions
