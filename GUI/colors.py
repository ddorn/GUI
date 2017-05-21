try:
    from .locals import *
except ImportError:
    from GUI.locals import *
    
    
def bw_contrasted(color, threshold=200):
    return [WHITE, BLACK][sum(color) / 3 > threshold]
