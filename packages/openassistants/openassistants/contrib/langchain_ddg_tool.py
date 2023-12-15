from typing import Literal, Sequence

from langchain.tools.ddg_search.tool import DuckDuckGoSearchAPIWrapper
from openassistants.data_models.function_input import BaseJSONSchema
from openassistants.data_models.function_output import FunctionOutput, TextOutput
from openassistants.functions.base import BaseFunction, FunctionExecutionDependency
from openassistants.functions.utils import AsyncStreamVersion


class DuckDuckGoToolFunction(BaseFunction):
    type: Literal["DuckDuckGoToolFunction"] = "DuckDuckGoToolFunction"
    parameters: BaseJSONSchema

    async def execute(
        self, deps: FunctionExecutionDependency
    ) -> AsyncStreamVersion[Sequence[FunctionOutput]]:
        try:
            if "query" in deps.arguments:
                query = deps.arguments["query"]
                search = DuckDuckGoSearchAPIWrapper()

                results = search.results(query, max_results=4, source="text")
                formatted_results = "\n\n".join(
                    f"**{result['title']}**  \n_{result['snippet']}_"
                    for index, result in enumerate(results)
                )
                yield [
                    TextOutput(
                        text=f"Found this on DuckDuckGo: \n\n{formatted_results}"
                    )
                ]
            else:
                raise ValueError(
                    f"Query not found in arguments for action function: {self.id}"
                )
        except Exception as e:
            raise RuntimeError(
                f"Error while executing action function {self.id}. function raised: {e}"
            ) from e

    async def get_parameters_json_schema(self) -> dict:
        return self.parameters.json_schema
