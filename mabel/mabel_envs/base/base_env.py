import numpy as np
from gym import utils
from mjrl.envs import mujoco_env
from mujoco_py import MjViewer


class frankaBaseEnv(mujoco_env.MujocoEnv, utils.EzPickle):
    def __init__(self, model_path, frame_skip=40):
        utils.EzPickle.__init__(self)
        self.initializing = True

        mujoco_env.MujocoEnv.__init__(self, model_path, frame_skip)

        self.act_mid = np.mean(self.model.actuator_ctrlrange, axis=1)
        self.act_rng = 0.5*(self.model.actuator_ctrlrange[:,1]-self.model.actuator_ctrlrange[:,0])
        self.init_qpos[:self.sim.model.nu] = self.act_mid
        self.initializing = False

    def step(self, a):
        a = np.clip(a, -1.0, 1.0)
        try:
            a = self.act_mid + a*self.act_rng # mean center and scale
        except:
            a = a                             # only for the initialization phase
            print("WARNING: Actions cannot be remapped. (Expected during initialization)")
            
        self.do_simulation(a, self.frame_skip)
        obs = self.get_obs()

        score, reward_dict, solved, done = self.get_score_reward_solved_done(self.obs_dict)

        # finalize step
        env_info = {
            'time': self.obs_dict['t'],
            'obs_dict': self.obs_dict,
            'rewards': reward_dict,
            'score': score,
            'solved': solved
        }
        return obs, reward_dict['total'], done, env_info

    def get_score_reward_solved_done(self):
        raise NotImplementedError

    def get_obs(self, obs_dict, act=None):
        raise NotImplementedError

    def compute_path_rewards(self, paths):
        # path has two keys: observations and actions
        # path["observations"] : (num_traj, horizon, obs_dim)
        # path["rewards"] should have shape (num_traj, horizon)
        obs = paths["observations"]
        score, rewards, done = self.get_score_reward_solved_done(obs)
        paths["rewards"] = rewards if rewards.shape[0] > 1 else rewards.ravel()

    def reset_model(self):
        raise NotImplementedError # for child class to define 

    def evaluate_success(self, paths, logger=None):
        success = 0.0
        for p in paths:
            if np.mean(p['env_infos']['solved'][-4:]) > 0.0:
                success += 1.0
        success_rate = 100.0*success/len(paths)
        if logger is None:
            # nowhere to log so return the value
            return success_rate
        else:
            # log the success
            # can log multiple statistics here if needed
            logger.log_kv('success_rate', success_rate)
            return None

    # --------------------------------
    # get and set states
    # --------------------------------
    def get_env_state(self):
        return dict(qp=self.data.qpos.copy(), qv=self.data.qvel.copy())

    def set_env_state(self, state):
        self.sim.reset()
        qp = state['qp'].copy()
        qv = state['qv'].copy()
        self.set_state(qp, qv)
        self.sim.forward()

    # --------------------------------
    # utility functions
    # --------------------------------
    def get_env_infos(self):
        return dict(state=self.get_env_state())

    def mj_viewer_setup(self):
        self.viewer = MjViewer(self.sim)
        self.viewer.cam.azimuth = -90
        self.viewer.cam.distance = 2.5
        self.viewer.cam.elevation = -30
        self.sim.forward()

    def close_env(self):
        pass