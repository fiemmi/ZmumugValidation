# ZmumugValidation
Simple framework to skim trees and produce Zμμγ validation plots in the context of H(γγ) analyses. In order to make plots, please follow the steps described below.

## Step 1. Make histograms
Run
```
root -l -q 'makeHistos.cpp("path/to/inputfile.root", "treeName", isdata, "Run2")'
```
Setting `isdata` to true/false will deal with event weights accordingly.
You can implement new selections by changing the fields in `defineSelections.cpp`.

## Step 2. Generate DrawVariablesAll.cpp script
Run
```
cd plots
python3 makeDrawVariablesAll.py
```
This will read the content of the files created at step 1 and automatically create one call to the `DrawVariable()` method for each selection you designed. The calls will be collected in the script `DrawVariablesAll.cpp`.

## Step 3. Make plots
Run
```
root -l setTDRStyle.C
.x DrawVariablesAll.cpp(PRINT)
```
Setting `PRINT==true` will make the script save the plots locally.


 
