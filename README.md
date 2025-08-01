# ZmumugValidation
Simple framework to skim trees and produce Zμμγ validation plots in the context of H(γγ) analyses. In order to make plots, please follow the steps described below.

## Step 1. Add FNUF branches to ZmmgTree
Run
```
cd addFNUFBranches
python addFNUF_Zmmg.py --era Run2 --data
python addFNUF_Zmmg.py --era Run2 --mc
```

## Step 2. Make histograms
Run
```
root -l -q 'makeHistos.cpp("path/to/inputfile.root", "treeName", isdata, "Run2")'
```
Setting `isdata` to true/false will deal with event weights accordingly. E.g.:

```
root -l -q 'makeHistos.cpp("/eos/user/b/bmarzocc/Zmmg_ForFNUF_phoReg_IJazz_SnS/data_ZpT_S5_Run2_withFNUF_withPNCorr_fix_v3.root", "ZmmgTree", 1, "Run2")'
root -l -q 'makeHistos.cpp("/eos/user/b/bmarzocc/Zmmg_ForFNUF_phoReg_IJazz_SnS/DY_ZpT_S5_Run2_withFNUF_withPNCorr_fix_v3.root", "ZmmgTree", 0, "Run2")'
```
You can implement new selections by changing the fields in `defineSelections.cpp`.

## Step 3. Generate DrawVariablesAll.cpp script
Run
```
cd plots
python3 makeDrawVariablesAll.py
```
This will read the content of the files created at step 1 and automatically create one call to the `DrawVariable()` method for each selection you designed. The calls will be collected in the script `DrawVariablesAll.cpp`.

## Step 4. Make plots
Run
```
root -l setTDRStyle.C
.x DrawVariablesAll.cpp(PRINT)
```
Setting `PRINT==true` will make the script save the plots locally.

