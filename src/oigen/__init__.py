__version__ = "0.1.0"
__all__ = ["OI", "values", "oitypes"]

def __getattr__(name: str):
    """延迟加载"""
    if name == "OI":
        from .gen import OI
        return OI
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

def __init__():
    print(f"Oi Gen {__version__} initialized.")

__init__()