import concurrent.futures
import os
from typing import List, Union

import dotenv
import numpy as np
# import oceandb
import pandas as pd
import pyarrow.parquet as pq
from oceandb.utils.embedding_functions import ImageBindEmbeddingFunction
from PIL import Image
from tenacity import retry, stop_after_attempt, wait_random_exponential


# Embedding functions for different modalities
text_embedding_function = ImageBindEmbeddingFunction(modality="text")
vision_embedding_function = ImageBindEmbeddingFunction(modality="vision")
audio_embedding_function = ImageBindEmbeddingFunction(modality="audio")


class Elysium:
    def __init__(self, file_path: str, file_type: str):
        self.file_path = file_path
        self.file_type = file_type
        self.df = None
        self.embedding_function = ImageBindEmbeddingFunction()

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
    def get_embedding(self, file_path: str) -> List[float]:
        if self.file_type == 'image':
            img = Image.open(file_path)
            return self.embedding_function.embed_image(img)
        elif self.file_type == 'audio':
            audio_data, samplerate = sf.read(file_path)
            return self.embedding_function.embed_audio(audio_data, samplerate)

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


if __name__ == "__main__":
    directory_path = 'path_to_your_directory'
    file_type = 'audio'  # or 'image'
    elysium = Elysium(directory_path, file_type)
    elysium.generate_embeddings()
    elysium.save_to_parquet()
    elysium.verify_embeddings()