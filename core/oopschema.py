import inspect

registry={}

def annot(type):
    map={
        str: "string",
        int: "integer",
        float: "float",
        bool: "boolean"
    }
    return map.get(type,"string")

def properties(fn):
    properties={}
    required=[]
    for i,j in inspect.signature(fn).parameters.items():
        if i=="self":
            continue

        properties[i]= {"type":annot(j.annotation)}

        if j.default is inspect.Parameter.empty:
            required.append(i)

    return properties,required



def Tool():
    def genschema(cls):
        clschm=[]
        for i,j in inspect.getmembers(cls,inspect.isfunction):
            property,required=properties(j)
            schema={
            "type":"function",
            "function":{
                "name": f"{cls.__name__}::{i}",
                "description": j.__doc__,
                "parameters": {
                    "type": "object",
                    "properties": property
                    },
                "required": required
                }
            }
            clschm.append(schema)

        registry[cls.__name__]={
            "instance": cls(),
            "schemas":clschm
        }

        return cls
    return genschema