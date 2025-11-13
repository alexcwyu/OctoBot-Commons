# pylint: disable=too-many-branches,too-many-return-statements
#  Drakkar-Software OctoBot-Commons
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import ast
import typing
import octobot_commons.dsl_interpreter.operator as dsl_interpreter_operator


class Interpreter:
    """
    Interpreter class for parsing and interpreting DSL expressions.
    Maps AST elements to Operator instances based on operator names.
    """

    def __init__(
        self, operators: typing.List[typing.Type[dsl_interpreter_operator.Operator]]
    ):
        """
        Initialize the interpreter with a list of operator classes.

        Args:
            operators: List of Operator subclasses to be used for interpretation
        """
        # Save operators as a dictionary mapping operator name to operator class
        self.operators_by_name: typing.Dict[
            str, typing.Type[dsl_interpreter_operator.Operator]
        ] = {operator_class.get_name(): operator_class for operator_class in operators}
        self._operator_tree_or_constant: typing.Union[
            dsl_interpreter_operator.Operator,
            dsl_interpreter_operator.ComputedOperatorParameterType,
        ] = None

    async def interprete(
        self, expression: str
    ) -> dsl_interpreter_operator.ComputedOperatorParameterType:
        """
        Interpret a string expression by parsing it with AST and mapping to operators.

        Args:
            expression: String expression to interpret

        Returns:
            Operator instance or literal value representing the interpreted expression
        """
        self.parse_expression(expression)
        return await self.compute_expression()

    def parse_expression(self, expression: str):
        """
        Parse the expression into an AST and store the result in self._operator_tree_or_constant.
        """
        # Parse the expression into an AST
        # mode:  can be 'exec' if source consists of a sequence of statements, 'eval' if
        # it consists of a single expression, or 'single' if it consists of a single
        # interactive statement.
        # docs: https://docs.python.org/3/library/functions.html#compile
        tree = ast.parse(expression, mode="eval")

        # Visit the AST and convert nodes to Operator instances
        self._operator_tree_or_constant = self._visit_node(tree.body)

    async def compute_expression(
        self,
    ) -> dsl_interpreter_operator.ComputedOperatorParameterType:
        """
        Compute the result of the expression stored in self._operator_tree_or_constant.
        If the expression is a constant, return it directly.
        If the expression is an operator, initialize it and compute its result.
        """
        if isinstance(
            self._operator_tree_or_constant, dsl_interpreter_operator.Operator
        ):
            await self._operator_tree_or_constant.initialize()
            return self._operator_tree_or_constant.compute()
        return self._operator_tree_or_constant

    def _visit_node(
        self, node: ast.AST
    ) -> typing.Union[
        dsl_interpreter_operator.Operator,
        dsl_interpreter_operator.ComputedOperatorParameterType,
    ]:
        """
        Recursively visit AST nodes and convert them to Operator instances or values.

        Args:
            node: AST node to visit

        Returns:
            Operator instance or literal value representing the node
        """
        if isinstance(node, ast.Call):
            # Function call: func(arg1, arg2, ...)
            func_name = self._get_name_from_node(node.func)
            if func_name in self.operators_by_name:
                operator_class = self.operators_by_name[func_name]
                # Convert arguments to Operator instances or values
                args = [
                    self._get_value_from_constant_node(arg)
                    if isinstance(arg, ast.Constant)
                    else self._visit_node(arg)
                    for arg in node.args
                ]
                return operator_class(*args)
            raise ValueError(f"Unknown operator: {func_name}")

        if isinstance(node, ast.BinOp):
            # Binary operation: left op right
            op_name = type(node.op).__name__
            if op_name in self.operators_by_name:
                operator_class = self.operators_by_name[op_name]
                left = self._visit_node(node.left)
                right = self._visit_node(node.right)
                return operator_class(left, right)
            raise ValueError(f"Unknown binary operator: {op_name}")

        if isinstance(node, ast.UnaryOp):
            # Unary operation: op operand
            op_name = type(node.op).__name__
            if op_name in self.operators_by_name:
                operator_class = self.operators_by_name[op_name]
                operand = self._visit_node(node.operand)
                return operator_class(operand)
            raise ValueError(f"Unknown unary operator: {op_name}")

        if isinstance(node, ast.Compare):
            # Comparison: left op right
            if len(node.ops) == 1 and len(node.comparators) == 1:
                op_name = type(node.ops[0]).__name__
                if op_name in self.operators_by_name:
                    operator_class = self.operators_by_name[op_name]
                    left = self._visit_node(node.left)
                    right = self._visit_node(node.comparators[0])
                    return operator_class(left, right)
                raise ValueError(f"Unknown comparison operator: {op_name}")
            raise ValueError("Multiple comparisons not supported")

        if isinstance(node, (ast.Constant)):
            # Literal values: numbers, strings, booleans, None
            return self._get_value_from_constant_node(node)

        if isinstance(node, ast.Name):
            # Name reference: look up in operators_by_name
            name = node.id
            if name in self.operators_by_name:
                operator_class = self.operators_by_name[name]
                return operator_class()
            raise ValueError(f"Unknown name: {name}")

        if isinstance(node, ast.BoolOp):
            # Boolean operation: left op right
            op_name = type(node.op).__name__
            if op_name in self.operators_by_name:
                operator_class = self.operators_by_name[op_name]
                operands = [self._visit_node(operand) for operand in node.values]
                return operator_class(*operands)
            raise ValueError(f"Unknown BoolOp operator: {op_name}")

        if isinstance(node, ast.IfExp):
            # If expression: "body if test else orelse"
            op_name = ast.IfExp.__name__
            if op_name in self.operators_by_name:
                operator_class = self.operators_by_name[op_name]
                test = self._visit_node(node.test)
                body = self._visit_node(node.body)
                orelse = self._visit_node(node.orelse)
                return operator_class(test, body, orelse)
            raise ValueError(f"Unknown IfExp operator: {op_name}")

        raise ValueError(f"Unsupported AST node type: {type(node).__name__}")

    def _get_name_from_node(self, node: ast.AST) -> str:
        """Extract the name from a function node."""
        if isinstance(node, ast.Name):
            return node.id
        # elif isinstance(node, ast.Attribute): ex: snake.colour => not supported
        #     return node.attr
        raise ValueError(f"Cannot extract name from node type: {type(node).__name__}")

    def _get_value_from_constant_node(
        self, node: ast.Constant
    ) -> dsl_interpreter_operator.ComputedOperatorParameterType:
        """Extract a literal value from an AST constant node."""
        value = node.value
        # Filter out unsupported types like complex numbers or Ellipsis
        if isinstance(value, (str, int, float, bool, type(None))):
            return value
        raise ValueError(f"Unsupported constant type: {type(value).__name__}")
