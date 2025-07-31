import ROOT

# Open the ROOT file with histograms
file = ROOT.TFile.Open("../makeHistos_output_ZmmgTree_Run2_data.root")

# Only keep histograms named exactly like this pattern
target_prefix = "CMS_mumug_mass_Run2_Zmumug_"
excluded_keywords = ["FNUF", "Scale", "Smear", "Roch"]

pt_labels = {
    "ptg20": "p_{T.#gamma} #geq 20 GeV;",
    "ptg25": "p_{T.#gamma} #geq 25 GeV;",
    "pt20to35": "p_{T,#gamma} #in [20, 35) GeV;",
    "pt35to50": "p_{T,#gamma} #in [35, 50) GeV;",
    "ptg50": "p_{T.#gamma} #geq 50 GeV;"
}

eta_labels = {
    "etal1p5": "|#eta_{#gamma}| < 1.5",
    "etag1p5": "|#eta_{#gamma}| #geq 1.5",
    "": ""
}

r9_labels = {
    "r9l0p96": "R9 < 0.96",
    "r9g0p96": "R9 #geq 0.96",
    "": ""
}

# Get all histogram names from the file
keys = file.GetListOfKeys()
hist_names = [k.GetName() for k in keys]

# Filter relevant histograms
selection_names = set()
for name in hist_names:
    if not name.startswith(target_prefix):
        continue
    if any(x in name for x in excluded_keywords):
        continue
    sel_label = name[len(target_prefix):]
    selection_names.add(sel_label)

# Build DrawVariable commands
calls = []
for sel in sorted(selection_names):
    parts = sel.split('_')

    pt_part = next((p for p in parts if p.startswith("ptg") or "pt" in p), "")
    eta_part = next((p for p in parts if p.startswith("etal") or p.startswith("etag")), "")
    r9_part = next((p for p in parts if p.startswith("r9")), "")

    pt_label = pt_labels.get(pt_part, "")
    eta_label = eta_labels.get(eta_part, "")
    r9_label = r9_labels.get(r9_part, "")

    line = (
        f'DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_{sel}", false, 1, 5, 80, 100, 0.4, 1.3, '
        f'"m_{{#mu#mu#gamma}} [GeV]", "{pt_label}", "{eta_label}", "{r9_label}", "", false, 505, PRINT);'
    )
    calls.append(line)

# Write the output script
with open("DrawVariablesAll.cpp", "w") as f_out:
    f_out.write("// Auto-generated DrawVariable calls\n")
    f_out.write("#include \"DrawVariable.cpp\"\n\n")  # Replace if needed
    f_out.write("void DrawVariablesAll(bool PRINT) {\n")
    for call in calls:
        f_out.write("    " + call + "\n")
    f_out.write("}\n")

print(f"Generated DrawVariablesAll.cpp with {len(calls)} DrawVariable calls.")
