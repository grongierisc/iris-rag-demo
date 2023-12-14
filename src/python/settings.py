from rag.bo import ChatOperation, VectorOperation
from rag.bs import ChatService
from rag.bp import ChatProcess

CLASSES = {
    "Python.ChatService": ChatService,
    "Python.ChatOperation": ChatOperation,
    "Python.ChatProcess": ChatProcess,
    "Python.VectorOperation": VectorOperation
}

PRODUCTIONS = [{
    "Chat.Production": {
        "@Name": "Chat.Production",
        "@TestingEnabled": "true",
        "@LogGeneralTraceEvents": "false",
        "Description": "",
        "ActorPoolSize": "2",
        "Item": [
            {
                "@Name": "ChatService",
                "@ClassName": "Python.ChatService",
                "@Enabled": "true",
                "Setting": [
                    {
                        "@Target": "Host",
                        "@Name": "%settings",
                        "#text": "target=ChatOperation"
                    }
                ]
            },
            {
                "@Name": "ChatOperation",
                "@ClassName": "Python.ChatOperation",
                "@Enabled": "true"
            },
            {
                "@Name": "ChatProcess",
                "@ClassName": "Python.ChatProcess",
                "@Enabled": "true",
                "Setting": [
                    {
                        "@Target": "Host",
                        "@Name": "%settings",
                        "#text": "target_vector=VectorOperation\ntarget_chat=ChatOperation"
                    }
                ]
            },
            {
                "@Name": "VectorOperation",
                "@ClassName": "Python.VectorOperation",
                "@Enabled": "true"
            }
        ]
    }
}]
