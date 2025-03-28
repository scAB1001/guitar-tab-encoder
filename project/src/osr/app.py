# src/osr/app.py

from osr.training.train import train as run_training

def main():
    print("[CLI] Starting training process...")
    run_training()
