from model.CNN_model import Conv_QNet

import unittest
import torch


class TestConvQNet(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.num_channels = 1
        self.model = Conv_QNet(num_channels=self.num_channels, output_size=3)

    def test_forward(self):
        game_grid_size = 20
        input: torch.Tensor = torch.rand(
            (1, self.num_channels, game_grid_size, game_grid_size))
        output = self.model(input)
        self.assertEqual(output.shape, torch.Size([1, 3]))


if __name__ == "__main__":
    unittest.main()
