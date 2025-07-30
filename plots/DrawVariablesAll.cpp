#include "DrawVariable.cpp"
void DrawVariablesAll(bool PRINT)
{
    DrawVariable("CMS_mumug_mass","Run2","Zmumug",false,1,5,80,100,0.4,1.3,"m_{#mu#mu#gamma} [GeV]","#gamma #gamma preselection","","",false,505,PRINT);
    DrawVariable("CMS_mumug_mass","Run2","Zmumug_ptg25",false,1,5,80,100,0.4,1.3,"m_{#mu#mu#gamma} [GeV]","p_{T.#gamma} > 25 GeV","","",false,505,PRINT);
    DrawVariable("CMS_mumug_mass","Run2","Zmumug_ptg25_etal1p5",false,1,5,80,100,0.4,1.3,"m_{#mu#mu#gamma} [GeV]","p_{T.#gamma} > 25 GeV;","|#eta_{#gamma}| < 1.5","",false,505,PRINT);
    DrawVariable("CMS_mumug_mass","Run2","Zmumug_ptg25_etag1p5",false,1,5,80,100,0.4,1.3,"m_{#mu#mu#gamma} [GeV]","p_{T.#gamma} > 25 GeV;","|#eta_{#gamma}| > 1.5","",false,505,PRINT);
  DrawVariable("CMS_mumug_mass","Run2","Zmumug_ptg35",false,1,5,80,100,0.4,1.3,"m_{#mu#mu#gamma} [GeV]","p_{T.#gamma} > 35 GeV","","",false,505,PRINT);
    DrawVariable("CMS_mumug_mass","Run2","Zmumug_ptg35_etal1p5",false,1,5,80,100,0.4,1.3,"m_{#mu#mu#gamma} [GeV]","p_{T.#gamma} > 35 GeV;","|#eta_{#gamma}| < 1.5","",false,505,PRINT);
    DrawVariable("CMS_mumug_mass","Run2","Zmumug_ptg35_etag1p5",false,1,5,80,100,0.4,1.3,"m_{#mu#mu#gamma} [GeV]","p_{T.#gamma} > 35 GeV;","|#eta_{#gamma}| > 1.5","",false,505,PRINT);
    DrawVariable("CMS_mumug_mass","Run2","Zmumug_ptg50",false,1,5,80,100,0.4,1.3,"m_{#mu#mu#gamma} [GeV]","p_{T.#gamma} > 50 GeV","","",false,505,PRINT);
    DrawVariable("CMS_mumug_mass","Run2","Zmumug_ptg50_etal1p5",false,1,5,80,100,0.4,1.3,"m_{#mu#mu#gamma} [GeV]","p_{T.#gamma} > 50 GeV;","|#eta_{#gamma}| < 1.5","",false,505,PRINT);
    DrawVariable("CMS_mumug_mass","Run2","Zmumug_ptg50_etag1p5",false,1,5,80,100,0.4,1.3,"m_{#mu#mu#gamma} [GeV]","p_{T.#gamma} > 50 GeV;","|#eta_{#gamma}| > 1.5","",false,505,PRINT);
}






