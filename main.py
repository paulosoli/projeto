##Importações
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

##teste
def download_images(url):
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()

        soup = BeautifulSoup(resposta.text, "html.parser")

        tags_img = soup.find_all("img")

        os.makedirs("imagens_baixadas", exist_ok=True)

        for tag_img in tags_img:
            url_img = tag_img.get("src")

            if url_img:
                url_img = urljoin(url, url_img)

                nome_arquivo_img = os.path.join(
                    "imagens_baixadas", os.path.basename(urlparse(url_img).path)
                )

                if url_img.lower().endswith((".jpg", ".jpeg", ".png")):
                    dados_img = requests.get(url_img).content
                    with open(nome_arquivo_img, "wb") as arquivo_img:
                        arquivo_img.write(dados_img)

                    print(f"Baixado: {nome_arquivo_img}")

    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Use: python image_scraper.py <URL>")
        sys.exit(1)

    url_a_analisar = sys.argv[1]
    download_images(url_a_analisar)
