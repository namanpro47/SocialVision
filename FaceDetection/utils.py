import torch
import torch.nn.functional as F
import torch.nn as nn
import os
from twilio.rest import Client


# create the Siamese Neural Network
class SiameseNetwork(nn.Module):

    def __init__(self):
        super(SiameseNetwork, self).__init__()

        # Setting up the Sequential of CNN Layers
        self.cnn1 = nn.Sequential(
            nn.Conv2d(1, 96, kernel_size=11, stride=4),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, stride=2),

            nn.Conv2d(96, 256, kernel_size=5, stride=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, stride=2),

            nn.Conv2d(256, 384, kernel_size=3, stride=1),
            nn.ReLU(inplace=True)
        )

        # Setting up the Fully Connected Layers
        self.fc1 = nn.Sequential(
            nn.Linear(384, 1024),
            nn.ReLU(inplace=True),

            nn.Linear(1024, 256),
            nn.ReLU(inplace=True),

            nn.Linear(256, 64)
        )

    def forward_once(self, x):
        # This function will be called for both images
        # It's output is used to determine the similiarity
        output = self.cnn1(x)
        output = output.view(output.size()[0], -1)
        output = self.fc1(output)
        return output

    def forward(self, input1, input2):
        # In this function we pass in both images and obtain both vectors
        # which are returned
        output1 = self.forward_once(input1)
        output2 = self.forward_once(input2)

        return output1, output2


def send_sms(data):
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = 'AC442336d53d2aba9de33c7d34b15a2b7f'
    auth_token = 'a2ddca46bff05e0f6a950138a46e070a'
    client = Client(account_sid, auth_token)
    message_text = f"Hi! You've connected with {data['first_name']} {data['last_name']}, who is a {data['title']} at {data['company']}. {data['first_name']} studies {data['degree']} at {data['school']}.\nFun facts about {data['first_name']}: {data['headline']}.\nYou can reach them at {data['profile']}."
    try:
        message = client.messages \
            .create(
                body=message_text,
                from_='+19108382790',
                to='+15712793320'
            )
    except Exception as e:
        print("From Twilio: ", e)
    print(f"SMS sent: {message.sid}")
