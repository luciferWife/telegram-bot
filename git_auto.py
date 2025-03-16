import subprocess

# Функция для выполнения команды в терминале
def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Ошибка: {result.stderr}")
    else:
        print(result.stdout)

# Добавляем все файлы в Git
run_command(["git", "add", "."])

# Делаем коммит с сообщением
commit_message = "Автоматический коммит"
run_command(["git", "commit", "-m", commit_message])

# Отправляем изменения в удалённый репозиторий (например, в main)
run_command(["git", "push", "origin", "main"])
