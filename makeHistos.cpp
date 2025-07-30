#include "defineFunctions.cpp"

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
  auto f_sel_ptg25 = f_sel.Filter("pho_pt_ScaleSmeared*pho_FnufCorr>25.");
  auto f_sel_ptg25_etal1p5 = f_sel_ptg25.Filter("fabs(pho_sceta) < 1.5");
  auto f_sel_ptg25_etag1p5 = f_sel_ptg25.Filter("fabs(pho_sceta) > 1.5");
  auto f_sel_ptg35 = f_sel.Filter("pho_pt_ScaleSmeared*pho_FnufCorr>35.");
  auto f_sel_ptg35_etal1p5 = f_sel_ptg35.Filter("fabs(pho_sceta) < 1.5");
  auto f_sel_ptg35_etag1p5 = f_sel_ptg35.Filter("fabs(pho_sceta) > 1.5");
  auto f_sel_ptg50 = f_sel.Filter("pho_pt_ScaleSmeared*pho_FnufCorr>50.");
  auto f_sel_ptg50_etal1p5 = f_sel_ptg50.Filter("fabs(pho_sceta) < 1.5");
  auto f_sel_ptg50_etag1p5 = f_sel_ptg50.Filter("fabs(pho_sceta) > 1.5");
  ///////////////////////////////////////////////////////////////////////////////////////////
  ///////// DEFINE QUANTITIES OF INTEREST TO BE PLOTTED LATER ///////////////////////////////
  ///////////////////////////////////////////////////////////////////////////////////////////

  defineQuantitiesOfInterest(f_sel);
  defineQuantitiesOfInterest(f_sel_ptg25);
  defineQuantitiesOfInterest(f_sel_ptg25_etal1p5);
  defineQuantitiesOfInterest(f_sel_ptg25_etag1p5);
  defineQuantitiesOfInterest(f_sel_ptg35);
  defineQuantitiesOfInterest(f_sel_ptg35_etal1p5);
  defineQuantitiesOfInterest(f_sel_ptg35_etag1p5);
  defineQuantitiesOfInterest(f_sel_ptg50);
  defineQuantitiesOfInterest(f_sel_ptg50_etal1p5);
  defineQuantitiesOfInterest(f_sel_ptg50_etag1p5);
  
  if (isdata) std::cout << "Running on data." << std::endl;
  else std::cout << "Running on MC." << std::endl; 
  
  //book histogrammers and define the wanted histograms
  Histogrammer H_sel,H_sel_ptg25,H_sel_ptg25_etal1p5,H_sel_ptg25_etag1p5,H_sel_ptg35,H_sel_ptg35_etal1p5,H_sel_ptg35_etag1p5,H_sel_ptg50,H_sel_ptg50_etal1p5,H_sel_ptg50_etag1p5;
  H_sel.defineHistos(f_sel, isdata);
  H_sel_ptg25.defineHistos(f_sel_ptg25, isdata);
  H_sel_ptg25_etal1p5.defineHistos(f_sel_ptg25_etal1p5, isdata);
  H_sel_ptg25_etag1p5.defineHistos(f_sel_ptg25_etag1p5, isdata);
  H_sel_ptg35.defineHistos(f_sel_ptg35, isdata);
  H_sel_ptg35_etal1p5.defineHistos(f_sel_ptg35_etal1p5, isdata);
  H_sel_ptg35_etag1p5.defineHistos(f_sel_ptg35_etag1p5, isdata);
  H_sel_ptg50.defineHistos(f_sel_ptg50, isdata);
  H_sel_ptg50_etal1p5.defineHistos(f_sel_ptg50_etal1p5, isdata);
  H_sel_ptg50_etag1p5.defineHistos(f_sel_ptg50_etag1p5, isdata);

  TString isdata_string;
  if (isdata) isdata_string = "_data";
  else isdata_string = "_MC";
  
  TFile *outputfile = new TFile( "makeHistos_output_" + TString(tree) + "_" + year + isdata_string + ".root", "RECREATE" );
  H_sel.writeHistos(year+"_Zmumug");
  H_sel_ptg25.writeHistos(year+"_Zmumug_ptg25");
  H_sel_ptg25_etal1p5.writeHistos(year+"_Zmumug_ptg25_etal1p5");
  H_sel_ptg25_etag1p5.writeHistos(year+"_Zmumug_ptg25_etag1p5");
  H_sel_ptg35.writeHistos(year+"_Zmumug_ptg35");
  H_sel_ptg35_etal1p5.writeHistos(year+"_Zmumug_ptg35_etal1p5");
  H_sel_ptg35_etag1p5.writeHistos(year+"_Zmumug_ptg35_etag1p5");
  H_sel_ptg50.writeHistos(year+"_Zmumug_ptg50");
  H_sel_ptg50_etal1p5.writeHistos(year+"_Zmumug_ptg50_etal1p5");
  H_sel_ptg50_etag1p5.writeHistos(year+"_Zmumug_ptg50_etag1p5");
  
  
  outputfile->Close();
  delete outputfile;

  std::cout << "Done. Event loop has been run " << d0.GetNRuns() << " times." << std::endl;
  gBenchmark->Show("running time");

}
