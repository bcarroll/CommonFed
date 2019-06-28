from platform import machine, system
from os.path import join as path_join
bindir = path_join('bin', system(), machine())
print(bindir)