import gym
import numpy as np

#print(gym.envs.registry.all())
obs= np.array([])

env= gym.make('FullCheetah')
#print(env.action_space.low.shape)
print(env.observation_space)
print(env.action_space)
print(env.spec.max_episode_steps)
ob= env.reset()
#print(ob)

for i in range(1000):
    env.render()
    observation, reward, done, info= env.step(5)
    if done:
        break
#print(i)
env.close()
