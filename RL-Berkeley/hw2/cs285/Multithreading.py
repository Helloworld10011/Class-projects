#this should be replaced to utils.py!

import psutil
import ray
import numpy as np
import gym
import time

num_cpus = psutil.cpu_count(logical=False)
ray.init(num_cpus=num_cpus)

@ray.remote
def sample_trajectory_ray(env_name, max_path_length):
    # initialize env for the beginning of a new rollout
    env= gym.make(env_name)
    ob = env.reset()

    # init vars
    obs, acs, rewards, next_obs, terminals, image_obs = [], [], [], [], [], []
    steps = 0
    while True:
        # use the most recent ob to decide what to do
        obs.append(ob)
        ac = env.action_space.sample()
        acs.append(ac)

        # take that action and record results
        ob, rew, done, _ = env.step(ac)

        # record result of taking that action
        steps += 1
        next_obs.append(ob)
        rewards.append(rew)

        # End the rollout if the rollout ended
        # Note that the rollout can end due to done, or due to max_path_length
        rollout_done = done or len(rewards) > max_path_length
        terminals.append(rollout_done)

        if rollout_done:
            break

    return Path(obs, image_obs, acs, rewards, next_obs, terminals)

def sample_trajectory(env_name, max_path_length):
    # initialize env for the beginning of a new rollout
    env= gym.make(env_name)
    ob = env.reset()

    # init vars
    obs, acs, rewards, next_obs, terminals, image_obs = [], [], [], [], [], []
    steps = 0
    while True:
        # use the most recent ob to decide what to do
        obs.append(ob)
        ac = env.action_space.sample()
        acs.append(ac)

        # take that action and record results
        ob, rew, done, _ = env.step(ac)

        # record result of taking that action
        steps += 1
        next_obs.append(ob)
        rewards.append(rew)

        # End the rollout if the rollout ended
        # Note that the rollout can end due to done, or due to max_path_length
        rollout_done = done or len(rewards) > max_path_length
        terminals.append(rollout_done)

        if rollout_done:
            break

    return Path(obs, image_obs, acs, rewards, next_obs, terminals)


def sample_trajectories(env_name, min_timesteps_per_batch, max_path_length, multithreading= False):
    paths = []
    if multithreading:
        timesteps_this_batch = 0
        while timesteps_this_batch < min_timesteps_per_batch:
            print(timesteps_this_batch)
            path = ray.get([sample_trajectory_ray.remote(env_name, max_path_length) for _ in range(num_cpus)])
            timesteps_this_batch += get_pathslength(path)
            paths.extend(path)
        return paths, timesteps_this_batch

    else:
        timesteps_this_batch= 0
        while timesteps_this_batch < min_timesteps_per_batch:
            path = sample_trajectory(env_name, max_path_length)
            timesteps_this_batch += get_pathlength(path)
            paths.append(path)
        return paths, timesteps_this_batch

def Path(obs, image_obs, acs, rewards, next_obs, terminals):
    """
        Take info (separate arrays) from a single rollout
        and return it in a single dictionary
    """
    if image_obs != []:
        image_obs = np.stack(image_obs, axis=0)
    return {"observation" : np.array(obs, dtype=np.float32),
            "image_obs" : np.array(image_obs, dtype=np.uint8),
            "reward" : np.array(rewards, dtype=np.float32),
            "action" : np.array(acs, dtype=np.float32),
            "next_observation": np.array(next_obs, dtype=np.float32),
            "terminal": np.array(terminals, dtype=np.float32)}

def get_pathslength(paths):
    leng= 0
    for path in paths:
        leng += len(path["reward"])
    return leng

def get_pathlength(path):
    return len(path["reward"])


env= gym.make("LunarLanderContinuous-v2")

tic= time.time()

sample_trajectories("LunarLanderContinuous-v2", 40000, env.spec.max_episode_steps, multithreading= False)

toc= time.time()

print(toc-tic)


