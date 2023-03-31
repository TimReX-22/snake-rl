from model.CNN_model import Conv_QNet

import unittest
import torch

class TestConvQNet(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.model = Conv_QNet(num_channels=1, output_size=3)

    def test_forward(self):
        input: torch.Tensor = torch.Tensor()
        output = self.model(input)

if __name__ == "__main__":
    unittest.main()
