# downloader.py
import requests
import os
import datetime
import time
import logging

# --- Constantes ---
HORARIO_INICIAL = datetime.time(20, 20)
HORARIO_LIMITE = datetime.time(20, 58)
TEMPO_ESPERA_TENTATIVA = 300  # 5 minutos em segundos
TEMPO_ESPERA_INICIAL = 1200  # 20 minutos em segundos
PASTA_PADRAO = "downloads"
PREFIXO_PADRAO = "voz_do_brasil"
LOG_FILE = 'download.log'

# --- Configuração do Logging ---
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def baixar_audio(url, nome_arquivo, pasta_destino):
    """Baixa um arquivo de áudio, renomeia e salva na pasta de destino."""
    try:
        logging.info(f"Iniciando download de: {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Lança uma exceção para erros HTTP

        caminho_completo = os.path.join(pasta_destino, nome_arquivo)
        with open(caminho_completo, 'wb') as arquivo:
            for chunk in response.iter_content(chunk_size=8192):
                arquivo.write(chunk)

        logging.info(f"Áudio baixado e salvo com sucesso em: {caminho_completo}")
        return True

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"Erro HTTP: {http_err}")
        return False
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f"Erro de Conexão: {conn_err}")
        return False
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Erro na Requisição: {req_err}")
        return False
    except Exception as e:
        logging.error(f"Ocorreu um erro inesperado: {e}")
        return False

def renomear_arquivo(data_atual, prefixo_nome=PREFIXO_PADRAO):
    """Retorna uma string com o nome do arquivo baseado na data e prefixo."""
    nome_arquivo = f"{prefixo_nome}_{data_atual.strftime('%Y-%m-%d')}.mp3"
    return nome_arquivo

def verificar_dia_semana():
    """Verifica se é dia de semana (segunda a sexta)."""
    dia_semana = datetime.datetime.today().weekday()
    return dia_semana < 5

def verificar_horario(limite_horario):
    """Verifica se o horário atual é antes do limite."""
    horario_atual = datetime.datetime.now().time()
    return horario_atual <= limite_horario

def verificar_horario_inicial(horario_inicial):
    """Verifica se o horário atual é igual ou posterior ao horário inicial."""
    horario_atual = datetime.datetime.now().time()
    return horario_atual >= horario_inicial

def gerar_url1(date):
    """Gera a URL1 de download com base na data."""
    url1 = f"https://audios.ebc.com.br/radiogov/{date.year}/{date.month:02d}/{date.day:02d}-{date.month:02d}-{date.year}-a-voz-do-brasil.mp3"
    return url1

def gerar_url2(date):
    """Gera a URL2 de download com base na data."""
    url2 = f"https://radiogov.ebc.com.br/programas/a-voz-do-brasil-download/{date.day:02d}-{date.month:02d}-{date.year}/@@download/file"
    return url2

def executar_download(pasta_destino, prefixo_nome=PREFIXO_PADRAO, terminou_por_tempo=None, monitorando=None):
    """Executa o processo de download, verificando dia, horário e tentativas."""
    logging.info("Iniciando a rotina de download.")
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
        logging.info(f"Pasta de destino criada: {pasta_destino}")

    if verificar_dia_semana():
        logging.info("Hoje é dia de semana.")

        while not verificar_horario_inicial(HORARIO_INICIAL):
            if monitorando and not monitorando[0]:
                logging.info("Monitoramento interrompido pelo usuário.")
                return

            tempo_restante = datetime.datetime.combine(datetime.date.today(), HORARIO_INICIAL) - datetime.datetime.now()
            logging.info(f"Aguardando até {HORARIO_INICIAL}. Tempo restante: {tempo_restante}")
            if tempo_restante.total_seconds() > TEMPO_ESPERA_INICIAL:
                time.sleep(TEMPO_ESPERA_INICIAL)
            else:
                time.sleep(tempo_restante.total_seconds())


        logging.info(f"Horário correto ({HORARIO_INICIAL}). Iniciando o processo de download...")

        while verificar_horario(HORARIO_LIMITE):
            if monitorando and not monitorando[0]:
                logging.info("Monitoramento interrompido pelo usuário.")
                return

            logging.info(f"Iniciando o download... Limite: {HORARIO_LIMITE}")
            data_atual = datetime.date.today()
            nome_arquivo = renomear_arquivo(data_atual, prefixo_nome)

            url1 = gerar_url1(data_atual)
            logging.info(f"Tentando baixar da URL1: {url1}")
            sucesso = baixar_audio(url1, nome_arquivo, pasta_destino)

            if sucesso:
                logging.info("Download bem-sucedido da URL1. Aguardando o próximo dia útil.")
                return

            url2 = gerar_url2(data_atual)
            logging.info(f"Falha na URL1. Tentando baixar da URL2: {url2}")
            sucesso = baixar_audio(url2, nome_arquivo, pasta_destino)

            if sucesso:
                logging.info("Download bem-sucedido da URL2. Aguardando o próximo dia útil.")
                return

            logging.info("Falha em ambas as URLs. Aguardando 5 minutos para tentar novamente...")
            time.sleep(TEMPO_ESPERA_TENTATIVA)

        logging.info(f"Tempo limite atingido ({HORARIO_LIMITE}). O processo será encerrado até o próximo dia útil.")
        if terminou_por_tempo:
            terminou_por_tempo[0] = True  # Indicar que terminou por tempo

    else:
        logging.info("Hoje não é dia de semana. Nenhum download será feito.")
        return


if __name__ == "__main__":
    executar_download(PASTA_PADRAO, PREFIXO_PADRAO)

