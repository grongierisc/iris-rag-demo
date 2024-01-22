from rag.bo import ChatOperation, IrisVectorOperation, ChromaVectorOperation
from rag.bs import ChatService
from rag.bp import ChatProcess

CLASSES = {
    "Python.ChatService": ChatService,
    "Python.ChatOperation": ChatOperation,
    "Python.ChatProcess": ChatProcess,
    "Python.IrisVectorOperation": IrisVectorOperation,
    "Python.ChromaVectorOperation": ChromaVectorOperation,
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
                        "#text": "target=ChatProcess"
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
                        "#text": "target_vector=ChromaVectorOperation\ntarget_chat=ChatOperation"
                    }
                ]
            },
            {
                "@Name": "IrisVectorOperation",
                "@ClassName": "Python.IrisVectorOperation",
                "@Enabled": "true"
            },
            {
                "@Name": "ChromaVectorOperation",
                "@ClassName": "Python.ChromaVectorOperation",
                "@Enabled": "true"
            }
        ]
    }
}]
