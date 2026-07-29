import inspect

tool_registry={}

py_to_json={
    int: "integer",
    str: "string",
    bool: "boolean",
    float: "floating number"
}

def tool(Description:str ):
    def wrapper(func):
        signature=inspect.signature(func)
        properties={}
        required=[]
        for name,parameter in signature.parameters.items():
            properties[name]={"type":py_to_json.get(name,"string")}
            if parameter.default == inspect.Parameter.empty:
                    required.append(name)
        schema={
                "type": "function",
                "function": {
                    "name": func.__name__,
                    "description": Description or func.__doc__ or "",
                    "parameters": {
                        "type": "object",
                        "properties": properties,
                        "required": required
                    }
                }
            }

        func.schema=schema
        tool_registry[func.__name__]={
             "function": func,
             "schema": func.schema
        }
        return func
    return wrapper
