from django.apps import AppConfig 

from config import CFG
from model_builder import load_sbert, SimpleMLC

import argparse
import pandas as pd

import torch

 
class SearchConfig(AppConfig):

    name = 'api'
    tagged_store = pd.read_csv(f"{CFG.DATA_PATH}/{CFG.TAG_CSV}")

    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    s_bert = load_sbert(model_path=CFG.SBERT_MODEL_PATH,
                        sbert_path=CFG.SBERT_MODEL_FOLDER)

    classifier = SimpleMLC(n_classes=CFG.N_CLASSES)
    classifier.load_state_dict(torch.load(f'{CFG.CLASSIFIER_MODEL_PATH}/{CFG.CLASSIFIER_MODEL_DATE}/{CFG.CLASSIFIER_MODEL_FILE}.pth',
                                          map_location=torch.device(device)))