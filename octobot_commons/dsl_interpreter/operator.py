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
import typing
import numpy as np

import octobot_commons.constants

OperatorParameterType = typing.Union[str, int, float, bool, None, list, np.ndarray, "Operator"]
ComputedOperatorParameterType = typing.Union[str, int, float, bool, None, list, np.ndarray]


class Operator:
    """
    Operator class is used to represent an operator in the DSL.
    It can have one or more parameters which are used to compute the result of the operator.
    """

    def __init__(self, *parameters: OperatorParameterType, **kwargs: typing.Any):
        self.parameters = parameters
        self.kwargs = kwargs

    @staticmethod
    def get_name() -> str:
        """
        Get the name of the operator, as seen in the DSL expression.
        """
        raise NotImplementedError("get_name is not implemented")

    @staticmethod
    def get_library() -> str:
        """
        Get the library of the operator.
        """
        return octobot_commons.constants.BASE_OPERATORS_LIBRARY

    async def initialize(self) -> None:
        """
        Initialize the operator, override if necessary.
        Will always be called before compute()
        """
        for parameter in self.parameters:
            if isinstance(parameter, Operator):
                await parameter.initialize()

    def compute(self) -> ComputedOperatorParameterType:
        """
        Compute the result of the operator considering its computed parameters.
        """
        raise NotImplementedError("compute is not implemented")

    def get_computed_parameters(self) -> typing.List[ComputedOperatorParameterType]:
        """
        Get the computed parameters of the operator.
        Here computed means that any nested operator has already been computed.
        """
        return [
            parameter.compute() if isinstance(parameter, Operator) else parameter
            for parameter in self.parameters
        ]
