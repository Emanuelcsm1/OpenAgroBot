import os
import random
import shutil

# Caminhos base
base_dir = 'dataset'
img_dir = os.path.join(base_dir, 'images', 'train')
lbl_dir = os.path.join(base_dir, 'labels', 'train')

# Novos diretórios de destino
img_train = os.path.join(base_dir, 'images', 'train')
img_val = os.path.join(base_dir, 'images', 'val')
lbl_train = os.path.join(base_dir, 'labels', 'train')
lbl_val = os.path.join(base_dir, 'labels', 'val')

# Criação dos diretórios de validação
os.makedirs(img_val, exist_ok=True)
os.makedirs(lbl_val, exist_ok=True)

# Lista de imagens
image_files = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

# Embaralhar e dividir 80/20
random.shuffle(image_files)
split_idx = int(0.8 * len(image_files))
train_imgs = image_files[:split_idx]
val_imgs = image_files[split_idx:]

# Função para mover imagens e labels
def mover(lista, destino_img, destino_lbl):
    for img_file in lista:
        base = os.path.splitext(img_file)[0]
        label_file = f"{base}.txt"

        img_src = os.path.join(img_dir, img_file)
        lbl_src = os.path.join(lbl_dir, label_file)

        img_dst = os.path.join(destino_img, img_file)
        lbl_dst = os.path.join(destino_lbl, label_file)

        if os.path.exists(lbl_src):
            shutil.move(img_src, img_dst)
            shutil.move(lbl_src, lbl_dst)
        else:
            print(f"❌ Label não encontrada para {img_file}, pulando...")

# Mover arquivos de validação (treino já está no lugar)
mover(val_imgs, img_val, lbl_val)

print("✅ Separação 80/20 concluída. Arquivos de validação movidos.")
