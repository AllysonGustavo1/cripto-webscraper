import requests
import json
import re

def obter_precos_binance(symbols, time_zone="0", type="FULL"):
    """Obtém preços da Binance usando os parâmetros fornecidos."""
    url = "https://api.binance.com/api/v3/ticker/24hr"

    # Validar formato do parâmetro 'symbols'
    symbols_json = json.dumps(symbols)  # Ex.: '["BTCUSDT","ETHUSDT"]'
    if not re.match(r'^\["[A-Z0-9]{1,20}(USDT)?"(,"[A-Z0-9]{1,20}(USDT)?")*\]$', symbols_json):
        print(f"Formato inválido para symbols: {symbols_json}")
        return []

    # Configurar os parâmetros da requisição
    params = {
        "symbols": symbols_json,
        "timeZone": time_zone,
        "type": type,
    }

    # Fazer a requisição
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        print(f"Dados recebidos: {data}")
        return data
    else:
        print(f"Erro ao obter preços da Binance. Status: {response.status_code}, Resposta: {response.text}")
        return []

def salvar_precos_binance(nome_arquivo, precos):
    """Salva os preços da Binance no arquivo especificado."""
    with open(nome_arquivo, "w", encoding="utf-8") as file:
        for item in precos:
            symbol = item.get("symbol", "N/A")
            price = item.get("lastPrice", "N/A")
            file.write(f"{symbol} - {price}\n")
    print(f"Dados da Binance salvos em '{nome_arquivo}'")

def processar_precos_binance(arquivo_precos):
    """Processa os preços do arquivo em lotes de 100 para a Binance."""
    with open(arquivo_precos, "r", encoding="utf-8") as file:
        linhas = file.readlines()

    # Extrair os símbolos e formatar para o padrão da Binance
    symbols = [linha.split(" - ")[0].strip() + "USDT" for linha in linhas]

    # Validar símbolos
    valid_symbols = [symbol for symbol in symbols if re.match(r"^[A-Z0-9]{1,20}USDT$", symbol)]
    print(f"Símbolos válidos: {valid_symbols}")

    # Dividir em lotes de até 100 símbolos
    lotes = [valid_symbols[i:i + 100] for i in range(0, len(valid_symbols), 100)]

    for lote in lotes:
        print(f"Consultando lote: {lote}")
        precos = obter_precos_binance(lote)
        if precos:
            salvar_precos_binance("precos_binance.txt", precos)

def obter_precos_novadax():
    """Obtém preços da NovaDAX e retorna os resultados formatados."""
    url = "https://www.novadax.com.br/api/transaction/market/currencies/v2?"
    headers = {
        "accept": "application/json",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "access-token": "undefined",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded",
        "customerid": "undefined",
        "novadax-area": "BRAZIL",
        "novadax-locale": "pt-BR",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "source-mark": "web",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text)
        currencies = data.get("data", {}).get("data", {}).get("currencies", [])

        resultados = ""
        for item in currencies:
            if "currency" in item and "price" in item:
                currency_price = f"{item['currency']} - {item['price']}\n"
                resultados += currency_price

        return resultados
    else:
        print(f"Falha ao obter dados. Status: {response.status_code}")
        return ""

def dolar_hoje():
    """Obtém a cotação do dólar."""
    url = "https://economia.awesomeapi.com.br/last/USD-BRL"
    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.text)
        dolar = data.get("USDBRL", {}).get("bid", 0)
        return dolar
    else:
        print(f"Falha ao obter dados. Status: {response.status_code}")
        return 0