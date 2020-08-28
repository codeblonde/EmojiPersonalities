import pandas as pd
import numpy as np
import glob
import os

from extract_img_embeddings import process_img, get_embedding, create_dataset, save_compressed_dataset
from extract_caption_embeddings import get_emojis, clean_caption, get_text_embedding, pad_embeddings


# transform personality traits into binary markers
# adapt labels for images, captions and emojis
