import ast

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
        return f"{node.value.id}.{node.attr}"
    if isinstance(node, ast.Constant):
        return str(node.value)
    if isinstance(node, ast.UnaryOp):
        op_c = node.op.__class__.__name__
        return name_to_operation(op_c)(ast_to_glsl(node.operand))
    else:
        raise SyntaxError(f"Cannot parse {node.__class__.__name__}.")


class ShaderCompiler:
    def __init__(self):
        with open("shaders/fragments/function_template.frag,glsl") as f:
            self.function_template = f.read()

        self.type_token = '<type>'
        self.expr_token = '<expr>'
        self.name_token = '<name>'

        self.glsl_version = '#version 330'

    def create_glsl_function(self, name, vtype, expr):
        temp = self.function_template.replace(self.type_token, vtype)
        temp = temp.replace(self.name_token, name)
        temp = temp.replace(self.expr_token, self.to_glsl(expr))
        return temp

    def to_glsl(self, expr):
        ast_parse = ast.parse(expr, '<string>', 'eval')
        return ast_to_glsl(ast_parse)

    def compile(self, context):
        vertex_shader = self.build_vertex_shader()
        fragment_shader = self.build_fragment_shader()
        return context.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader,
        )
