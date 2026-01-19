import torch
import sys

print(f"Python version: {sys.version}")
try:
    print(f"Torch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA version: {torch.version.cuda}")
except Exception as e:
    print(f"Error importing torch: {e}")
except OSError as e:
    print(f"OSError importing torch: {e}")
