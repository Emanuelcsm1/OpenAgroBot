import serial
import time
import os
import string

CAMINHO_ARQUIVO = "command_buffer.txt"
COM_PORT = "COM11"  # Altere aqui se necessário
BAUDRATE = 9600
ultimo_comando = ""

# Remove caracteres não ASCII e BOM invisível
def limpar_ascii(texto):
    return ''.join(c for c in texto if c in string.printable).strip()

def ler_comando_arquivo():
    try:
        with open(CAMINHO_ARQUIVO, "rb") as f:
            bruto = f.read()
            texto = bruto.decode("utf-8", errors="ignore")  # remove BOM, ignora erros
            return limpar_ascii(texto)
    except Exception as e:
        print("❌ Erro ao ler o arquivo:", e)
        return ""

# Tenta conectar ao Arduino
try:
    arduino = serial.Serial(COM_PORT, BAUDRATE, timeout=1)
    time.sleep(2)  # Espera inicial
    print(f"✅ Conectado ao Arduino em {COM_PORT}")
except Exception as e:
    print(f"❌ Erro ao conectar no Arduino: {e}")
    arduino = None

print("🔁 Monitorando command_buffer.txt...")

# Loop principal
while True:
    comando = ler_comando_arquivo()
    if comando and comando != ultimo_comando:
        if arduino and arduino.is_open:
            try:
                arduino.write(f"{comando}\n".encode())
                print(f"📤 Enviado para Arduino: {comando}")
                ultimo_comando = comando
            except Exception as e:
                print("❌ Erro ao enviar comando:", e)
    time.sleep(0.2)
