# 1. IRIS RAG Demo

![IRIS RAG Demo](https://github.com/grongierisc/iris-rag-demo/blob/master/misc/title.jpg?raw=true)

Ceci est une simple démo de l'IRIS avec un exemple de RAG (Retrieval Augmented Generation).
Le backend est écrit en Python en utilisant IRIS et IoP, le modèle LLM est `orca-mini` et est servi par le serveur `ollama`.
Le frontend est un chatbot écrit avec Streamlit.

- [1. IRIS RAG Demo](#1-iris-rag-demo)
  - [1.1. Quest-ce que RAG?](#11-quest-ce-que-rag)
  - [1.2. Comment ça marche?](#12-comment-ça-marche)
  - [1.3. Installation de la démo](#13-installation-de-la-démo)
  - [1.4. Usage](#14-usage)
  - [1.5. Comment fonctionne la démo ?](#15-comment-fonctionne-la-démo-)
    - [1.5.1. Le frontend](#151-le-frontend)
    - [1.5.2. Le backend](#152-le-backend)
      - [1.5.2.1. Le business service](#1521-le-business-service)
      - [1.5.2.2. Le business process](#1522-le-business-process)
      - [1.5.2.3. L'opération LLM](#1523-lopération-llm)
      - [1.5.2.4. L'opération vectorielle](#1524-lopération-vectorielle)
  - [1.6. Remarques générales](#16-remarques-générales)


## 1.1. Quest-ce que RAG?

RAG signifie Retrieval Augmented Generation, il permet d'utiliser un modèle LLM (GPT-3.5/4, Mistral, Orca, etc.) avec une **base de connaissances**.

**Pourquoi est-ce important ?** Parce que cela permet d'utiliser une *base de connaissances* pour répondre aux questions, et d'utiliser le LLM pour générer la réponse.

Par exemple, si vous demandez **"Qu'est-ce que le module grongier.pex ?"** directement au LLM, il ne pourra pas répondre, car il ne sait pas ce qu'est ce module (et peut-être que vous ne le savez pas non plus 🤪).

Mais si vous posez la même question à RAG, il pourra répondre, car il utilisera la *base de connaissances* qui sait ce qu'est le module grongier.pex pour trouver la réponse.

Maintenant que vous savez ce qu'est RAG, voyons comment cela fonctionne.

## 1.2. Comment ça marche?

Tout d'abord, nous devons comprendre comment fonctionne un LLM. Les LLM sont entraînés pour prédire le mot suivant, étant donné les mots précédents. Ainsi, si vous lui donnez une phrase, il essaiera de prédire le mot suivant, et ainsi de suite. Facile, non ?

Pour interagir avec un LLM, vous devez généralement lui donner une requête, et il générera le reste de la phrase. Par exemple, si vous lui donnez la requête `Qu'est-ce que le module grongier.pex ?`, il générera le reste de la phrase, et cela ressemblera à ceci :

```
Je suis désolé, mais je ne connais pas le module Pex que vous avez mentionné. Pouvez-vous fournir plus d'informations ou de contexte à ce sujet ?
```

Ok, comme prévu, il ne sait pas ce qu'est le module grongier.pex. Mais que se passe-t-il si nous lui donnons une requête qui contient la réponse ? Par exemple, si nous lui donnons la requête `Qu'est-ce que le module grongier.pex ? C'est un module qui vous permet de faire X, Y et Z.`, il générera le reste de la phrase, et cela ressemblera à ceci :

```
Le module grongier.pex est un module qui vous permet de faire X, Y et Z.
```

Ok, maintenant il sait ce qu'est le module grongier.pex.

Mais que se passe-t-il si nous ne savons pas ce qu'est le module grongier.pex ? Comment pouvons-nous lui donner une requête qui contient la réponse ?
Eh bien, c'est là que la *base de connaissances* entre en jeu.

![RAG](https://github.com/grongierisc/iris-rag-demo/blob/master/misc/rag_schema.png?raw=true)

L'idée de RAG est d'utiliser la *base de connaissances* pour trouver le **contexte**, puis d'utiliser le LLM pour générer la réponse.

Pour trouver le **contexte**, RAG utilisera un **retriever**. Le **retriever** recherchera la *base de connaissances* pour les documents les plus pertinents, puis RAG utilisera le LLM pour générer la réponse.

Pour rechercher la *base de connaissances*, nous utiliserons la recherche vectorielle.

La recherche vectorielle est une technique qui permet de trouver les documents les plus pertinents étant donné une requête. Elle fonctionne en convertissant les documents et la requête en vecteurs, puis en calculant la similarité cosinus entre le vecteur de la requête et les vecteurs des documents. Plus la similarité cosinus est élevée, plus le document est pertinent.

Pour plus d'informations sur la recherche vectorielle, vous pouvez consulter [ce lien](https://community.intersystems.com/post/vectors-support-well-almost). Merci à @Dmitry Maslennikov pour son article.

![Vector Search](https://github.com/grongierisc/iris-rag-demo/blob/master/misc/vector_search.jpg?raw=true)

Maintenant que nous savons comment fonctionne RAG, voyons comment l'utiliser.

## 1.3. Installation de la démo

Pour installer la démo, vous devez avoir Docker et Docker Compose installés sur votre machine.

Ensuite, il suffit de cloner le repo et d'exécuter la commande `docker-compose up`.

```bash
git clone https://github.com/grongierisc/iris-rag-demo
cd iris-rag-demo
docker-compose up
```

⚠️ tout est local, rien n'est envoyé dans le cloud, donc soyez patient, cela peut prendre quelques minutes pour démarrer.  

## 1.4. Usage

Une fois la démo démarrée, vous pouvez accéder au frontend à l'adresse http://localhost:8501.

![Frontend](https://github.com/grongierisc/iris-rag-demo/blob/master/misc/iris_chat.png?raw=true)

Vous pouvez poser des questions sur l'IRIS, par exemple :

- Qu'est-ce que le module grongier.pex ?

![Question](https://github.com/grongierisc/iris-rag-demo/blob/master/misc/without_rag.png?raw=true)

Comme vous pouvez le voir, la réponse n'est pas très bonne, car le LLM ne sait pas ce qu'est le module grongier.pex.

Maintenant, essayons avec RAG :

Uploader la documentation du module `grongier.pex`, elle se trouve dans le dossier `docs`, fichier `grongier.pex.md`.

Ensuite, posez la même question :

- Qu'est-ce que le module grongier.pex ?

![Question](https://github.com/grongierisc/iris-rag-demo/blob/master/misc/with_rag.png?raw=true)

Comme vous pouvez le voir, la réponse est bien meilleure, car le LLM sait maintenant ce qu'est le module grongier.pex.

Vous pouvez voir les détails dans les logs :

Aller dans le portail de gestion à l'adresse http://localhost:53795/csp/irisapp/EnsPortal.ProductionConfig.zen?$NAMESPACE=IRISAPP&$NAMESPACE=IRISAPP& et cliquer sur l'onglet `Messages`.

Premièrement, vous verrez le message envoyé au processus RAG :

![Message](https://github.com/grongierisc/iris-rag-demo/blob/master/misc/trace_query.png?raw=true)

Ensuite, la requête de recherche dans la *base de connaissances* (base de données vectorielle) :

![Message](https://github.com/grongierisc/iris-rag-demo/blob/master/misc/trace_result_vector.png?raw=true)

Et enfin la nouvelle requête envoyée au LLM :

![Message](https://github.com/grongierisc/iris-rag-demo/blob/master/misc/trace_new_query.png?raw=true)

## 1.5. Comment fonctionne la démo ?

La démo est composée de 3 parties :

- Le frontend, écrit avec Streamlit
- Le backend, écrit avec Python et IRIS
- La *base de connaissances* Chroma et la base de données vectorielle
- Le LLM, Orca-mini, servi par le serveur Ollama

### 1.5.1. Le frontend

Le frontend est écrit avec Streamlit, c'est un simple chatbot qui vous permet de poser des questions.

Rien de bien compliqué ici, juste un simple chatbot.

<spoiler>

```python
import os
import tempfile
import time
import streamlit as st
from streamlit_chat import message

from grongier.pex import Director

_service = Director.create_python_business_service("ChatService")

st.set_page_config(page_title="ChatIRIS")


def display_messages():
    st.subheader("Chat")
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))


def process_input():
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()
        with st.spinner(f"Thinking about {user_text}"):
            rag_enabled = False
            if len(st.session_state["file_uploader"]) > 0:
                rag_enabled = True
            time.sleep(1) # help the spinner to show up
            agent_text = _service.ask(user_text, rag_enabled)

        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((agent_text, False))


def read_and_save_file():

    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False,suffix=f".{file.name.split('.')[-1]}") as tf:
            tf.write(file.getbuffer())
            file_path = tf.name

        with st.spinner(f"Ingesting {file.name}"):
            _service.ingest(file_path)
        os.remove(file_path)

    if len(st.session_state["file_uploader"]) > 0:
        st.session_state["messages"].append(
            ("File(s) successfully ingested", False)
        )

    if len(st.session_state["file_uploader"]) == 0:
        _service.clear()
        st.session_state["messages"].append(
            ("Clearing all data", False)
        )

def page():
    if len(st.session_state) == 0:
        st.session_state["messages"] = []
        _service.clear()

    st.header("ChatIRIS")

    st.subheader("Upload a document")
    st.file_uploader(
        "Upload document",
        type=["pdf", "md", "txt"],
        key="file_uploader",
        on_change=read_and_save_file,
        label_visibility="collapsed",
        accept_multiple_files=True,
    )

    display_messages()
    st.text_input("Message", key="user_input", on_change=process_input)


if __name__ == "__main__":
    page()
```
</spoiler>

💡 Je n'utilise que :

```python
_service = Director.create_python_business_service("ChatService")
```

Pour créer un lien entre le frontend et le backend.

`ChatService` est un simple service métier dans la production d'interopérabilité.

### 1.5.2. Le backend

Le backend est écrit avec Python et IRIS.

Il est composé de 3 parties :

- Le service métier
  - point d'entrée du frontend
- Le processus métier
  - effectuer la recherche dans la *base de connaissances* si nécessaire
- Deux opérations métier
  - Une pour la *base de connaissances*
    - Ingestion des documents
    - Recherche des documents
    - Effacer les documents
  - Une pour le LLM
    - Générer la réponse

#### 1.5.2.1. Le business service

Le service métier est un simple service métier qui permet :
- D'uploader des documents
- De poser des questions
- De vider la base de données vectorielle

<spoiler>

```python
from grongier.pex import BusinessService

from rag.msg import ChatRequest, ChatClearRequest, FileIngestionRequest

class ChatService(BusinessService):

    def on_init(self):
        if not hasattr(self, "target_chat"):
            self.target_chat = "ChatProcess"
        if not hasattr(self, "target_vector"):
            self.target_vector = "VectorOperation"

    def ingest(self, file_path: str):
        # build message
        msg = FileIngestionRequest(file_path=file_path)
        # send message
        self.send_request_sync(self.target_vector, msg)

    def ask(self, query: str, rag: bool = False):
        # build message
        msg = ChatRequest(query=query)
        # send message
        response = self.send_request_sync(self.target_chat, msg)
        # return response
        return response.response

    def clear(self):
        # build message
        msg = ChatClearRequest()
        # send message
        self.send_request_sync(self.target_vector, msg)
```
</spoiler>

Si vous regardez le code, vous verrez que le service métier est très simple, il ne fait que passer entre l'opération et le processus.

#### 1.5.2.2. Le business process

Le processus métier est aussi un simple processus qui permet de rechercher la *base de connaissances* si nécessaire.

<spoiler>

```python
from grongier.pex import BusinessProcess

from rag.msg import ChatRequest, ChatResponse, VectorSearchRequest

class ChatProcess(BusinessProcess):
    """
    the aim of this process is to generate a prompt from a query
    if the vector similarity search returns a document, then we use the document's content as the prompt
    if the vector similarity search returns nothing, then we use the query as the prompt
    """
    def on_init(self):
        if not hasattr(self, "target_vector"):
            self.target_vector = "VectorOperation"
        if not hasattr(self, "target_chat"):
            self.target_chat = "ChatOperation"

        # prompt template
        self.prompt_template = "Given the context: \n {context} \n Answer the question: {question}"


    def ask(self, request: ChatRequest):
        query = request.query
        prompt = ""
        # build message
        msg = VectorSearchRequest(query=query)
        # send message
        response = self.send_request_sync(self.target_vector, msg)
        # if we have a response, then use the first document's content as the prompt
        if response.docs:
            # add each document's content to the context
            context = "\n".join([doc['page_content'] for doc in response.docs])
            # build the prompt
            prompt = self.prompt_template.format(context=context, question=query)
        else:
            # use the query as the prompt
            prompt = query
        # build message
        msg = ChatRequest(query=prompt)
        # send message
        response = self.send_request_sync(self.target_chat, msg)
        # return response
        return response
```
</spoiler>

Comme je le disais, le processus est très simple, il ne fait que passer entre l'opération et le processus.

Si la recherche vectorielle retourne des documents, alors il utilisera le contenu des documents comme prompt, sinon il utilisera la requête comme prompt.

#### 1.5.2.3. L'opération LLM

L'opération LLM est une simple opération qui permet de générer la réponse.

<spoiler>

```python

class ChatOperation(BusinessOperation):

    def __init__(self):
        self.model = None

    def on_init(self):
        self.model = Ollama(base_url="http://ollama:11434",model="orca-mini")

    def ask(self, request: ChatRequest):
        return ChatResponse(response=self.model(request.query))
```

</spoiler>

Difficile de faire plus simple, non ?

#### 1.5.2.4. L'opération vectorielle

L'opération vectorielle est une opération qui permet d'ingérer des documents, de rechercher des documents et de vider la base de données vectorielle.

<spoiler>

```python

class VectorOperation(BusinessOperation):

    def __init__(self):
        self.text_splitter = None
        self.vector_store = None

    def on_init(self):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
        self.vector_store = Chroma(persist_directory="vector",embedding_function=FastEmbedEmbeddings())

    def ingest(self, request: FileIngestionRequest):
        file_path = request.file_path
        file_type = self._get_file_type(file_path)
        if file_type == "pdf":
            self._ingest_pdf(file_path)
        elif file_type == "markdown":
            self._ingest_markdown(file_path)
        elif file_type == "text":
            self._ingest_text(file_path)
        else:
            raise Exception(f"Unknown file type: {file_type}")

    def clear(self, request: ChatClearRequest):
        self.on_tear_down()

    def similar(self, request: VectorSearchRequest):
        # do a similarity search
        docs = self.vector_store.similarity_search(request.query)
        # return the response
        return VectorSearchResponse(docs=docs)

    def on_tear_down(self):
        docs = self.vector_store.get()
        for id in docs['ids']:
            self.vector_store.delete(id)
        
    def _get_file_type(self, file_path: str):
        if file_path.lower().endswith(".pdf"):
            return "pdf"
        elif file_path.lower().endswith(".md"):
            return "markdown"
        elif file_path.lower().endswith(".txt"):
            return "text"
        else:
            return "unknown"

    def _store_chunks(self, chunks):
        ids = [str(uuid.uuid5(uuid.NAMESPACE_DNS, doc.page_content)) for doc in chunks]
        unique_ids = list(set(ids))
        self.vector_store.add_documents(chunks, ids = unique_ids)
        
    def _ingest_text(self, file_path: str):
        docs = TextLoader(file_path).load()
        chunks = self.text_splitter.split_documents(docs)
        chunks = filter_complex_metadata(chunks)

        self._store_chunks(chunks)
        
    def _ingest_pdf(self, file_path: str):
        docs = PyPDFLoader(file_path=file_path).load()
        chunks = self.text_splitter.split_documents(docs)
        chunks = filter_complex_metadata(chunks)

        self._store_chunks(chunks)

    def _ingest_markdown(self, file_path: str):
        # Document loader
        docs = TextLoader(file_path).load()

        # MD splits
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
        ]

        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        md_header_splits = markdown_splitter.split_text(docs[0].page_content)

        # Split
        chunks = self.text_splitter.split_documents(md_header_splits)
        chunks = filter_complex_metadata(chunks)

        self._store_chunks(chunks)
```

</spoiler>

Si vous regardez le code, vous verrez que l'opération vectorielle est un peu plus complexe que les autres.
Les raisons sont les suivantes :

- Nous devons ingérer des documents
- Nous devons rechercher des documents
- Nous devons vider la base de données vectorielle

Pour ingérer des documents, nous devons d'abord les charger, puis les diviser en morceaux, puis les stocker dans la base de données vectorielle.

Le processus de diviser est **important**, car cela permettra à la recherche vectorielle de trouver les documents les plus pertinents.

Par exemple, si nous avons un document qui contient 1000 mots, et que nous le divisons en 10 morceaux de 100 mots, alors la recherche vectorielle pourra trouver les documents les plus pertinents, car elle pourra comparer les vecteurs de la requête avec les vecteurs des morceaux.

Dans le cas des markdowns, nous utilisons également les en-têtes pour diviser le document en morceaux.

## 1.6. Remarques générales

Tout cela peut être fait avec `langchains`, mais je voulais vous montrer comment le faire avec le framework d'interopérabilité. Et le rendre plus accessible à tous pour comprendre comment le principe des RAG fonctionne.
