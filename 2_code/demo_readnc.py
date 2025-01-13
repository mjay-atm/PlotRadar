#%% Function
def readnc(diri:str, printable:bool):

    import netCDF4 as nc

    ds = nc.Dataset(diri)
    var_name = list(ds.variables.keys())

    if printable:
        for idx, var in enumerate(var_name):
            print(f'{idx:03} -> {var} {ds.variables[var].shape}') 
            ##### if wanna ignore Warning, use python -W ignore::DeprecationWarning filename.py
            description = ds.variables[var].__dict__.get('description')
            if description is None:
                pass
            else:
                print(f"    -> {ds.variables[var].__dict__.get('description')}")
    
    return ds, var_name

#%%
if __name__ == '__main__':
    
    diri = '../1_data/cfrad.20220625_000000.768_to_20220625_000048.402_SPOL_PrecipRhi1_RHI.nc'
    ds, var_name = readnc(diri, True)
