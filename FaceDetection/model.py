import numpy as np
import random
import json
from PIL import Image
from collections import defaultdict

import torchvision.datasets as datasets
import torchvision.transforms as transforms
from torch.utils.data import Dataset
import torch
import torch.nn.functional as F
from utils import SiameseNetwork


def __helper__():
    # load pretrained model
    net = torch.load("models/network.pth")

    # Resize the images and transform to tensors
    transformation = transforms.Compose([transforms.Resize((100, 100)),
                                        transforms.ToTensor()
                                         ])
    return net, transformation


def run_inference(test_image: str):
    """ Identify the person given an image """

    net, transformation = __helper__()

    test_image = Image.open(test_image)
    # assuming structure -> data/DB/name/pic.jpg
    def get_name(x): return x.split("/")[-2]

    # collects dissimilarity scores per face to average it later
    scores = defaultdict(list)

    test_folder = "data/DB"
    DB_dataset = datasets.ImageFolder(root=test_folder)

    t_test = transformation(test_image.convert("L"))  # format test image
    for i, (img, label) in enumerate(DB_dataset):
        t_img = transformation(img.convert("L"))
        output1, output2 = net(torch.unsqueeze(
            t_img, 0), torch.unsqueeze(t_test, 0))
        score = F.pairwise_distance(output1, output2).item()

        scores[get_name(DB_dataset.imgs[i][0])].append(score)

    min_score, min_name = float('inf'), None
    for k, v in scores.items():
        if np.mean(v) < min_score:
            min_score = np.mean(v)
            min_name = k

    # label and corresponding score
    with open(f"{test_folder}/{min_name}/{min_name}.json") as f:
        return json.load(f), min_score
