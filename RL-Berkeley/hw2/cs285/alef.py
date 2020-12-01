import threading
import gym
import numpy as np
import time

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
        timesteps_this_batch = [0]

        #n = min_timesteps_per_batch // max_path_length + 1
        n=8

        while timesteps_this_batch[0] < min_timesteps_per_batch:
            print(timesteps_this_batch[0])
            threads= []
            for _ in range(n):
                t= Trajectory(env_name, max_path_length, paths, timesteps_this_batch, lock)
                #t = threading.Thread(target=traject, args=(env_name, max_path_length, paths, timesteps_this_batch))
                t.start()
                threads.append(t)
            for t in threads:
                t.join()

        return paths, timesteps_this_batch[0]

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

def get_pathlength(path):
    return len(path["reward"])



def traject(env_name, max_path_length, paths, batches):
    path = sample_trajectory(env_name, max_path_length)
    paths.append(path)
    batches[0] += get_pathlength(path)


class Trajectory(threading.Thread):
    def __init__(self, env_name, max_path_length, path, batches, lock):
        threading.Thread.__init__(self)
        self.env_name= env_name
        self.max_path_length= max_path_length
        self.path= path
        self.batches= batches
        #self.lock= lock

    def run(self):
        lock.acquire()
        print(self.getName(), ": ", time.time(), " Start")
        lock.release()

        path= sample_trajectory(self.env_name, self.max_path_length)

        lock.acquire()
        print(self.getName(), ": ", time.time(), " Finish")
        self.path.append(path)
        self.batches[0] += get_pathlength(path)
        lock.release()
        #print(self.getName(), ": ", time.time(), " Finish")
        #lock.acquire()


env= gym.make("HalfCheetah-v2")

lock = threading.Lock()
tic= time.time()

sample_trajectories("HalfCheetah-v2", 40000, env.spec.max_episode_steps, multithreading= True)

toc= time.time()

print(toc-tic)