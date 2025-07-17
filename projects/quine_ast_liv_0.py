import os, sys, random, ast, string


def mutate_function_source(source_code, node_name, node_type):
    """
    Parse the source code and target the definition of evolved_function.
    Apply smart AST mutations only to that function.
    """
    tree = ast.parse(source_code)
    for node in ast.walk(tree):
        if isinstance(node, node_type) and node.name == node_name:
            mutType = random.choice([0, 1])
            print(mutType)
            if mutType == 0:
                attach_generated_subtree(node, max_depth=4)
            if mutType == 1:
                mutate_ast_subtree(node, max_depth=2, mutation_prob=0.5)
            break
    mutated_source = ast.unparse(tree)
    return mutated_source

def mutate_ast_subtree(input_node, max_depth=3, mutation_prob=0.3):
    """
    Mutates the given AST subtree by randomly replacing nodes with newly generated random AST nodes.
    The mutation is performed in-place starting from the provided input_node.
    
    :param input_node: The root AST node from which mutations will be applied.
    :param max_depth: Maximum depth for generating new random nodes.
    :param mutation_prob: The probability with which an eligible node is replaced.
    :return: The mutated AST node.
    """
    import ast
    import random

    class RandomMutator(ast.NodeTransformer):

        def __init__(self, max_depth, mutation_prob, in_function=False):
            self.max_depth = max_depth
            self.mutation_prob = mutation_prob
            self.in_function = in_function
            super().__init__()

        def generic_visit(self, node):
            node = super().generic_visit(node)
            if isinstance(node, ast.expr) and random.random() < self.mutation_prob:
                candidate = random_expr(self.max_depth, in_function=self.in_function)
                if isinstance(candidate, type(node)):
                    return candidate
            elif isinstance(node, ast.stmt) and random.random() < self.mutation_prob:
                candidate = random_stmt(self.max_depth, in_function=self.in_function)
                if isinstance(candidate, type(node)):
                    return candidate
            return node

        def visit_FunctionDef(self, node):
            old_in_function = self.in_function
            self.in_function = True
            node = self.generic_visit(node)
            self.in_function = old_in_function
            return node

        def visit_Lambda(self, node):
            old_in_function = self.in_function
            self.in_function = True
            node = self.generic_visit(node)
            self.in_function = old_in_function
            return node
    mutator = RandomMutator(max_depth, mutation_prob)
    mutated = mutator.visit(input_node)
    ast.fix_missing_locations(mutated)
    return mutated

def mutate_ast(node):
    """
    Recursively traverse and smartly mutate AST nodes.
    - For numeric constants, add a small random offset.
    - For binary operations, with some probability, swap the operator.
    """
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        delta = random.choice([i for i in range(-2, 3) if i != 0])
        node.value += delta
    elif isinstance(node, ast.BinOp):
        if random.random() < 0.5:
            ops = [ast.Add(), ast.Sub(), ast.Mult(), ast.Div()]
            node.op = random.choice(ops)
    for field, value in ast.iter_fields(node):
        if isinstance(value, list):
            for item in value:
                if isinstance(item, ast.AST):
                    mutate_ast(item)
        elif isinstance(value, ast.AST):
            mutate_ast(value)
    return node
with open(__file__, 'r') as f:
    base_code = f.read()

def get_identifiers_from_code(base_code: str) -> list:
    """
    Extracts all identifier names from the given Python source code.
    
    This includes names from:
    - Variable and attribute usage (ast.Name)
    - Function definitions (ast.FunctionDef)
    - Class definitions (ast.ClassDef)
    - Function arguments (ast.arg)
    
    :param source_code: A string containing Python source code.
    :return: A list of unique identifier names found in the source code.
    """
    tree = ast.parse(base_code)
    identifiers = set()

    class IdentifierVisitor(ast.NodeVisitor):

        def visit_Name(self, node):
            identifiers.add(node.id)
            self.generic_visit(node)

        def visit_FunctionDef(self, node):
            identifiers.add(node.name)
            self.generic_visit(node)

        def visit_ClassDef(self, node):
            identifiers.add(node.name)
            self.generic_visit(node)

        def visit_arg(self, node):
            identifiers.add(node.arg)
            self.generic_visit(node)
    IdentifierVisitor().visit(tree)
    return list(identifiers)

def random_name():
    names = get_identifiers_from_code(base_code)
    if names and random.random() < 0.9:
        return random.choice(names)
    else:
        length = random.randint(3, 8)
        name = random.choice(string.ascii_lowercase)
        name += ''.join(random.choices(string.ascii_lowercase + string.digits, k=length - 1))
        return name

def random_expr(max_depth, in_function=False):
    """Recursively generate a random ast.expr node."""
    if max_depth <= 0:
        if random.random() < 0.5:
            value_choices = [random.randint(-100, 100), random.uniform(-100, 100), ''.join(random.choices(string.ascii_lowercase, k=5)), True, False, None]
            return ast.Constant(value=random.choice(value_choices))
        else:
            return ast.Name(id=random_name(), ctx=ast.Load())
    expr_type = random.choice([
        'binop', 'boolop', 'unaryop', 'compare', 'call', 'attribute', 'subscript',
        'ifexp', 'lambda', 'list', 'tuple', 'dict', 'set', 'listcomp', 'setcomp',
        'dictcomp', 'genexp', 'namedexpr', 'await', 'joinedstr', 'bytes',
        'ellipsis', 'starred', 'slice'
    ] + (['yield'] if in_function else []))
    if expr_type == 'binop':
        left = random_expr(max_depth - 1, in_function=in_function)
        right = random_expr(max_depth - 1, in_function=in_function)
        op = random.choice([ast.Add(), ast.Sub(), ast.Mult(), ast.Div(), ast.Mod(), ast.Pow(), ast.BitAnd(), ast.BitOr(), ast.BitXor(), ast.LShift(), ast.RShift(), ast.FloorDiv()])
        return ast.BinOp(left=left, op=op, right=right)
    elif expr_type == 'boolop':
        op = random.choice([ast.And(), ast.Or()])
        values = [random_expr(max_depth - 1, in_function=in_function) for _ in range(random.randint(2, 3))]
        return ast.BoolOp(op=op, values=values)
    elif expr_type == 'unaryop':
        op = random.choice([ast.UAdd(), ast.USub(), ast.Not(), ast.Invert()])
        operand = random_expr(max_depth - 1, in_function=in_function)
        return ast.UnaryOp(op=op, operand=operand)
    elif expr_type == 'compare':
        left = random_expr(max_depth - 1, in_function=in_function)
        num_ops = random.randint(1, 3)
        ops = []
        comparators = []
        comp_ops = [ast.Eq(), ast.NotEq(), ast.Lt(), ast.Gt(), ast.LtE(), ast.GtE(), ast.Is(), ast.IsNot(), ast.In(), ast.NotIn()]
        for _ in range(num_ops):
            ops.append(random.choice(comp_ops))
            comparators.append(random_expr(max_depth - 1, in_function=in_function))
        return ast.Compare(left=left, ops=ops, comparators=comparators)
    elif expr_type == 'call':
        func_expr = random_expr(max_depth - 1, in_function=in_function)
        if isinstance(func_expr, ast.Constant):
            func_expr = ast.Name(id=random_name(), ctx=ast.Load())
        args = [random_expr(max_depth - 1, in_function=in_function) for _ in range(random.randint(0, 2))]
        keywords = []
        if random.random() < 0.5:
            kw_name = random_name()
            kw_value = random_expr(max_depth - 1, in_function=in_function)
            keywords.append(ast.keyword(arg=kw_name, value=kw_value))
        return ast.Call(func=func_expr, args=args, keywords=keywords)
    elif expr_type == 'attribute':
        value = random_expr(max_depth - 1, in_function=in_function)
        return ast.Attribute(value=value, attr=random_name(), ctx=ast.Load())
    elif expr_type == 'subscript':
        value = random_expr(max_depth - 1, in_function=in_function)
        index = random_expr(max_depth - 1, in_function=in_function)
        return ast.Subscript(value=value, slice=index, ctx=ast.Load())
    elif expr_type == 'ifexp':
        cond = random_expr(max_depth - 1, in_function=in_function)
        body_expr = random_expr(max_depth - 1, in_function=in_function)
        orelse_expr = random_expr(max_depth - 1, in_function=in_function)
        return ast.IfExp(test=cond, body=body_expr, orelse=orelse_expr)
    elif expr_type == 'lambda':
        num_args = random.randint(0, 2)
        args_list = [ast.arg(arg=random_name(), annotation=None) for _ in range(num_args)]
        lambda_args = ast.arguments(posonlyargs=[], args=args_list, vararg=None, kwonlyargs=[], kw_defaults=[], defaults=[], kwarg=None)
        body = random_expr(max_depth - 1, in_function=in_function)
        return ast.Lambda(args=lambda_args, body=body)
    elif expr_type == 'list':
        elements = [random_expr(max_depth - 1, in_function=in_function) for _ in range(random.randint(0, 3))]
        return ast.List(elts=elements, ctx=ast.Load())
    elif expr_type == 'tuple':
        elements = [random_expr(max_depth - 1, in_function=in_function) for _ in range(random.randint(0, 3))]
        return ast.Tuple(elts=elements, ctx=ast.Load())
    elif expr_type == 'dict':
        n = random.randint(0, 3)
        keys = [random_expr(max_depth - 1, in_function=in_function) for _ in range(n)]
        values = [random_expr(max_depth - 1, in_function=in_function) for _ in range(n)]
        return ast.Dict(keys=keys, values=values)
    elif expr_type == 'set':
        elements = [random_expr(max_depth - 1, in_function=in_function) for _ in range(random.randint(1, 3))]
        return ast.Set(elts=elements)
    elif expr_type in ('listcomp', 'setcomp', 'dictcomp', 'genexp'):
        target = ast.Name(id=random_name(), ctx=ast.Store())
        iter_expr = random_expr(max_depth - 1, in_function=in_function)
        if random.random() < 0.5:
            if_cond = random_expr(max_depth - 1, in_function=in_function)
            comp = ast.comprehension(target=target, iter=iter_expr, ifs=[if_cond], is_async=0)
        else:
            comp = ast.comprehension(target=target, iter=iter_expr, ifs=[], is_async=0)
        if expr_type == 'listcomp':
            elt = random_expr(max_depth - 1, in_function=in_function)
            return ast.ListComp(elt=elt, generators=[comp])
        elif expr_type == 'setcomp':
            elt = random_expr(max_depth - 1, in_function=in_function)
            return ast.SetComp(elt=elt, generators=[comp])
        elif expr_type == 'genexp':
            elt = random_expr(max_depth - 1, in_function=in_function)
            return ast.GeneratorExp(elt=elt, generators=[comp])
        elif expr_type == 'dictcomp':
            key = random_expr(max_depth - 1, in_function=in_function)
            value = random_expr(max_depth - 1, in_function=in_function)
            return ast.DictComp(key=key, value=value, generators=[comp])
    elif expr_type == 'namedexpr':
        target = ast.Name(id=random_name(), ctx=ast.Store())
        value = random_expr(max_depth - 1, in_function=in_function)
        return ast.NamedExpr(target=target, value=value)
    elif expr_type == 'yield':
        if random.random() < 0.5:
            val = random_expr(max_depth - 1, in_function=in_function)
            return ast.Yield(value=val)
        else:
            val = random_expr(max_depth - 1, in_function=in_function)
            return ast.YieldFrom(value=val)

    # Extended expression types
    elif expr_type == 'await':
        return ast.Await(value=random_expr(max_depth - 1, in_function=in_function))
    elif expr_type == 'joinedstr':
        fragments = []
        for _ in range(random.randint(1, 3)):
            if random.random() < 0.5:
                fragments.append(ast.Constant(value=''.join(random.choices(string.ascii_lowercase, k=random.randint(1,5)))))
            else:
                fragments.append(ast.FormattedValue(value=random_expr(max_depth - 1, in_function=in_function), conversion=-1))
        return ast.JoinedStr(values=fragments)
    elif expr_type == 'bytes':
        length = random.randint(1, 4)
        value = bytes(random.randint(0, 255) for _ in range(length))
        return ast.Constant(value=value)
    elif expr_type == 'ellipsis':
        return ast.Constant(value=Ellipsis)
    elif expr_type == 'starred':
        return ast.Starred(value=random_expr(max_depth - 1, in_function=in_function), ctx=ast.Load())
    elif expr_type == 'slice':
        lower = random_expr(max_depth - 1, in_function=in_function)
        upper = random_expr(max_depth - 1, in_function=in_function)
        step = random_expr(max_depth - 1, in_function=in_function)
        return ast.Slice(lower=lower, upper=upper, step=step)

def random_stmt(max_depth, in_function=False, in_loop=False):
    """Recursively generate a random ast.stmt node."""
    if max_depth <= 0:
        simple_opts = []
        if in_loop:
            simple_opts += ['break', 'continue']
        if in_function:
            simple_opts += ['return']
        simple_opts += ['pass', 'expr']
        choice = random.choice(simple_opts)
        if choice == 'break':
            return ast.Break()
        elif choice == 'continue':
            return ast.Continue()
        elif choice == 'return':
            if random.random() < 0.5:
                return ast.Return(value=None)
            else:
                return ast.Return(value=random_expr(0, in_function=in_function))
        elif choice == 'pass':
            return ast.Pass()
        elif choice == 'expr':
            return ast.Expr(value=random_expr(0, in_function=in_function))
    stmt_type = random.choice([
        'assign', 'augassign', 'if', 'for', 'async_for', 'while',
        'funcdef', 'async_funcdef', 'annassign', 'class',
        'with', 'async_with', 'try', 'expr', 'return',
        'import', 'importfrom', 'global', 'delete',
        'assert', 'raise', 'nonlocal', 'match'
    ])
    if stmt_type == 'return' and (not in_function):
        stmt_type = 'expr'
    if stmt_type in ('break', 'continue'):
        stmt_type = 'pass'
    if stmt_type == 'assign':
        num_targets = random.randint(1, 2)
        targets = [ast.Name(id=random_name(), ctx=ast.Store()) for _ in range(num_targets)]
        value = random_expr(max_depth - 1, in_function=in_function)
        return ast.Assign(targets=targets, value=value)
    elif stmt_type == 'augassign':
        target = ast.Name(id=random_name(), ctx=ast.Store())
        op = random.choice([ast.Add(), ast.Sub(), ast.Mult(), ast.Div(), ast.Mod(), ast.Pow(), ast.BitAnd(), ast.BitOr(), ast.BitXor(), ast.LShift(), ast.RShift(), ast.FloorDiv()])
        value = random_expr(max_depth - 1, in_function=in_function)
        return ast.AugAssign(target=target, op=op, value=value)
    elif stmt_type == 'if':
        test = random_expr(max_depth - 1, in_function=in_function)
        body_count = random.randint(1, 3)
        orelse_count = random.randint(0, 2)
        body = [random_stmt(max_depth - 1, in_function=in_function, in_loop=in_loop) for _ in range(body_count)]
        orelse = [random_stmt(max_depth - 1, in_function=in_function, in_loop=in_loop) for _ in range(orelse_count)] if orelse_count > 0 else []
        return ast.If(test=test, body=body, orelse=orelse)
    elif stmt_type == 'for':
        target = ast.Name(id=random_name(), ctx=ast.Store())
        iter_expr = random_expr(max_depth - 1, in_function=in_function)
        body_count = random.randint(1, 3)
        orelse_count = random.randint(0, 1)
        body = [random_stmt(max_depth - 1, in_function=in_function, in_loop=True) for _ in range(body_count)]
        orelse = [random_stmt(max_depth - 1, in_function=in_function, in_loop=in_loop) for _ in range(orelse_count)] if orelse_count > 0 else []
        return ast.For(target=target, iter=iter_expr, body=body, orelse=orelse)
    elif stmt_type == 'while':
        test = random_expr(max_depth - 1, in_function=in_function)
        body_count = random.randint(1, 3)
        orelse_count = random.randint(0, 1)
        body = [random_stmt(max_depth - 1, in_function=in_function, in_loop=True) for _ in range(body_count)]
        orelse = [random_stmt(max_depth - 1, in_function=in_function, in_loop=in_loop) for _ in range(orelse_count)] if orelse_count > 0 else []
        return ast.While(test=test, body=body, orelse=orelse)
    elif stmt_type == 'funcdef':
        name = random_name()
        args_count = random.randint(0, 3)
        params = [ast.arg(arg=random_name(), annotation=None) for _ in range(args_count)]
        arguments = ast.arguments(posonlyargs=[], args=params, vararg=None, kwonlyargs=[], kw_defaults=[], defaults=[], kwarg=None)
        body_count = random.randint(1, 3)
        body = [random_stmt(max_depth - 1, in_function=True, in_loop=False) for _ in range(body_count)]
        if not body:
            body = [ast.Pass()]
        func_node = ast.FunctionDef(name=name, args=arguments, body=body, decorator_list=[], returns=None)
        if hasattr(ast.FunctionDef, '_fields') and 'type_params' in ast.FunctionDef._fields:
            func_node.type_params = []
        if hasattr(ast.FunctionDef, '_fields') and 'type_comment' in ast.FunctionDef._fields:
            func_node.type_comment = None
        return func_node
    elif stmt_type == 'class':
        name = random_name().capitalize()
        bases = []
        if random.random() < 0.5:
            bases.append(ast.Name(id='object', ctx=ast.Load()))
        body_count = random.randint(1, 3)
        body = [random_stmt(max_depth - 1, in_function=False, in_loop=False) for _ in range(body_count)]
        if not body:
            body = [ast.Pass()]
        class_node = ast.ClassDef(name=name, bases=bases, keywords=[], body=body, decorator_list=[])
        if hasattr(ast.ClassDef, '_fields') and 'type_params' in ast.ClassDef._fields:
            class_node.type_params = []
        return class_node
    elif stmt_type == 'with':
        num_items = random.randint(1, 2)
        items = []
        for _ in range(num_items):
            context_expr = random_expr(max_depth - 1, in_function=in_function)
            if random.random() < 0.5:
                optional_vars = ast.Name(id=random_name(), ctx=ast.Store())
            else:
                optional_vars = None
            items.append(ast.withitem(context_expr=context_expr, optional_vars=optional_vars))
        body_count = random.randint(1, 3)
        body = [random_stmt(max_depth - 1, in_function=in_function, in_loop=in_loop) for _ in range(body_count)]
        if not body:
            body = [ast.Pass()]
        node = ast.With(items=items, body=body)
        if hasattr(ast.With, '_fields') and 'type_comment' in ast.With._fields:
            node.type_comment = None
        return node
    elif stmt_type == 'try':
        body_count = random.randint(1, 3)
        body = [random_stmt(max_depth - 1, in_function=in_function, in_loop=in_loop) for _ in range(body_count)]
        if not body:
            body = [ast.Pass()]
        handlers = []
        orelse = []
        finalbody = []
        if random.random() < 0.7:
            num_handlers = random.randint(1, 2)
            for _ in range(num_handlers):
                exc_type = ast.Name(id='Exception', ctx=ast.Load()) if random.random() < 0.5 else None
                exc_name = random_name() if random.random() < 0.5 else None
                h_body_count = random.randint(1, 2)
                h_body = [random_stmt(max_depth - 1, in_function=in_function, in_loop=in_loop) for _ in range(h_body_count)]
                if not h_body:
                    h_body = [ast.Pass()]
                handlers.append(ast.ExceptHandler(type=exc_type, name=exc_name, body=h_body))
            if random.random() < 0.5:
                else_count = random.randint(1, 2)
                orelse = [random_stmt(max_depth - 1, in_function=in_function, in_loop=in_loop) for _ in range(else_count)]
        if not handlers or random.random() < 0.5:
            final_count = random.randint(1, 2)
            finalbody = [random_stmt(max_depth - 1, in_function=in_function, in_loop=in_loop) for _ in range(final_count)]
            if not finalbody:
                finalbody = [ast.Pass()]
        return ast.Try(body=body, handlers=handlers, orelse=orelse, finalbody=finalbody)
    elif stmt_type == 'expr':
        return ast.Expr(value=random_expr(max_depth - 1, in_function=in_function))
    elif stmt_type == 'import':
        num_names = random.randint(1, 2)
        names = [ast.alias(name=random_name(), asname=None) for _ in range(num_names)]
        return ast.Import(names=names)
    elif stmt_type == 'importfrom':
        module_name = random_name()
        num_names = random.randint(1, 2)
        aliases = [ast.alias(name=random_name(), asname=None) for _ in range(num_names)]
        level = random.choice([0, 0, 1])
        return ast.ImportFrom(module=module_name, names=aliases, level=level)
    elif stmt_type == 'global':
        num_vars = random.randint(1, 2)
        names = [random_name() for _ in range(num_vars)]
        return ast.Global(names=names)

    # Extended statement types
    elif stmt_type == 'delete':
        num_targets = random.randint(1, 2)
        targets = [ast.Name(id=random_name(), ctx=ast.Del()) for _ in range(num_targets)]
        return ast.Delete(targets=targets)
    elif stmt_type == 'assert':
        test = random_expr(max_depth - 1, in_function=in_function)
        msg = None if random.random() < 0.5 else random_expr(max_depth - 1, in_function=in_function)
        return ast.Assert(test=test, msg=msg)
    elif stmt_type == 'raise':
        exc = random_expr(max_depth - 1, in_function=in_function)
        return ast.Raise(exc=exc, cause=None)
    elif stmt_type == 'nonlocal':
        num_vars = random.randint(1, 2)
        names = [random_name() for _ in range(num_vars)]
        return ast.Nonlocal(names=names)
    elif stmt_type == 'annassign':
        target = ast.Name(id=random_name(), ctx=ast.Store())
        annotation = random_expr(max_depth - 1, in_function=in_function)
        value = random_expr(max_depth - 1, in_function=in_function) if random.random() < 0.5 else None
        return ast.AnnAssign(target=target, annotation=annotation, value=value, simple=1)
    elif stmt_type == 'async_for':
        target = ast.Name(id=random_name(), ctx=ast.Store())
        iter_expr = random_expr(max_depth - 1, in_function=in_function)
        body_count = random.randint(1, 3)
        body = [random_stmt(max_depth - 1, in_function=in_function, in_loop=True) for _ in range(body_count)]
        orelse_count = random.randint(0, 1)
        orelse = [random_stmt(max_depth - 1, in_function=in_function, in_loop=in_loop) for _ in range(orelse_count)] if orelse_count > 0 else []
        return ast.AsyncFor(target=target, iter=iter_expr, body=body, orelse=orelse)
    elif stmt_type == 'async_funcdef':
        name = random_name()
        args_count = random.randint(0, 3)
        params = [ast.arg(arg=random_name(), annotation=None) for _ in range(args_count)]
        arguments = ast.arguments(posonlyargs=[], args=params, vararg=None, kwonlyargs=[], kw_defaults=[], defaults=[], kwarg=None)
        body_count = random.randint(1, 3)
        body = [random_stmt(max_depth - 1, in_function=True, in_loop=False) for _ in range(body_count)]
        if not body:
            body = [ast.Pass()]
        return ast.AsyncFunctionDef(name=name, args=arguments, body=body, decorator_list=[], returns=None)
    elif stmt_type == 'async_with':
        num_items = random.randint(1, 2)
        items = []
        for _ in range(num_items):
            context_expr = random_expr(max_depth - 1, in_function=in_function)
            optional_vars = ast.Name(id=random_name(), ctx=ast.Store()) if random.random() < 0.5 else None
            items.append(ast.withitem(context_expr=context_expr, optional_vars=optional_vars))
        body_count = random.randint(1, 3)
        body = [random_stmt(max_depth - 1, in_function=in_function, in_loop=in_loop) for _ in range(body_count)]
        if not body:
            body = [ast.Pass()]
        return ast.AsyncWith(items=items, body=body)
    elif stmt_type == 'match':
        subject = random_expr(max_depth - 1, in_function=in_function)
        pat = ast.MatchValue(value=random_expr(max_depth - 1, in_function=in_function))
        case_body = [random_stmt(max_depth - 1, in_function=in_function, in_loop=in_loop)]
        case = ast.match_case(pattern=pat, guard=None, body=case_body)
        return ast.Match(subject=subject, cases=[case])

def generate_random_ast(max_depth=3):
    """Generate a random AST for a module (ast.Module) with given max depth."""
    num_statements = random.randint(1, 3)
    body = [random_stmt(max_depth, in_function=False, in_loop=False) for _ in range(num_statements)]
    if not body:
        body = [ast.Pass()]
    module_node = ast.Module(body=body, type_ignores=[])
    ast.fix_missing_locations(module_node)
    return module_node

def get_terminal_leaves(node):
    """
    Recursively traverse the AST to find terminal leaves.
    Terminal leaves are nodes without children.
    """
    leaves = []
    if not isinstance(node, ast.AST):
        return [node]
    for field, value in ast.iter_fields(node):
        if isinstance(value, list):
            for item in value:
                leaves.extend(get_terminal_leaves(item))
        elif isinstance(value, ast.AST):
            leaves.extend(get_terminal_leaves(value))
    return leaves

def attach_to_random_leaf(node, max_depth):
    """
    Attach the generated subtree to a random terminal leaf of the AST.
    """
    leaves = get_terminal_leaves(node)
    if leaves:
        random_leaf = random.choice(leaves)
        attach_generated_subtree(random_leaf, max_depth)

def attach_generated_subtree(input_node, max_depth=3):
    """
    Given an input AST node, attach a randomly generated subtree to it.
    
    This function searches for a field in the node that is a list (typically the 'body' field)
    and appends a new randomly generated statement (or statement list) to that field.
    It respects context (e.g. if the node is a FunctionDef, it generates statements accordingly).
    
    Raises a ValueError if no list-type field is found.
    """
    if hasattr(input_node, 'body') and isinstance(input_node.body, list):
        in_func = isinstance(input_node, ast.FunctionDef)
        new_stmt = random_stmt(max_depth, in_function=in_func)
        input_node.body.append(new_stmt)
        return input_node
    for field in getattr(input_node, '_fields', []):
        field_val = getattr(input_node, field)
        if isinstance(field_val, list):
            new_stmt = random_stmt(max_depth, in_function=False)
            field_val.append(new_stmt)
            return input_node
    raise ValueError('Input node does not have a list attribute to attach a new subtree.')

def main(index):
    try:
        with open(f'quine_ast_liv_{index-1}.py', 'r') as file:
            content = file.read()
    except FileNotFoundError:
        content = ''
    except IOError as e:
        content = ''
    source_code = content
    node_name = 'evolved_function'
    node_type = ast.FunctionDef
    new_source = mutate_function_source(source_code, node_name, node_type)
    new_file = f'quine_ast_liv_{index}.py'

    try:
        code_object = compile(new_source, "temp_file.py", "exec")
    except SyntaxError as e:
        new_source = source_code

    #visualize_ast_tree(source_code, output_filename=f'ast_visualization_{index}', format='png', view=False, cleanup=True, node_name=node_name)

    with open(new_file, 'w') as f:
        f.write(new_source)
    os.execl(sys.executable, sys.executable, new_file)

def evolved_function():
    """
    A function that performs a simple calculation.
    The behavior of this function will evolve over generations.
    """
    a = 10
    b = 5
    result = a + b  # this operation may change over generations!
    print("Result:", result)

if __name__ == '__main__':
    import sys
    import traceback
    current_file = sys.argv[0]
    print('Current file:', current_file)
    if current_file.startswith('quine_ast_liv_') and current_file.endswith('.py'):
        current_index = int(current_file[14:-3])
    else:
        current_index = 0

    new_index = current_index + 1
    mutation_successful = False
    mutTry = 5
    for attempt in range(1, mutTry + 1):
        try:
            evolved_function()
            main(new_index)
            mutation_successful = True
            break
        except Exception as e:
            print(f'Mutation attempt {attempt} failed:')

    if not mutation_successful:
        fallback_index = current_index - 1
        print(f'Mutation failed after {mutTry} attempts. Reverting to file with index {fallback_index}.')
        if fallback_index == 0:
            fallback_index=1
            mutTry = 100
        for attempt in range(1, mutTry + 1):
            try:
                main(fallback_index)
                mutation_successful = True
                break
            except Exception as e:
                print(f'Mutation attempt {attempt} failed:')