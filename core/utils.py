__all__ = ['phi_fix', 'phi_diff']

import numpy as np

def phi_fix(phi):
    if phi < -1*np.pi : return phi + 2*np.pi
    if phi > np.pi: return phi - 2*np.pi
    return phi

def phi_diff( phi1, phi2 ):
    return phi_fix( phi_fix(phi1) - phi_fix(phi2) )
     