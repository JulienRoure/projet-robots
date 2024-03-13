import serial

def enviar_via_serial(dados, porta_serial='/dev/ttyS0', velocidade_serial=115200):
    try:
        # Inicializa a conexão serial
        ser = serial.Serial(porta_serial, velocidade_serial, timeout=1)
        
        # Lê e envia cada linha do arquivo
        for linha in dados:
            ser.write(linha.encode('utf-8'))
            # Aguarda um curto período de tempo (ajuste conforme necessário)
            ser.flush()
        
        # Fecha a conexão serial
        ser.close()
        print("Envio concluído.")
    except Exception as e:
        print(f"Erro: {e}")

# Substitua 'seu_arquivo.txt' pelo caminho do seu arquivo .txt
caminho_arquivo = 'commande.txt'

try:
    # Abre o arquivo para leitura
    with open(caminho_arquivo, 'r') as arquivo:
        # Lê todas as linhas do arquivo
        linhas = arquivo.readlines()
        
        # Remove os parênteses de cada linha, se existirem
        linhas_formatadas = [linha.strip('()\n') for linha in linhas]

        # Exibe os dados formatados
        for dados_formatados in linhas_formatadas:
            print(f'[{dados_formatados}]')

        # Chama a função para enviar via serial
        enviar_via_serial(linhas_formatadas)
except FileNotFoundError:
    print(f"Arquivo '{caminho_arquivo}' não encontrado.")
except Exception as e:
    print(f"Erro: {e}")
