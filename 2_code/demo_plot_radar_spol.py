import sys
import pyart
from matplotlib import pyplot as plt

diri = sys.argv[1]
print(diri)

radar = pyart.io.read(diri)