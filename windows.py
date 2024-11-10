import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
import cv2
import threading
from main import process_file
from realtime import detect_and_display_emotions

# Глобальный флаг для остановки обработки
stop_thread = False

def open_camera():
    """Функция запуска камеры в отдельном потоке для отображения эмоций."""
    threading.Thread(target=detect_and_display_emotions).start()

def process_frame(frame):
    """Обработка кадра"""
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return gray_frame

def show_error_window(message):
    """Отображение окна ошибки с переданным сообщением."""
    root = tk.Tk()
    root.withdraw()  # Скрыть основное окно
    messagebox.showerror("Ошибка", message)
    root.destroy()

def open_file_dialog():
    """Открытие диалогового окна для выбора файла и запуск его обработки в отдельном потоке."""
    global stop_thread
    file_path = filedialog.askopenfilename()
    if file_path:  # Проверяем, что файл был выбран
        root.withdraw()  # Скрыть основное окно
        loading_window = show_loading_window()
        
        # Сбрасываем флаг остановки и запускаем поток обработки
        stop_thread = False
        processing_thread = threading.Thread(target=process_video, args=(file_path, loading_window))
        processing_thread.start()
        
        # Привязываем событие закрытия окна к функции on_closing
        loading_window.protocol("WM_DELETE_WINDOW", lambda: on_closing(loading_window, processing_thread))

def show_loading_window():
    """Создание окна загрузки с индикатором процесса."""
    loading_window = Toplevel(root)
    loading_window.title("Обработка")
    loading_window.geometry("300x100")
    label = tk.Label(loading_window, text="Обработка видео, пожалуйста подождите...")
    label.pack(pady=20)
    return loading_window

def process_video(file_path, loading_window):
    """Обработка видео с возможностью прерывания по флагу stop_thread."""
    global stop_thread
    try:
        process_file(file_path)  # Обработка файла
    except Exception as e:
        print("Ошибка обработки:", e)
    finally:
        # Закрытие окна загрузки и возврат к основному окну
        if not stop_thread:  # Закрываем окно только если обработка не прервана
            loading_window.destroy()
            root.deiconify()  # Показать основное окно снова

def on_closing(loading_window=None, processing_thread=None):
    """Функция завершения программы или остановки потока обработки."""
    global stop_thread
    stop_thread = True  # Устанавливаем флаг остановки
    if processing_thread and processing_thread.is_alive():
        processing_thread.join()  # Ожидаем завершения потока обработки
    if loading_window:
        loading_window.destroy()  # Закрываем окно загрузки
    root.quit()  # Завершить программу

# Создаем главное окно
root = tk.Tk()
root.title("EDM")
root.geometry("400x170")
root.protocol("WM_DELETE_WINDOW", on_closing)

# Создаем кнопки
camera_button = tk.Button(root, text="Открыть камеру", command=open_camera, width=50, height=3)
camera_button.pack(pady=10)

file_button = tk.Button(root, text="Выбрать видео", command=open_file_dialog, width=50, height=3)
file_button.pack(pady=10)

# Запускаем главный цикл приложения
root.mainloop()
