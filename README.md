# Snake using RL ![pylint_badge](https://github.com/TimReX-22/snake-rl/actions/workflows/pylint.yml/badge.svg) &nbsp;&nbsp; ![test_badge](https://github.com/TimReX-22/snake-rl/actions/workflows/python-tests.yml/badge.svg)
Reinforcement Learning for the game snake using PyTorch and PyGame. Tested on Ubuntu 20.04.

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

To run a model, you will have to create or modify `parameters.json`. The JSON file should include the following parameters:
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
`model_name` should be the relative path to the model file. If you want to train a new model, do not include a `model_name` in the JSON file. Then you can run the agent using:
```
python agent.py parameters.json
```

If you simpy want to play the snake game using your keyboard, your can run the game by:
```
python snake_pygame/run.py
```

Incase you get a `ModuleNotFoundError`, you can most likely resolve it by updating `PYTHONPATH` with the path to the repo directory:
```
export PYTHONPATH=$PYTHONPATH:<path to repo>
```

## Credits
The Inspiration for this project stems from this [YouTube Video](https://www.youtube.com/watch?v=L8ypSXwyBds)
