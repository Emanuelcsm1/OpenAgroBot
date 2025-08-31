import os

# Garante que o arquivo existe
if not os.path.exists("command_buffer.txt"):
    with open("command_buffer.txt", "w", encoding="utf-8") as f:
        f.write("idle\n")

def send_command(cmd):
    try:
        with open("command_buffer.txt", "w", encoding="utf-8") as f:
            f.write(f"{cmd}\n")
        print(f"📤 Comando salvo: {cmd}")
    except Exception as e:
        print("❌ Falha ao gravar comando:", e)
