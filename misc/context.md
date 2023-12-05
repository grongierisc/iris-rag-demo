# 1. interoperability-embedded-python

# Too long, didn't read

Iop is a framework that allows you to use Python code in Interoperability productions of IRIS.
It's main module is grongier.pex.

You can use it in two ways :
* Register your components in the management portal
* Use the command line
  * The command line is available since version 2.3.1
  * The name of the command line is iop

## Example of a component :
```python
from grongier.pex import BusinessOperation

class FileOperation(BusinessOperation):
    """
    This operation receive a PostMessage and write the content of the post
    inside a file.
    """
    def on_message(self, request):
        with open("/tmp/"+request.post.title+".txt", "w") as file:
            file.write(request.post.selftext)
```

## How to register a component :
```python
from grongier.pex import Utils

Utils.register_component("MyCombinedBusinessOperation","MyCombinedBusinessOperation","/irisdev/app/src/python/demo/",1,"PEX.MyCombinedBusinessOperation")
```

## settings.py file
```python
import bp

CLASSES = {
    'Python.FilterPostRoutingRule': bp.FilterPostRoutingRule,
}
```

