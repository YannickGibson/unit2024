
import json
import openai
import pathlib

def print_and_read(path: pathlib.Path):
    print(f"gonna read {str(path)}")
    return path.read_text(encoding="utf-8")

SYSMSG = print_and_read(pathlib.Path("./sysmsg.txt"))

SPECIALIZATION_INFOS = {
    fpath.name[:-4]: print_and_read(fpath)
    for fpath in pathlib.Path("./specialization-info").iterdir()
    if fpath.is_file() and fpath.name.endswith(".txt")
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "description": "Prints information about the given specialization.",
            "name": "specialization_info",
            "parameters": {
                "type": "object",
                "properties": {
                    "specialization": {
                        "type": "string",
                        "enum": [
                            "information-sceurity",
                            "bussiness-informatics",
                            "computer-graphics",
                            "computer-engineering",
                            "computer-networks-and-internet",
                            "computer-systems-and-virtualization",
                            "software-engineering",
                            "computer-science",
                            "artificial-intelligence",
                            "web-engineering",
                        ],
                        "description": "The specialization to retrieve information about.",
                    },
                },
                "required": ["specialization"]
            },
        }
    }
]

class Chatbot:
    def __init__(self, client: openai.Client, model: str):
        self._client = client
        self._model = model
        self._messages = [
            { "role": "system", "content": SYSMSG }
        ]

    def chat(self, msg: str):
        self._messages.append({ "role": "user", "content": msg })
        res = self._client.chat.completions.create(
            model=self._model,
            messages=self._messages,
            tools=TOOLS,
            n=1,
        ).choices[0].message
        
        if res.tool_calls:
            for tool_call in res.tool_calls:
                if tool_call.function.name == "specialization_info":
                    try:
                        args_dict = json.loads(tool_call.function.arguments)
                        specialization = args_dict["specialization"]
                        specialization_info = SPECIALIZATION_INFOS[specialization]
                        self._messages.append({
                            "role": "function",
                            "tool_call_id": tool_call.id,
                            "name": tool_call.function.name,
                            "content": specialization_info,
                        })
                    except:
                        self._messages.append({
                            "role": "function",
                            "tool_call_id": tool_call.id,
                            "name": tool_call.function.name,
                            "content": "(invalid function call)",
                        })
                else:
                    self._messages.append({
                        "role": "function",
                        "tool_call_id": tool_call.id,
                        "name": tool_call.function.name,
                        "content": "(unknown function)",
                    })

            res = self._client.chat.completions.create(
                model=self._model,
                messages=self._messages,
                tools=TOOLS,
                n=1,
            ).choices[0].message
        
        self._messages.append({ "role": "assistant", "content": res.content })
        return res.content
