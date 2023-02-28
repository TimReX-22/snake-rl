# Snake using RL
Reinforcement Learning for the game snake using PyTorch and PyGame

## Install

You can install the source using:
```
git clone git@github.com:TimReX-22/snake-rl.git
```
The required dependencies can be install by using pip:
```
pip install -r requirements.txt
```

## Run

To run a model, add the relative path to `parameters.json`. The JSON file should also include the following:
```
{
  "max_memory": 100000,
  "batch_size": 1000,
  "lr": 0.001,
  "gamma": 0.9,
  "epsilon": 100,
  "model_name": "model/model_score_36_1.pth"
}
```
If you want to train a new model, do not include a `model_name` in the JSON file. Then you can run the agent using:
```
python agent.py parameters.json
```
## Credits
The Inspiration for this project stems from this [YouTube Video](https://www.youtube.com/watch?v=L8ypSXwyBds)