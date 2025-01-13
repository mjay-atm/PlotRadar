#%% Import Modules
import sys
import warnings
import pyart

warnings.filterwarnings('ignore')
#%% Read Raw data
# diri = "../1_data/X-Rock211126050159.RAW0363"
diri = sys.argv[1]
radar = pyart.io.read(diri)

#%% 
datetime_str = radar.time['units'].split()[-1]
datetime_str = ''.join(s for s in datetime_str if s.isdigit())

#%% Output using UF format
diro = f"../1_data/TEAM-R_{datetime_str}.uf"
f = pyart.io.write_uf(diro, radar)
print(f"{diro}\n")

# %%
