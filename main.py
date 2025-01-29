from corretoras import obter_precos_novadax, dolar_hoje, processar_precos_binance

def main():
    dolar = dolar_hoje()
    print(f"Dólar hoje: {dolar}")

    resultados = obter_precos_novadax()
    if resultados:
        with open("precos_novadax.txt", "w", encoding="utf-8") as file:
            file.write(resultados)
        print("Dados salvos em 'precos_novadax.txt'")
    else:
        print("Nenhum dado disponível para salvar.")

    processar_precos_binance("precos_novadax.txt")

if __name__ == "__main__":
    main()
