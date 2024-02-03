from pokemon_env import PokemonEnv
from model import DQNAgent
import torch

def main(args) :
    env = PokemonEnv("jeu/PokemonRed.gb", emulation_speed=0, render_reward=True, render_view=True)
    infos, img = env.reset()
    agent = DQNAgent()
    agent.target_q_network.load_state_dict(torch.load(args.model_weights))
    agent.target_q_network.to(agent.device)

    agent.frame_stacking.reset(img)
    frames =  torch.tensor(agent.frame_stacking.stack_frames(), dtype=torch.float32).permute(2, 0, 1).unsqueeze(0).to(agent.device)
    infos = torch.tensor(infos, dtype=torch.float32).unsqueeze(0).to(agent.device)

    for _ in range(10000):
        action = agent.target_q_network(frames, infos).max(1).indices.item()
        infos, img, reward, done  = env.step(action)
        agent.frame_stacking.update_buffer(img)
        frames = torch.tensor(agent.frame_stacking.stack_frames(), dtype=torch.float32).permute(2, 0, 1).unsqueeze(0).to(agent.device)
        infos = torch.tensor(infos, dtype=torch.float32).unsqueeze(0).to(agent.device)

    env.close()

if __name__ == "__main__" :
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-w', "--model_weights", type=str, default="checkpoints/training_1/target_q_network_11.pth")