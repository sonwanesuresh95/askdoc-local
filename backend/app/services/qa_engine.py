from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from langchain.chains import retrieval

COLLECTION_NAME = "askdoc"

def get_retriever():
    embedding = OllamaEmbeddings(model="mistral")
    vectordb = Chroma(
        embedding_function=embedding,
        collection_name=COLLECTION_NAME,
    )
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})
    return retriever

def answer_question(query: str) -> str:
    retriever = get_retriever()
    llm = ChatOllama(model="mistral")
    docs = retriever.invoke(query)
    print(f"[INFO] Retrieved {len(docs)} docs for query: {query}")
    for d in docs:
        print(f"[CHUNK] {d.page_content[:200]}...")

    if not docs:
        return "No relevant content found to answer this question."

    prompt = PromptTemplate.from_template("""
                                          Answer the following question using the provided context.
                                          If the answer is not in the context, say "Answer not found in document."
                                          
                                          Context:
                                          {context}
                                          
                                          Question:
                                          {question}
                                          """)
    
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke(query)