#%% Import Modules
import sys
import warnings
import pyart
import numpy.ma as ma

warnings.filterwarnings('ignore')
#%% Read Raw data
# diri = "../1_data/uf_RNN_TEAM-R_20211126050159.uf"
# diri = "../1_data/UF_TR/5_PSS/uf_PSS_20211126_045537_TEAM-R_v117_SUR.uf"
diri = sys.argv[1]
radar = pyart.io.read_uf(diri)

#%% Deal with VR (TEAM-R)
nsweeps = radar.nsweeps
VR_copy = [radar.get_field(ns, 'velocity', True) for ns in range(nsweeps)]
nbc = 2     # number of beam for compute
ngc = 10    # number of gate for compute
VR_rdgt5 = []
VR_vfbgm = []

for id, VR in enumerate(VR_copy):
    print(id)
    nbeams, ngates = VR.shape
    rdgt5 = VR.copy() # copy VR as to removed diff. gt 5
    vfbgm = VR.copy() # copy VR as to vacancy is filled with bg mean
    for nb in range(nbeams):
        for ng in range(ngates):
            if (nb >= nbc and nb+nbc+1 < nbeams):
                if (ng >= ngc and ng+ngc+1 < ngates):
                    vr_entry = VR[nb-nbc:nb+nbc+1, ng-ngc:ng+ngc+1].copy()
                    vr_value = vr_entry[nbc, ngc].copy()
                    vr_entry[nbc, ngc] = ma.masked
                    vr_mean = vr_entry.mean()
                    vr_diff = abs(vr_value - vr_mean)
                    if vr_diff > 5:
                        rdgt5[nb, ng] = ma.masked
                        vfbgm[nb, ng] = vr_mean
                    # print(VR[nb-nbc:nb+nbc+1, ng-ngc:ng+ngc+1])
                    # print(rdgt5[nb-nbc:nb+nbc+1, ng-ngc:ng+ngc+1])
                    # print(vfbgm[nb-nbc:nb+nbc+1, ng-ngc:ng+ngc+1])
        # print(nb)
    VR_rdgt5.append(rdgt5)
    VR_vfbgm.append(vfbgm)


v_tmp = VR_rdgt5[0]
for v in VR_rdgt5[1:]:
    VR_rdgt5_all = ma.vstack([v_tmp, v])
    v_tmp = VR_rdgt5_all

v_tmp = VR_vfbgm[0]
for v in VR_vfbgm[1:]:
    VR_vfbgm_all = ma.vstack([v_tmp, v])
    v_tmp = VR_vfbgm_all

# radar.add_field_like('velocity', 'VR_removed_by_gt_5_bg_diff', VR_rdgt5_all)
radar.add_field_like('velocity', 'VR_vacancy_filled_with_bgm', VR_vfbgm_all)

#%% 
datetime_str = radar.time['units'].split()[-1]
datetime_str = ''.join(s for s in datetime_str if s.isdigit())

#%% Output using UF format
diro = f"../1_data/UF_TR/VRQC_TEAM-R_{datetime_str}.uf"
F2C = {
    'reflectivity': 'DZ',
    'velocity':     'VR',
    'VR_removed_by_gt_5_bg_diff':   'VE',
    'VR_vacancy_filled_with_bgm':   'VE'
}

# C2F = {
#     'DZ':   'reflectivity',
#     'VR':   'velocity',
#     'VE':   'VR_removed_by_gt_5_bg_diff',
#     'VF':   'VR_vacancy_filled_with_bgm',
# }
f = pyart.io.write_uf(diro, radar, F2C, False)
print(f"{diro}\n")

# %%
