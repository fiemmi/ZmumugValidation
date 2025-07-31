#include "defineSelections.cpp"

void makeHistos(std::string_view file, std::string_view tree, bool isdata, TString year) {
  
  std::string u = std::string(file);
  gBenchmark->Start("running time");
  ROOT::EnableImplicitMT(5); // Tell ROOT you want to go parallel

  //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  //~~~~~~~~~~~~~~~~~~ SELECTION REQUIREMENTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  ROOT::RDataFrame d0(tree, string_view(u)); // Interface to TTree and TChain
  //Define dataframes for each selection
  //Zmumug selection (by JTao)
  auto f_sel = d0.Filter("mass_ScaleSmeared>80. && mass_ScaleSmeared<100. &&event_PassHLT_DiMu>0 && ( (fabs(pho_sceta) < 1.5 && pho_full5x5_r9Corr > 0.85 && pho_full5x5_r9Corr > 0.5) || (fabs(pho_sceta) < 1.5  && pho_full5x5_r9Corr < 0.85 && pho_full5x5_r9Corr > 0.5 && pho_full5x5_sieieCorr < 0.015 && pho_pfPhoIso03Corr_effA < 4. && pho_TrackIsoMuCorr < 6.) || (fabs(pho_sceta) > 1.5  && pho_full5x5_r9Corr > 0.9 && pho_full5x5_r9Corr > 0.85) || (fabs(pho_sceta) > 1.5  && pho_full5x5_r9Corr < 0.9 && pho_full5x5_r9Corr > 0.8 && pho_full5x5_sieieCorr < 0.035 && pho_pfPhoIso03Corr_effA < 4. && pho_TrackIsoMuCorr < 6.) ) && pho_hoe < 0.08 && pho_MVAOutputCorr>-0.9 && pho_PassEleVeto>0 && pho_pt_ScaleSmeared*pho_FnufCorr>20.");
  f_sel = f_sel.Define("FinalWeight", "TotWeight * PTWeight");
  
  if (isdata) std::cout << "Running on data." << std::endl;
  else std::cout << "Running on MC." << std::endl; 

  TString isdata_string;
  if (isdata) isdata_string = "_data";
  else isdata_string = "_MC";
  TFile *outputfile = new TFile( "makeHistos_output_" + TString(tree) + "_" + year + isdata_string + ".root", "RECREATE" );
  
  std::vector<ROOT::RDF::RResultHandle> allHistHandles;
  defineAllSelections(f_sel, allHistHandles, isdata, std::string(year.Data()));
  
  outputfile->Close();
  delete outputfile;

  std::cout << "Done. Event loop has been run " << d0.GetNRuns() << " times." << std::endl;
  gBenchmark->Show("running time");

}
