import ast

from utils.util import replace_with_all

def name_to_operation(name):
    if name == "Add":
        op = "+"
    elif name == "Sub":
        op = "-"
    elif name == "MatMult":
        op = "*"
    elif name == "Mult":
        op = "*"
    elif name == "Div":
        op = "/"
    elif name == "Pow":
        return lambda x,y : f"pow({x}, {y})"
    elif name == "USub":
        return lambda x : f"- {x}"
    return lambda x,y : f"{x} {op} {y}"

def ast_to_glsl(node):
    if isinstance(node, ast.Expression):
        return ast_to_glsl(node.body)
    if isinstance(node, ast.BinOp):
        op_c = node.op.__class__.__name__
        return "(" + name_to_operation(op_c)(
            ast_to_glsl(node.left), 
            ast_to_glsl(node.right)
        ) + ")"
    if isinstance(node, ast.Name):
        return "val" #str(node.id)
    if isinstance(node, ast.Call):
        args = []
        for a in node.args:
            args.append(ast_to_glsl(a))
        return str(node.func.id) +"(" + ", ".join(args) + ")"
    if isinstance(node, ast.Attribute):
        return f"{ast_to_glsl(node.value)}.{node.attr}"
    if isinstance(node, ast.Constant):
        return str(node.value)
    if isinstance(node, ast.UnaryOp):
        op_c = node.op.__class__.__name__
        return name_to_operation(op_c)(ast_to_glsl(node.operand))
    else:
        raise SyntaxError(f"Cannot parse {node.__class__.__name__}.")

def to_glsl(expr):
    ast_parse = ast.parse(expr, '<string>', 'eval')
    return ast_to_glsl(ast_parse)

type_token = '<type>'
expr_token = '<expr>'
name_token = '<name>'

with open("shaders/scripts/function_template.frag.glsl") as f:
    function_template = f.read()

def create_glsl_function(name, vtype, expr):
    return replace_with_all(function_template, [
        (type_token, vtype),
        (name_token, name),
        (expr_token, to_glsl(expr))
    ])