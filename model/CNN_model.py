from torch.nn import Module
from torch.nn import Conv2d
from torch.nn import Linear
from torch.nn import MaxPool2d
import torch.nn.functional as F
from torch.nn import LogSoftmax
from torch import flatten


class Conv_QNet(Module):
    def __init__(self, num_channels: int, output_size: int) -> None:
        super(Conv_QNet, self).__init__()
        self.conv1 = Conv2d(in_channels=num_channels,
                            out_channels=20, kernel_size=(5, 5))
        self.maxpool1 = MaxPool2d(kernel_size=(2, 2), stride=(2, 2))

        self.conv2 = Conv2d(in_channels=20, out_channels=50,
                            kernel_size=(5, 5))
        self.maxpool2 = MaxPool2d(kernel_size=(2, 2), stride=(2, 2))

        self.linear1 = Linear(in_features=200, out_features=24)
        self.linear2 = Linear(in_features=24, out_features=output_size)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.maxpool1(x)

        x = F.relu(self.conv2(x))
        x = self.maxpool2(x)

        x = flatten(x, 1)
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x
