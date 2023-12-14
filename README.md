# IRIS RAG Demo

![IRIS RAG Demo](https://github.com/grongierisc/iris-rag-demo/blob/master/misc/title.png?raw=true)

This is a simple demo of the IRIS with RAG (Retrieval Augmented Generation) example.
The backend is written in Python using IRIS and IoP, the LLM model is `orca-mini` and served by the `ollama` server.
The frontend is an chatbot written with Streamlit.

## What is RAG?

RAG stand for Retrieval Augmented Generation, it bring the ability to use an LLM model (GPT-3.5/4, Mistral, Orca, etc.) with a **knowledge base**.


**Why is it important?** Because it allows to use the *knowledge base* to answer questions, and use the LLM to generate the answer.


For example, if you ask **"What is the grongier.pex module?"** directly to the LLM, it will not be able to answer, because it does not know what is this module (and maybe you don't know it either 🤪).

But if you ask the same question to RAG, it will be able to answer, because it will use the *knowledge base* that know what grongier.pex module is to find the answer.

Now that you know what is RAG, let's see how it works.

## How it works?

First, we need to understand how LLMS works. LLMS are trained to predict the next word, given the previous words. So, if you give it a sentence, it will try to predict the next word, and so on. Easy, right?

To interact with an LLM, usually you need to give it a prompt, and it will generate the rest of the sentence. For example, if you give it the prompt `What is the grongier.pex module?`, it will generate the rest of the sentence, and it will look like this:

```
I'm sorry, but I'm not familiar with the Pex module you mentioned. Can you please provide more information or context about it?
```

Ok, as expected, it does not know what is the grongier.pex module. But what if we give it a prompt that contains the answer? For example, if we give it the prompt `What is the grongier.pex module? It is a module that allows you to do X, Y and Z.`, it will generate the rest of the sentence, and it will look like this:

```
The grongier.pex module is a module that allows you to do X, Y and Z.
```

Ok, now it knows what is the grongier.pex module. But what if we don't know what is the grongier.pex module? How can we give it a prompt that contains the answer? Well, that's where the *knowledge base* comes in.

![RAG](https://github.com/grongierisc/iris-rag-demo/blob/master/misc/rag_schema.png?raw=true)

The whole idea of RAG is to use the *knowledge base* to find the **context**, and then use the LLM to generate the answer.
To find the **context**, RAG will use a **retriever**. The **retriever** will search the *knowledge base* for the most relevant documents, and then RAG will use the LLM to generate the answer.
To search the *knowledge base*, we will use vector search. 

Vector search is a technique that allows to find the most relevant documents given a query. It works by converting the documents and the query into vectors, and then computing the cosine similarity between the query vector and the document vectors. The higher the cosine similarity, the more relevant the document is.

![Vector Search](https://github.com/grongierisc/iris-rag-demo/blob/master/misc/vector_search.png?raw=true)

Now that we know how RAG works, let's see how to use it.

## Installation the demo

Just clone the repo and run the `docker-compose up` command.

```bash
git clone https://github.com/grongierisc/iris-rag-demo
cd iris-rag-demo
docker-compose up
```

⚠️ everything is local, nothing is sent to the cloud, so be patient, it can take a few minutes to start.

## Usage

Once the demo is started, you can access the frontend at http://localhost:8501.

![Frontend](https://github.com/grongierisc/iris-rag-demo/blob/master/misc/iris_chat.png?raw=true)

You can ask questions about the IRIS, for example:

- What is the grongier.pex module?

![Question](https://github.com/grongierisc/iris-rag-demo/blob/master/misc/without_rag.png?raw=true)

As you can see, the answer is not very good, because the LLM does not know what is the grongier.pex module.

Now, let's try with RAG:

Upload the `grongier.pex` module documentation, it's located in the `docs` folder, file `grongier.pex.md`.

And ask the same question:

- What is the grongier.pex module?

![Question](https://github.com/grongierisc/iris-rag-demo/blob/master/misc/with_rag.png?raw=true)

As you can see, the answer is much better, because the LLM now knows what is the grongier.pex module.

## How the demo works?

The demo is composed of 3 parts:

- The frontend, written with Streamlit
- The backend, written with Python and IRIS
- The *knowledge base* Chroma an vector database
- The LLM, Orca-mini, served by the Ollama server

### The frontend

The frontend is written with Streamlit, it's a simple chatbot that allows you to ask questions.

Nothing fancy here, just a simple chatbot.

I'm just using :

```python
_service = Director.create_python_business_service("ChatService")
```

To create a binding between the frontend and the backend.

`ChatService` is a simple business service in the interoperabilty production.

### The backend

The backend is written with Python and IRIS.

It's composed of 2 parts:

- The business service
- The business operation

#### The business service

The business service is a simple business service that allows :
- To upload documents
- To ask questions
- To clear the vector database

#### The business operation

The business operation is a simple business operation that allows :
- To parse the documents
- To index the documents
- To search the documents
- Use Langchain to generate the answer
