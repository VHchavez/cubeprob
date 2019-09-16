import psi4
import numpy_html
import matplotlib.pyplot as plt
import os

def _getline(cube):
    """
    Read a line from cube file where first field is an int 
    and the remaining fields are floats.
    
    params:
        cube: file object of the cube file
    
    returns: (int, list<float>)
    
    Author: P. R. Vaidyanathan
    """
    l = cube.readline().strip().split()
    return int(l[0]), map(float, l[1:])

def read_cube(fname):
    """ 
    Read cube file into numpy array
    
    params:
        fname: filename of cube file
        
    returns: (data: np.array, metadata: dict)
    
    Author: P. R. Vaidyanathan
    """
    meta = {}
    with open(fname, 'r') as cube:
        cube.readline(); cube.readline()  # ignore comments
        natm, meta['org'] = _getline(cube)
        nx, meta['xvec'] = _getline(cube)
        ny, meta['yvec'] = _getline(cube)
        nz, meta['zvec'] = _getline(cube)
        meta['atoms'] = [_getline(cube) for i in range(natm)]
        data = np.zeros((nx*ny*nz))
        idx = 0
        for line in cube:
            for val in line.strip().split():
                data[idx] = float(val)
                idx += 1
    data = np.reshape(data, (nx, ny, nz))
    return data, meta


class cubeprop():
    def __init__(self, geometry, method_basis):
        
        psi4.set_options({'reference' : 'uhf', 
                          'cubic_grid_spacing' : [.08, 0.08, 0.08]})

        self.geometry = geometry
        self.method = method_basis
        
        
    def plot_density(self, which_density, iso=0.020,slices=1,delete_cubefile=True):
        psi4.set_options({'cubeprop_tasks':['density']})

        energy, wfn = psi4.energy(self.method, molecule=self.geometry, return_wfn = True)
        
        psi4.cubeprop(wfn)
        
        if which_density == 'Da':
            D, D_info = read_cube('Da.cube')
            
        elif which_density == 'Db':
            D, D_info = read_cube('Db.cube')
            
        elif which_density == 'Ds':
            D, D_info = read_cube('Ds.cube')
            
        elif which_density == 'Dt':
            D, D_info = read_cube('Dt.cube')
            
        
        if delete_cubefile == True:
            os.remove('Da.cube')
            os.remove('Db.cube')
            os.remove('Ds.cube')
            os.remove('Dt.cube')
            
        fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10,10))
        print(D.shape)
#        for i in range(0):
#            for j in range(0):
            
        ax.imshow(D[60,:,:], interpolation="nearest")

        for i in range(D.shape[1]):
            for j in range(D.shape[2]):
                if np.isclose(D[60, i, j], iso, 0.3e-1) == True:
#                    if (i+j) % 0 == 0: 
                    ax.scatter(j,i, color="white")
        
        return D
        