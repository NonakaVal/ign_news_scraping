import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

# Função para coletar e salvar spans de URLs
def collect_and_save_spans(
    urls, output_file_path, scroll_iterations=1, scroll_pause_time=1
):
    # Configura o ChromeDriver
    driver = webdriver.Chrome()
    
    # Cria ou abre o arquivo de saída
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for url in urls:
            file.write(f"#### {url}\n\n")
            driver.get(url)
            
            # Aguarda elementos <span> estarem visíveis
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div//span'))
            )

            # Coleta inicial
            collected_spans = set()  # Evita duplicatas
            additional_info = []
            posting_times = []

            # Coleta tempos de postagem
            posting_time_elements = driver.find_elements(
                By.XPATH, '//span[contains(@class, "posting-time-class")]'
            )
            posting_times = [
                element.text.strip() for element in posting_time_elements if element.text.strip()
            ]

            # Realiza a rolagem e coleta
            for _ in range(scroll_iterations):
                spans = driver.find_elements(By.XPATH, '//div//span')
                collected_spans.update(span.text.strip() for span in spans if span.text.strip())
                
                additional_elements = driver.find_elements(
                    By.XPATH, '//*[@id="main-content"]/section/div/section/section/div/a/div[2]/div[2]'
                )
                additional_info.extend(
                    element.text.strip() for element in additional_elements if element.text.strip()
                )
                
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(scroll_pause_time)

            # Escreve no arquivo
            file.write("\n\n##### Last News\n\n")
            for span_text in collected_spans:
                file.write(f"- {span_text}\n")
            
            file.write("\n\n##### Time List\n\n")
            for i, info in enumerate(additional_info):
                time_info = f" (time: {posting_times[i]})" if i < len(posting_times) else ""
                file.write(f"- {info}{time_info}\n")

            file.write("\n" + "=" * 80 + "\n\n")

    print(f"Texto coletado e exportado para '{output_file_path}'.")
    driver.quit()