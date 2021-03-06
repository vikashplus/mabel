from mabel.mabel_envs.base.base_env import frankaBaseEnv
import os
import numpy as np


class MabelRelocateEnv(frankaBaseEnv):
    def __init__(self):
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = curr_dir+'/mabel_relocate-v0.xml'

        self.target = 0
        self.grasp = 0
        
        super().__init__(model_path=model_path)
        
        self.target = self.sim.model.site_name2id('target')
        self.grasp = self.sim.model.site_name2id('Block2')

        
    def get_obs(self):
        self.obs_dict = {}
        self.obs_dict['t'] = self.sim.data.time
        self.obs_dict['qp'] = self.sim.data.qpos.copy()
        self.obs_dict['qv'] = self.sim.data.qvel.copy()
        self.obs_dict['reach_err'] = self.sim.data.site_xpos[self.target]-self.sim.data.site_xpos[self.grasp]

        return np.concatenate([
            self.obs_dict['qp'],
            self.obs_dict['qv'],
            self.obs_dict['reach_err']])

    def get_score_reward_solved_done(self, obs_dict, act=None):
        reach_dist = np.linalg.norm(obs_dict['reach_err'])

        done = bool( reach_dist > 1.0) \
            if not self.initializing else False

        reward_dict = {}
        score = -1.* reach_dist
        reward_dict["reach_dist"] = score
        reward_dict["small_bonus"] = 4.0*(reach_dist<.1)
        reward_dict["big_bonus"] = 4.0*(reach_dist<.05)
        reward_dict["total"] = reward_dict["reach_dist"] + reward_dict["small_bonus"] + reward_dict["big_bonus"] - 50.0 * int(done) 
        
        solved = bool(reach_dist<0.050)
        return score, reward_dict, solved, done

class MabelRelocateEnvFixed(MabelRelocateEnv):
    def __init__(self):
        super().__init__()

    def reset_model(self):
        self.sim.model.site_pos[self.target] = np.array([.2, .4, .76])
        self.set_state(self.init_qpos, self.init_qvel)
        self.sim.forward()
        return self.get_obs()

class MabelRelocateEnvRandom(MabelRelocateEnv):
    def __init__(self):
        super().__init__()

    def reset_model(self):
        self.sim.model.site_pos[self.target] = self.np_random.uniform(high=[0.3, .5, .76], low=[-.3, .15, .76])
        self.set_state(self.init_qpos, self.init_qvel)
        self.sim.forward()
        return self.get_obs()