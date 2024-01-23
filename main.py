##Importações
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

##Função para baixar as imagens
def download_images(url):
    try:
        ##Requisição para HTTP à URL inserida
        resposta = requests.get(url)
        resposta.raise_for_status()

        # Analisa o conteúdo HTML da página usando BeautifulSoup
        soup = BeautifulSoup(resposta.text, "html.parser")

        # Encontra todas as tags de imagem (img) na página
        tags_img = soup.find_all("img")

        # Cria um diretório para armazenar as imagens baixadas, se não existir
        os.makedirs("imagens_baixadas", exist_ok=True)

        # Itera sobre as tags de imagem encontradas
        for tag_img in tags_img:
            #Obtem O URL da imagem
            url_img = tag_img.get("src")

            if url_img:
                # Constrói o URL absoluto da imagem usando urljoin
                url_img = urljoin(url, url_img)

                # Cria o caminho completo do arquivo local onde a imagem será salva
                nome_arquivo_img = os.path.join(
                    "imagens_baixadas", os.path.basename(urlparse(url_img).path)
                )
                # Verifica se o URL da imagem termina com uma extensão de imagem válida
                if url_img.lower().endswith((".jpg", ".jpeg", ".png")):
                    # Faz uma requisição para obter os dados da imagem
                    dados_img = requests.get(url_img).content
                    # Salva os dados da imagem no arquivo local
                    with open(nome_arquivo_img, "wb") as arquivo_img:
                        arquivo_img.write(dados_img)
                    # Imprime uma mensagem indicando que a imagem foi baixada com sucesso
                    print(f"Baixado: {nome_arquivo_img}")
    # Imprime uma mensagem de erro caso ocorra alguma exceção
    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Use: python image_scraper.py <URL>")
        sys.exit(1)

    url_a_analisar = sys.argv[1]
    download_images(url_a_analisar)
