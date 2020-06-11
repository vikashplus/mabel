# MABEL
MAnipulation BEnchmarks for Learning

`MABEL` is a collection of environments/tasks for benchmarking manipulation, simulated with the [Mujoco](http://www.mujoco.org/) physics engine and wrapped in the [OpenAI `gym`](https://gym.openai.com/) API. 'MABEL' constains following tasks

Pointing           | Pouring       | Relocation             | Zipping
:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:
![Alt text](/mabel_envs/reach/reach.png?raw=false "Fetch Reaching") |  ![Alt text](mabel_envs/pouring/pouring.png?raw=false "Liquid pouring") | ![Alt text](mabel_envs/relocate/relocate.png?raw=false "Object relocation") | ![Alt text](mabel_envs/zipper/zipper.png?raw=false "Fetch zipper")


## Getting Started
`MABEL` uses git submodules to resolve dependencies. Please follow steps exactly as below to install correctly.

0. Ensure you have access these two repositories - [Franka_sim](https://github.com/vikashplus/franka_sim), [Furniture_sim](https://github.com/vikashplus/furniture_sim) and [Scene_sim](https://github.com/vikashplus/scene_sim)

1. Clone this repo with pre-populated submodule dependencies
```
$ git clone --recursive git@github.com:vikashplus/mabel.git
```
2. Update submodules
```
$ cd mabel  
$ git submodule update --remote
```
3. Add repo to pythonpath by updating `~/.bashrc` or `~/.bash_profile`
```
export PYTHONPATH="<path/to/mabel>:$PYTHONPATH"
```
4. Follow install instructions from [mjrl](https://github.com/aravindr93/mjrl) to get model free agents for `MPL'
5. To visualize an env using a random policy
```
MJPL python mabel/mabel_agents/mjrl/examine_policy.py -i mabel -e MableReachRandom-v0
```
5. To visualize an trained `mjrl` agent
```
MJPL python mabel/mabel_agents/mjrl/examine_policy.py -i mabel -e MableReachRandom-v0 -p <path to policy>
```
