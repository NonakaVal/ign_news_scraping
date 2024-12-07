

import os
from dotenv import load_dotenv
from utils.SeleniumScrapingConfig import collect_and_save_spans
from utils.ProcessMarkdown import process_markdown_with_langchain
load_dotenv()
output_file_path = r'C:\Users\nonak\OneDrive\Área de Trabalho\me\news\collected_news.md'


# URLs para coleta
urls = [
    "https://www.ign.com/news/playstation",
    "https://www.ign.com/news/nintendo"
]


collect_and_save_spans(urls, output_file_path)

# Carrega as variáveis do arquivo .env
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API Key não encontrada. Certifique-se de que está definida no arquivo .env")

# Processa o Markdown e salva o resultado
result = process_markdown_with_langchain(output_file_path, api_key)
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(result)

print(f"Resultado salvo ")
