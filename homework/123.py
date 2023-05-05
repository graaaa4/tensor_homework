import os
import hashlib

def hash_file(file):
    # Открываем файл в бинарном режиме для считывания содержимого
    with open(file, 'rb') as f:
        # Считываем содержимое файла блоками и обновляем хэш
        hasher = hashlib.md5()
        buf = f.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
        # Возвращаем окончательный хэш
        return hasher.hexdigest()

# Создаем папку "duplicates", если ее еще нет
if not os.path.exists("duplicates"):
    os.makedirs("duplicates")

# Список всех файлов в текущей директории и вложенных директориях
all_files = []
for root, dirs, files in os.walk('.'):
    for name in files:
        all_files.append(os.path.join(root, name))

# Считаем количество файлов для отображения процесса
total_files = len(all_files)
current_file = 0

# Словарь для хранения хэшей имен файлов
hash_dict = {}

# Обрабатываем каждый файл и записываем хэши в словарь
for file in all_files:
    current_file += 1
    file_hash = hash_file(file)
    if file_hash in hash_dict:
        with open("duplicates.txt", "a") as f:
            f.write(file + '\n')
        os.rename(file, os.path.join("duplicates", os.path.basename(file)))
    else:
        hash_dict[file_hash] = os.path.basename(file)
    # Выводим процент выполнения
    print(f"Processed {current_file} out of {total_files} files ({int(current_file/total_files*100)}%)")

print("Duplicate files have been moved to 'duplicates' folder and their names have been written to 'duplicates.txt'.")
