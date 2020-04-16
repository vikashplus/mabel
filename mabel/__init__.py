from gym.envs.registration import register
from mjrl.envs.mujoco_env import MujocoEnv

# ----------------------------------------
HORIZON = 50

register(
    id='MableReachFixed-v0',
    entry_point='mabel.mabel_envs.reach.reach_env:frankaReachEnvFixed',
    max_episode_steps=HORIZON,
)

register(
    id='MableReachRandom-v0',
    entry_point='mabel.mabel_envs.reach.reach_env:frankaReachEnvRandom',
    max_episode_steps=HORIZON,
)

register(
    id='MableRelocateFixed-v0',
    entry_point='mabel.mabel_envs.relocate.relocate_env:MabelRelocateEnvFixed',
    max_episode_steps=HORIZON,
)

register(
    id='MableRelocateRandom-v0',
    entry_point='mabel.mabel_envs.relocate.relocate_env:MabelRelocateEnvRandom',
    max_episode_steps=HORIZON,
)

register(
    id='MablePouringFixed-v0',
    entry_point='mabel.mabel_envs.pouring.pouring_env:MabelPouringEnvFixed',
    max_episode_steps=HORIZON,
)


register(
    id='MableZipperFixed-v0',
    entry_point='mabel.mabel_envs.zipper.zipper_env:MabelZipperEnvFixed',
    max_episode_steps=HORIZON,
)