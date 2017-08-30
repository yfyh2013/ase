from ase.io import read, write
from ase.io import crystal
from ase.optimize import BFGS
from ase.atoms import Atoms
from ase.calculators.crystal import CRYSTAL
import os

geom = Atoms('OHH',
             positions=[(0, 0, 0), (1, 0, 0), (0, 1, 0)])

geom.set_calculator(CRYSTAL(label='water',
                            guess=True,
                            basis='sto-3g',
                            xc='PBE',
                            otherkey=['SCFDIR', 'ANDERSON',
                                     ['MAXCYCLES', '500'],
                                     ['TOLDEE', '6'],
                                     ['TOLINTEG', '7 7 7 7 14'],
                                     ['FMIXING', '90']]
                            ))

opt = BFGS(geom)
opt.run(fmax=0.05)

final_energy = geom.get_potential_energy()
assert abs(final_energy + 2047.34531091) < 1.0

files = ['SCFOUT.LOG', 'INPUT', 'opta1', 'ERROR',
         'FORCES.DAT', 'dffit3.dat', 'OUTPUT']

for file in files:
    try:
        os.remove(file)
    except OSError:
        pass

dir = os.getcwd()
fort = os.listdir(dir)
for file in fort:
    if file.startswith("fort."):
        os.remove(os.path.join(dir, file))