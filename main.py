import os
import pandas as pd
import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip
from fer import Video, FER
from moviepy.editor import *

def process_file(file_path):
    
    face_detector = FER(mtcnn=True)
    input_video = Video(file_path)

    processing_data = input_video.analyze(face_detector, display=False)

    vid_df = input_video.to_pandas(processing_data)
    vid_df = input_video.get_first_face(vid_df)
    vid_df = input_video.get_emotions(vid_df)
    pltfig = vid_df.plot(figsize=(20, 8), fontsize=16).get_figure()

    angry = sum(vid_df.angry)
    disgust = sum(vid_df.disgust)
    fear = sum(vid_df.fear)
    happy = sum(vid_df.happy)
    sad = sum(vid_df.sad)
    surprise = sum(vid_df.surprise)
    neutral = sum(vid_df.neutral)

    emotions = ['Злость', 'Отвращение', 'Страх', 'Счастье', 'Грусть', 'Удивление', 'Нейтральное']
    emotions_values = [angry, disgust, fear, happy, sad, surprise, neutral]

    score_comparisons = pd.DataFrame(emotions, columns=['Человеческие эмоции'])
    score_comparisons['Значение эмоций из видео'] = emotions_values
    
    # Определяем папку output в директории исполняемого файла
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Извлекаем имя файла и расширение
    file_name, file_extension = os.path.splitext(os.path.basename(file_path))
    
    # Сохранение графика
    plt.legend(['Злость', 'Отвращение', 'Страх', 'Счастье', 'Грусть', 'Удивление', 'Нейтральное'],fontsize=10)
    plot_file_name = f"{file_name}_plot.png"
    plot_path = os.path.join(output_dir, plot_file_name)
    pltfig.savefig(plot_path)
    
    # Сохранение таблицы в HTML файл
    html_file_name = f"{file_name}_emotions.html"
    html_file_path = os.path.join(output_dir, html_file_name)
    score_comparisons.to_html(html_file_path, index=False, escape=False)
    
    # Сохранение видео
    output_file_name = f"{file_name}_output{file_extension}"
    path = os.path.join(output_dir, output_file_name)
    
    clip=VideoFileClip(path)
    clip.ipython_display(width=560, maxduration=90)
    
    # Удаляем data.csv
    file_name = "data.csv"
    file_name2 = "__temp__.mp4"
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    file_path2 = os.path.join(os.path.dirname(__file__), file_name2)
    # Проверяем, существует ли файл, и удаляем его
    if os.path.exists(file_path):
        os.remove(file_path)
        os.remove(file_path2)
