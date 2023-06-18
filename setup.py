from setuptools import setup, find_packages

setup(
  name = 'elysium',
  packages = find_packages(exclude=['examples']),
  version = '0.0.1',
  license='APACHE',
  description = 'Elysium Knowledge Repository - Pytorch',
  author = 'Kye Gomez',
  author_email = 'kye@apac.ai',
  url = 'https://github.com/Agora-X/EKR',
  long_description_content_type = 'text/markdown',
  keywords = [
    'artificial intelligence',
    'attention mechanism',
    'transformers'
  ],
  install_requires=[
    'torch>=1.6',
    'oceandb',
    'youtube_dl',
    'pytube',
    'tenacity',
    'torchvision',
    'pandas'
    'PIL'
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)