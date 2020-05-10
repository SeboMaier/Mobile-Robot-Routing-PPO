import gym
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.gail import generate_expert_traj, ExpertDataset
from stable_baselines.common.vec_env import VecNormalize, DummyVecEnv, SubprocVecEnv
from stable_baselines.common import set_global_seeds, make_vec_env, vec_env
from stable_baselines import PPO2



def make_env(env_id, rank, seed=0):
    """
    Utility function for multiprocessed env.

    :param env_id: (str) the environment ID
    :param num_env: (int) the number of environments you wish to have in subprocesses
    :param seed: (int) the inital seed for RNG
    :param rank: (int) index of the subprocess
    """
    def _init():
        env = gym.make(env_id)
        env.seed(seed + rank)
        return env
    set_global_seeds(seed)
    return _init

def linear_schedule(initial_value):
    def func(progress):
        return progress * initial_value
    return func


if __name__ == '__main__':
    env_id = "Simulation-v0"
    num_cpu = 1
    # Create the vectorized environment
    env = DummyVecEnv([lambda: gym.make("Simulation-v0")])
    #nvenv = SubprocVecEnv([make_env(env_id, i) for i in range(num_cpu)])
    # Stable Baselines provides you with make_vec_env() helper
    # which does exactly the previous steps for you:

    #venv = DummyVecEnv([lambda: gym.make("Simulation-v0")])
    nvenv = VecNormalize(env, norm_obs=True, norm_reward=False)


    model = PPO2(MlpPolicy, nvenv, gamma=0.99, lam=0.95, nminibatches=4, noptepochs=4, learning_rate=1e-5,
                 ent_coef=0.005, n_steps=64, tensorboard_log="./logs/", verbose=1)

    generate_expert_traj(model, save_path="PPO2_100eps", n_episodes=5)
    #dataset = ExpertDataset(expert_path='PPO2_100eps.npz', traj_limitation=1, batch_size=128, sequential_preprocessing=True)
    #model.pretrain(dataset, n_epochs=40000, val_interval=100)
    #model = PPO2.load("PPO2_400M")
    #model.set_env(nvenv)
    #model.tensorboard_log = "./logs/"
    #model.ent_coef = 0.001
    #model.learning_rate = 5e-6

    #model.learn(total_timesteps=250000000, tb_log_name="zeropadding_ppo250M_const1e-5_hor65_nmbtch4_ent_001_new")
    #model.save("ppo250M_const1e-5_hor64_ent001")



    # tensorboard --logdir=logs --host localhost --port 8088
    # http://localhost:8088/
