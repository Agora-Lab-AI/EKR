# Agora
The Elysium Knowledge Repository or EKR is brought to you by Agora, we're an all-new open source multi-modal AI research organization devoted towards advancing Humanity.

[Join us and help embed all of Humanity's knowledge into multi-modal embeddings and join the discord for support!](https://discord.gg/qUtxnK2NMf)

# Elysium Knowledge Repository: Embedding the Wisdom of Humanity 🏛️

Welcome to the **Elysium Knowledge Repository**! Utilizing the principles of the ancient Greeks, this advanced solution converts all of humanity's wisdom into multi-modal embeddings, preserved and stored in an efficient Parquet format.

## Features 🚀
- Convert diverse knowledge sources into multi-modal embeddings
- Efficient data storage with Parquet format
- Easy integration with OpenAI models
- Versatile usage for AI, machine learning, data mining, and other applications

## Getting Started 🌟

### Installation
Install all necessary libraries with the following pip commands:

```sh
pip install numpy pandas pyarrow nomic tenacity python-dotenv concurrent
```

### Usage

You can start embedding humanity's wisdom by following the steps in the main Python script:

```python
# Import the necessary Python packages
import os
import pandas as pd
import pyarrow.parquet as pq
from elysium import Elysium

# Load your OpenAI API key
dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Specify your knowledge source file
file_path = 'path_to_your_file'

# Initialize the Elysium embedding object
elysium = Elysium(file_path)

# Generate the embeddings
elysium.generate_embeddings()

# Save the embeddings to a Parquet file
elysium.save_to_parquet()

# Verify the generated embeddings
elysium.verify_embeddings()

# That's it! Your wisdom is now embedded and stored efficiently!
```

### Requirements
- Python 3.7 or higher
- OpenAI API Key
- NumPy
- Pandas
- PyArrow
- Nomic
- Tenacity
- Dotenv
- Concurrent


## How it works ⚙️

The Elysium Knowledge Repository works by reading your knowledge source file (such as a CSV file), converting the information into multi-modal embeddings using [Pegasus](https://github.com/kyegomez/Pegasus) models, and storing these embeddings in a highly efficient Parquet format. It also provides capabilities to load and verify the generated embeddings, ensuring your wisdom is accurately preserved.

## Roadmap 🗺️

We aim to create a repository capable of embedding every type of multi-modal data, a mammoth task broken down into the following steps:

1. Develop and implement robust text embedding capabilities.

2. Expand our functionality to handle image data. This will involve creating image-to-embedding transformations.

3. Add functionality for audio data embedding. This will include developing a method for translating sound waves into a numerical representation that can be used for embeddings.

4. Incorporate video data embedding capabilities. This will require a combination of our image and audio data embedding strategies.

5. Extend our repository's functionality to handle sensor data. This can include data from IoT devices, biomedical sensors, and more.

6. Incorporate the ability to handle mixed data types within a single source. This is particularly useful for data sources such as scientific articles that contain text, images, and tables.

7. Develop a method for handling real-time data streams. This will enable us to provide up-to-date embeddings that reflect the most recent data.

8. Create an API for the Elysium Knowledge Repository. This will allow users to interact with our service programmatically and integrate it into their own applications.

9. Continuously optimize and refine our embedding processes. This includes improving efficiency, accuracy, and coverage.

10. Regularly update the repository with new data sources, keeping our stored wisdom current and comprehensive.

## Share with Friends 💌

Help spread the wisdom! Share the Elysium Knowledge Repository with your friends and colleagues via

 social media platforms:

- [Share on Facebook](https://www.facebook.com/sharer/sharer.php?u=<URL>)
- [Share on Twitter](https://twitter.com/intent/tweet?text=Check%20out%20the%20Elysium%20Knowledge%20Repository:%20<URL>)
- [Share on LinkedIn](https://www.linkedin.com/shareArticle?mini=true&url=<URL>&title=Elysium%20Knowledge%20Repository)

(Replace `<URL>` with the link to this GitHub repository)

## Contributing 🤝

Contributions are always welcome! If you have any improvements or additions, feel free to open a pull request. For major changes, please open an issue first to discuss your proposals.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Roadmap 

[Please help us craft a list of data sources to embed, join the Agora discord!](https://discord.gg/qUtxnK2NMf)


Multi-modal data sources provide rich context and enable diverse applications across several domains. Below are three data sources that could be embedded and open-sourced:

1. **YouTube videos**: YouTube is a massive source of multi-modal data, including audio, video, and text (closed captioning or comments). Embedding and open-sourcing this data can create opportunities for research in fields like natural language processing, computer vision, sentiment analysis, recommendation systems, etc. Your work might gain attention if you build effective tools to deal with YouTube data, given the platform's popularity and scale. However, data usage is subject to YouTube's terms of service, which restricts downloading content without explicit permission.

2. **Wikipedia**: The text data from Wikipedia articles along with the images, charts, and tables it contains can be used as a multi-modal dataset. This dataset can be helpful in fields like knowledge graph construction, semantic search engines, AI assistants, or even more general NLP tasks. Because Wikipedia is a go-to resource for various AI tasks, your contributions might stand out. It's worth mentioning that extracting, processing, and providing access to such a large-scale dataset requires significant computational resources.

3. **Twitter data**: Twitter offers text, image, and sometimes video data, and it's frequently used for sentiment analysis, event detection, and studying social phenomena. Open-sourcing Twitter embeddings might bring recognition, especially if you can handle the diverse languages and the informal and abbreviated language used. Twitter's API usage policies and data privacy considerations are critical factors here.

There are challenges and constraints associated with each data source. They include, but aren't limited to, the following:

- **Data volume**: The sheer size of these datasets can pose significant challenges for downloading, storing, processing, and distributing the data.

- **Privacy**: It's essential to respect user privacy and confidentiality. This is especially relevant for social media platforms like Twitter, where user-specific information can be sensitive.

- **Terms of use**: Each platform will have its own terms and conditions for data usage. For example, both YouTube and Twitter have specific rules governing how their data can be accessed and used.

- **Data heterogeneity**: Handling different data types (text, audio, video, images) may require different pre-processing and embedding strategies. This can make the project complex and computationally demanding.


+ Some  other potential data sources with potential challenges and obstacles:

1. **Podcasts (e.g., Apple Podcasts, Spotify)**: These are rich sources of audio data and often come with accompanying transcripts. They can be used for various audio analysis tasks, voice recognition, or natural language understanding tasks. However, obtaining the data might be challenging due to the need to scrape or use APIs, and some platforms may not provide full transcripts.

2. **TV News (e.g., CNN, BBC)**: These channels offer video, audio, and sometimes transcripts of their news programming. This can be used in many ways, including analyzing media bias or monitoring global events. However, access to this data might be restricted, and extraction can be complex due to the website structure or streaming formats used.

3. **Online Courses (e.g., Coursera, Udemy)**: Online courses offer video, audio, text, and sometimes quizzes and other interactive content. This can be used to build AI that learns from instructional content or to analyze online learning. However, the courses often require payment, and scraping could violate terms of service.

4. **E-Books (e.g., Project Gutenberg)**: E-books can offer text, and sometimes audio or images. This could be used for a variety of text analysis tasks. The challenge here might be dealing with different formats and ensuring that data is extracted correctly from each.

5. **Audiobooks (e.g., LibriVox)**: This source is useful for a variety of audio processing tasks. It might be challenging to sync audio with the corresponding text, especially when there's a lack of exact transcripts.

6. **Music Platforms (e.g., SoundCloud, Bandcamp)**: These platforms provide audio data and sometimes lyrics. They could be used for tasks like music recommendation or genre classification. Copyright issues may arise, and not all songs have accompanying lyrics.

7. **Image Databases (e.g., Flickr, Instagram)**: These platforms offer images, often with accompanying text in the form of tags or descriptions. This can be used for tasks like image captioning or object recognition. The platforms may restrict API usage, and user privacy must be respected.

8. **Medical Imaging Databases (e.g., The Cancer Imaging Archive)**: These databases offer medical images and related health data. They can be used for tasks like disease detection or health analytics. The primary challenges are privacy laws (like HIPAA in the United States) and the highly specialized knowledge required to use the data effectively.

9. **Government Records (e.g., U.S. Census Bureau, European Union Open Data Portal)**: These sources offer a variety of data types, including text, numerical data, and sometimes images or audio. The challenge is that the data may come in many different formats and may require extensive cleaning and pre-processing.

10. **Social Media Platforms (e.g., Facebook, Reddit)**: These platforms provide text, image, and sometimes video data. They can be used for sentiment analysis, event detection, and more. The obstacles include the platforms' API usage policies and privacy concerns.
