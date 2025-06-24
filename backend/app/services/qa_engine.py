from langchain.chains import retrieval
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama, OllamaEmbeddings

COLLECTION_NAME = "askdoc"

def get_retriever():
    embedding = OllamaEmbeddings(model="mistral")
    vectordb = Chroma(
        embedding_function=embedding,
        persist_directory="../data/vector_store",
        collection_name=COLLECTION_NAME,
    )
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})
    return retriever

def answer_question(query: str) -> str:
    retriever = get_retriever()
    llm = ChatOllama(model="mistral")
    docs = retriever.invoke(query)
    print(f"[QUERY] Retrieved {len(docs)} docs for '{query}'")
    for d in docs:
        print(f" -> source: {d.metadata.get('source')}, snippet: {d.page_content[:50]}")

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
    
    def context_text(_):
        return "\n\n".join(doc.page_content for doc in docs)
    

    chain = (
        {"context": context_text, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke(query)
