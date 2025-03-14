import torch
import gc

def run_garbage_collection() -> None:
    """
    Run Python's garbage collector to free up memory.

    Returns:
        None
    """
    gc.collect()

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
    return used_memory
