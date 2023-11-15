import ast
from string import ascii_lowercase

operators = {
    ast.Add: "+",
    ast.Sub: "-",
    ast.Mult: "*",
    ast.Div: "/",
    ast.Pow: "**",
    ast.USub: "-",  # unary -1
    ast.UAdd: "+"  # unary +1
}


def prepare_expression(text_expression):
    parsed_expression = parse_expression(text_expression)
    return eval("lambda **kwargs: " + parsed_expression)


def parse_expression(text_expression):
    node = ast.parse(text_expression, mode='eval')
    body = node.body

    return ast_walk(body)


def ast_walk(node):
    if isinstance(node, ast.Num) and isinstance(node.n, int):
        return str(node.n)
    elif isinstance(node, ast.BinOp):
        left = ast_walk(node.left)
        right = ast_walk(node.right)
        op_char = operators[type(node.op)]

        return "({}{}{})".format(left, op_char, right)
    elif isinstance(node, ast.UnaryOp):
        return operators[type(node.op)] + ast_walk(node.operand)
    elif isinstance(node, ast.Name) and len(node.id) == 1 and \
            node.id in ascii_lowercase:
        return "kwargs['{}']".format(node.id)
    else:
        raise TypeError(node)


def view_evaluated_expresion(text_expression, **kwargs):
    expression = prepare_expression(text_expression)
    expression_value = expression(**kwargs)

    parameters = ["{0}={1}".format(key, value)
                  for key, value in kwargs.items()]

    parameters_repr = ", ".join(parameters)
    echo_format = "{0}, {{{1}}} = {2}"

    return echo_format.format(text_expression, parameters_repr,
                              expression_value)


if __name__ == "__main__":
    num_of_samples = 10
    for i in range(num_of_samples):
        print(view_evaluated_expresion("(4*i**3)-4*(t+-9)*t", t=i, i=i * i))