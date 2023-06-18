from oceandb.utils.embedding_functions import ImageBindEmbeddingFunction

import concurrent.futures
import os
import youtube_dl
from pytube import YouTube
from tempfile import TemporaryDirectory
from typing import List, Union
from PIL import Image
import torch
from tenacity import retry, stop_after_attempt, wait_random_exponential
from torchvision import transforms
from ImageBind.models.multimodal_preprocessors import (
    EncodedVideo, 
    NormalizeVideo, 
    ConstantClipsPerVideoSampler, 
    pv_transforms, 
    get_clip_timepoints, 
    SpatialCrop
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
            return self.vision_embedding_function.embed_image(img)
        elif self.file_type == 'audio':
            return self.audio_embedding_function.embed_file(file_path)
    
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
        return self.load_and_transform_video_data(
            [video_path],
            device,
            clip_duration,
            clips_per_video,
            sample_rate
        )

    def load_and_transform_video_data(
        self,
        video_paths,
        device,
        clip_duration=2,
        clips_per_video=5,
        sample_rate=16000,
    ):
        if video_paths is None:
            return None

        video_outputs = []
        video_transform = transforms.Compose(
            [
                pv_transforms.ShortSideScale(224),
                NormalizeVideo(
                    mean=(0.48145466, 0.4578275, 0.40821073),
                    std=(0.26862954, 0.26130258, 0.27577711),
                ),
            ]
        )

        clip_sampler = ConstantClipsPerVideoSampler(
            clip_duration=clip_duration, clips_per_video=clips_per_video
        )
        frame_sampler = pv_transforms.UniformTemporalSubsample(num_samples=clip_duration)

        for video_path in video_paths:
            video = EncodedVideo.from_path(
                video_path,
                decoder="decord",
                decode_audio=False,
                **{"sample_rate": sample_rate},
            )

            all_clips_timepoints = get_clip_timepoints(clip_sampler, video.duration)

            all_video = []
            for clip_timepoints in all_clips_timepoints:
                clip = video.get_clip(clip_timepoints[0], clip_timepoints[1])
                if clip is None:
                    raise ValueError("No clip found")
                video_clip = frame_sampler(clip["video"])
                video_clip = video_clip / 255.0

                all_video.append(video_clip)

            all_video = [video_transform(clip) for clip in all_video]
            all_video = SpatialCrop(224, num_crops=3)(all_video)

            all_video = torch.stack(all_video, dim=0)
            video_outputs.append(all_video)

        return torch.stack(video_outputs, dim=0).to(device)

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
