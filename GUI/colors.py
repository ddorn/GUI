try:
    from .locals import *
except ImportError:
    from GUI.locals import *
    
    
def bw_contrasted(color, threshold=200):
    """ Return a color (B or W) of oposite balance : it will be easy to distinguish both """
    return [WHITE, BLACK][sum(color) / 3 > threshold]
