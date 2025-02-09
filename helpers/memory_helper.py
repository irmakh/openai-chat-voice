import torch
import gc
import datetime
import os
from bgcolors import bcolors
def run_garbage_collection() -> None:
    """
    Run garbage collection and free up GPU memory.

    Args:
        None

    Returns:
        None
    """
    torch.cuda.empty_cache()
    gc.collect()
    #print(f"{bcolors.OKGREEN}{datetime.datetime.now().strftime('%H:%M:%S')} - garbage collected{bcolors.ENDC}")
    print_used_gpu_memory()

def print_used_gpu_memory() -> None:
    """
    Print out the amount of memory used by the current process on the GPU.

    This value is the total amount of memory allocated by the process on the GPU,
    and is updated every time a tensor is allocated or deallocated. It is
    expressed in megabytes.

    Args:
        None
    Returns:
        None
    """
    if torch.cuda.is_available():
        used_memory: float = torch.cuda.memory_allocated() / (1024 ** 2)  # Convert to MB
        #print(f"{bcolors.OKBLUE}Used GPU Memory: {used_memory:.2f} MB{bcolors.ENDC}")

