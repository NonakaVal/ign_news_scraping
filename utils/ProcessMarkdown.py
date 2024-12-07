

from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Carrega o arquivo Markdown com LangChain
def process_markdown_with_langchain(markdown_path, api_key):
    loader = UnstructuredMarkdownLoader(markdown_path)
    data = loader.load()

    assert len(data) == 1
    assert isinstance(data[0], Document)
    
    readme_content = data[0].page_content
    print(readme_content[:250])

    llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=api_key)
    prompt = ChatPromptTemplate.from_messages(
        [("system", "Organize the lists of titles and times, each title with a corresponding time in the order it is:\n\n{context}")]
    )
    chain = create_stuff_documents_chain(llm, prompt)
    result = chain.invoke({"context": data})
    
    return result
