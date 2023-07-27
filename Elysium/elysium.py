from oceandb.utils.embedding_functions import ImageBindEmbeddingFunction
import concurrent.futures
import os
import youtube_dl
from pytube import YouTube
from tempfile import TemporaryDirectory
from typing import List 
import pyarrow.parquet as pq
from PIL import Image
from tenacity import retry, stop_after_attempt, wait_random_exponential
from ImageBind.models.multimodal_preprocessors import (
    load_and_transform_video_data
)
import pandas as pd


class Elysium:
    def __init__(self, file_path: str, file_type: str):
        self.file_path = file_path
        self.file_type = file_type
        self.df = None
        self.text_embedding_function = ImageBindEmbeddingFunction(modality="text")
        self.vision_embedding_function = ImageBindEmbeddingFunction(modality="vision")
        self.audio_embedding_function = ImageBindEmbeddingFunction(modality="audio")

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
    def get_embedding(self, file_path: str) -> List[float]:
        if self.file_type == 'image':
            img = Image.open(file_path)
            return self.vision_embedding_function(img)
        elif self.file_type == 'audio':
            return self.audio_embedding_function(file_path)
        elif self.file_type == "video":
            return self.vision_embedding_function(load_and_transform_video_data)
    
    def download_youtube_video(self, url, target_dir):
        ydl_opts = {'outtmpl': os.path.join(target_dir, '%(id)s.%(ext)s')}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def get_video_path(self, url):
        with TemporaryDirectory() as tmp_dir:
            self.download_youtube_video(url, tmp_dir)
            video_path = os.path.join(tmp_dir, YouTube(url).video_id + '.mp4')
            return video_path

    def load_and_transform_youtube_video(self, url, device, clip_duration=2, clips_per_video=5, sample_rate=16000):
        video_path = self.get_video_path(url)
        video_features = load_and_transform_video_data(
            [video_path],
            device,
            clip_duration,
            clips_per_video,
            sample_rate
        )
        return video_features
    
    def generate_embeddings(self):
        files = os.listdir(self.file_path)
        embeddings = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_to_embedding = {executor.submit(self.get_embedding, os.path.join(self.file_path, file)): file for file in files}
            for future in concurrent.futures.as_completed(future_to_embedding):
                embeddings.append((future_to_embedding[future], future.result()))
        self.df = pd.DataFrame(embeddings, columns=['File', 'Embedding'])

    def save_to_parquet(self):
        parquet_file_name = self.file_path + '.parquet'
        self.df.to_parquet(parquet_file_name)

    def verify_embeddings(self):
        parquet_file_name = self.file_path + '.parquet'
        table = pq.read_table(parquet_file_name)
        df = table.to_pandas()
        print(df.head())


# Use case example
directory_path = 'path_to_your_directory'
file_type = 'audio'  # or 'image'
elysium = Elysium(directory_path, file_type)
elysium.generate_embeddings()
elysium.save_to_parquet()
elysium.verify_embeddings()
