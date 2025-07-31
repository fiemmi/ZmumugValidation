#include "DrawVariable.cpp"
void DrawVariablesAll(bool PRINT)
{
  //inclusive bins
  DrawVariable("CMS_mumug_mass","Run2","Zmumug",false,1,5,80,100,0.4,1.3,"m_{#mu#mu#gamma} [GeV]","#gamma #gamma preselection","","","#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass","Run2","Zmumug_ptg25",false,1,5,80,100,0.4,1.3,"m_{#mu#mu#gamma} [GeV]","p_{T.#gamma} > 25 GeV","","","#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass","Run2","Zmumug_ptg25_etal1p5",false,1,5,80,100,0.4,1.3,"m_{#mu#mu#gamma} [GeV]","p_{T.#gamma} > 25 GeV;","|#eta_{#gamma}| < 1.5","","#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass","Run2","Zmumug_ptg25_etag1p5",false,1,5,80,100,0.4,1.3,"m_{#mu#mu#gamma} [GeV]","p_{T.#gamma} > 25 GeV;","|#eta_{#gamma}| > 1.5","","#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass","Run2","Zmumug_ptg35",false,1,5,80,100,0.4,1.3,"m_{#mu#mu#gamma} [GeV]","p_{T.#gamma} > 35 GeV","","","#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass","Run2","Zmumug_ptg35_etal1p5",false,1,5,80,100,0.4,1.3,"m_{#mu#mu#gamma} [GeV]","p_{T.#gamma} > 35 GeV;","|#eta_{#gamma}| < 1.5","","#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass","Run2","Zmumug_ptg35_etag1p5",false,1,5,80,100,0.4,1.3,"m_{#mu#mu#gamma} [GeV]","p_{T.#gamma} > 35 GeV;","|#eta_{#gamma}| > 1.5","","#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass","Run2","Zmumug_ptg50",false,1,5,80,100,0.4,1.3,"m_{#mu#mu#gamma} [GeV]","p_{T.#gamma} > 50 GeV","","","#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass","Run2","Zmumug_ptg50_etal1p5",false,1,5,80,100,0.4,1.3,"m_{#mu#mu#gamma} [GeV]","p_{T.#gamma} > 50 GeV;","|#eta_{#gamma}| < 1.5","","#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass","Run2","Zmumug_ptg50_etag1p5",false,1,5,80,100,0.4,1.3,"m_{#mu#mu#gamma} [GeV]","p_{T.#gamma} > 50 GeV;","|#eta_{#gamma}| > 1.5","","#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);

  //exclusive bins (thanks ChatGPT)
  // pt in [20, 35)
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_pt20to35", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} #in [20, 35) GeV", "", "", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_pt20to35_etal1p5", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} #in [20, 35) GeV", "|#eta_{#gamma}| < 1.5", "", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_pt20to35_etag1p5", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} #in [20, 35) GeV", "|#eta_{#gamma}| > 1.5", "", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_pt20to35_r9l0p96", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} #in [20, 35) GeV", "", "R9 < 0.96", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_pt20to35_r9g0p96", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} #in [20, 35) GeV", "", "R9 #geq 0.96", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_pt20to35_r9l0p96_etal1p5", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} #in [20, 35) GeV", "|#eta_{#gamma}| < 1.5", "R9 < 0.96", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_pt20to35_r9l0p96_etag1p5", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} #in [20, 35) GeV", "|#eta_{#gamma}| > 1.5", "R9 < 0.96", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_pt20to35_r9g0p96_etal1p5", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} #in [20, 35) GeV", "|#eta_{#gamma}| < 1.5", "R9 #geq 0.96", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_pt20to35_r9g0p96_etag1p5", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} #in [20, 35) GeV", "|#eta_{#gamma}| > 1.5", "R9 #geq 0.96", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);

  // pt in [35, 50)
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_pt35to50", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} #in [35, 50) GeV", "", "", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_pt35to50_etal1p5", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} #in [35, 50) GeV", "|#eta_{#gamma}| < 1.5", "", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_pt35to50_etag1p5", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} #in [35, 50) GeV", "|#eta_{#gamma}| > 1.5", "", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_pt35to50_r9l0p96", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} #in [35, 50) GeV", "", "R9 < 0.96", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_pt35to50_r9g0p96", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} #in [35, 50) GeV", "", "R9 #geq 0.96", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_pt35to50_r9l0p96_etal1p5", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} #in [35, 50) GeV", "|#eta_{#gamma}| < 1.5", "R9 < 0.96", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_pt35to50_r9l0p96_etag1p5", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} #in [35, 50) GeV", "|#eta_{#gamma}| > 1.5", "R9 < 0.96", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_pt35to50_r9g0p96_etal1p5", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} #in [35, 50) GeV", "|#eta_{#gamma}| < 1.5", "R9 #geq 0.96", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_pt35to50_r9g0p96_etag1p5", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} #in [35, 50) GeV", "|#eta_{#gamma}| > 1.5", "R9 #geq 0.96", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);

  // pt ≥ 50
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_ptg50", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} > 50 GeV", "", "", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_ptg50_etal1p5", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} > 50 GeV", "|#eta_{#gamma}| < 1.5", "", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_ptg50_etag1p5", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} > 50 GeV", "|#eta_{#gamma}| > 1.5", "", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_ptg50_r9l0p96", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} > 50 GeV", "", "R9 < 0.96", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_ptg50_r9g0p96", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} > 50 GeV", "", "R9 #geq 0.96", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_ptg50_r9l0p96_etal1p5", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} > 50 GeV", "|#eta_{#gamma}| < 1.5", "R9 < 0.96", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_ptg50_r9l0p96_etag1p5", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} > 50 GeV", "|#eta_{#gamma}| > 1.5", "R9 < 0.96", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_ptg50_r9g0p96_etal1p5", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} > 50 GeV", "|#eta_{#gamma}| < 1.5", "R9 #geq 0.96", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);
  DrawVariable("CMS_mumug_mass", "Run2", "Zmumug_ptg50_r9g0p96_etag1p5", false, 1, 5, 80, 100, 0.4, 1.3,
             "m_{#mu#mu#gamma} [GeV]", "p_{T.#gamma} > 50 GeV", "|#eta_{#gamma}| > 1.5", "R9 #geq 0.96", "#chi^{2}/N_{d.o.f.} = ", false, 505, PRINT);

}






