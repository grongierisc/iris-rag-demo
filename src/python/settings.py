from rag.bo import ChatOperation
from rag.bs import ChatService

CLASSES = {
    "Python.ChatService": ChatService,
    "Python.ChatOperation": ChatOperation,
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
            }
        ]
    }
}]
