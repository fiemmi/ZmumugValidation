ROOT::RDF::RNode defineQuantitiesOfInterest (ROOT::RDF::RNode f) {
  //"one" quantity. This is a dummy quantity that is used, in data, as a per-event weight when filling histograms
  f = f.Define("one", "return 1");
  return f;
};

class Histogrammer {

public:
  //initialize histograms to be produced as public members here
  ROOT::RDF::RResultPtr<TH1D> h_CMS_mumug_mass;
  ROOT::RDF::RResultPtr<TH1D> h_CMS_mumug_mass_FNUFUp;
  ROOT::RDF::RResultPtr<TH1D> h_CMS_mumug_mass_FNUFDown;
  ROOT::RDF::RResultPtr<TH1D> h_CMS_mumug_mass_ScaleUp;
  ROOT::RDF::RResultPtr<TH1D> h_CMS_mumug_mass_ScaleDown;
  ROOT::RDF::RResultPtr<TH1D> h_CMS_mumug_mass_SmearUp;
  ROOT::RDF::RResultPtr<TH1D> h_CMS_mumug_mass_SmearDown;
  ROOT::RDF::RResultPtr<TH1D> h_CMS_mumug_mass_RochUp;
  ROOT::RDF::RResultPtr<TH1D> h_CMS_mumug_mass_RochDown;
  ROOT::RDF::RResultPtr<TH1D> h_CMS_mumug_mass_noFNUF;
  ROOT::RDF::RResultPtr<TH1D> h_CMS_mumug_mass_noFNUF_ScaleUp;
  ROOT::RDF::RResultPtr<TH1D> h_CMS_mumug_mass_noFNUF_ScaleDown;
  ROOT::RDF::RResultPtr<TH1D> h_CMS_mumug_mass_noFNUF_SmearUp;
  ROOT::RDF::RResultPtr<TH1D> h_CMS_mumug_mass_noFNUF_SmearDown;
  ROOT::RDF::RResultPtr<TH1D> h_CMS_mumug_mass_noFNUF_RochUp;
  ROOT::RDF::RResultPtr<TH1D> h_CMS_mumug_mass_noFNUF_RochDown;
  
  void defineHistos(ROOT::RDF::RNode f, bool isData);
  std::vector<ROOT::RDF::RResultPtr<TH1D>> getAllHistograms();
  void writeHistos(TString name);
};

void Histogrammer::defineHistos (ROOT::RDF::RNode f, bool isData) {
  
  std::string_view weight;
  if (isData) weight = "one"; //weight of 1 if data
  else weight = "FinalWeight"; //use weight defined in makeHistos.cpp, it's the product of two weights, defined in the input dataframe via .Define() (done in the main script)
  
  //define histograms here
  this->h_CMS_mumug_mass = f.Histo1D({"CMS_mumug_mass", "CMS_mumug_mass", 200u, 80., 100.}, "mass_ScaleSmeared_FnufCorrected", weight); //all corrections applied
  this->h_CMS_mumug_mass_FNUFUp = f.Histo1D({"CMS_mumug_mass_FNUFUp", "CMS_mumug_mass_FNUFUp", 200u, 80., 100.}, "mass_ScaleSmeared_FnufCorrected_1sigmaUpFnuf", weight); 
  this->h_CMS_mumug_mass_FNUFDown = f.Histo1D({"CMS_mumug_mass_FNUFDown", "CMS_mumug_mass_FNUFDown", 200u, 80., 100.}, "mass_ScaleSmeared_FnufCorrected_1sigmaDnFnuf", weight); 
  this->h_CMS_mumug_mass_ScaleUp = f.Histo1D({"CMS_mumug_mass_ScaleUp", "CMS_mumug_mass_ScaleUp", 200u, 80., 100.}, "mass_ScaleSmeared_FnufCorrected_1sigmaUpScale", weight); 
  this->h_CMS_mumug_mass_ScaleDown = f.Histo1D({"CMS_mumug_mass_ScaleDown", "CMS_mumug_mass_ScaleDown", 200u, 80., 100.}, "mass_ScaleSmeared_FnufCorrected_1sigmaDnScale", weight);
  this->h_CMS_mumug_mass_SmearUp = f.Histo1D({"CMS_mumug_mass_SmearUp", "CMS_mumug_mass_SmearUp", 200u, 80., 100.}, "mass_ScaleSmeared_FnufCorrected_1sigmaUpSmear", weight); 
  this->h_CMS_mumug_mass_SmearDown = f.Histo1D({"CMS_mumug_mass_SmearDown", "CMS_mumug_mass_SmearDown", 200u, 80., 100.}, "mass_ScaleSmeared_FnufCorrected_1sigmaDnSmear", weight);
  this->h_CMS_mumug_mass_RochUp = f.Histo1D({"CMS_mumug_mass_RochUp", "CMS_mumug_mass_RochUp", 200u, 80., 100.}, "mass_ScaleSmeared_FnufCorrected_1sigmaUpMuRoc", weight); 
  this->h_CMS_mumug_mass_RochDown = f.Histo1D({"CMS_mumug_mass_RochDown", "CMS_mumug_mass_RochDown", 200u, 80., 100.}, "mass_ScaleSmeared_FnufCorrected_1sigmaDnMuRoc", weight);
  this->h_CMS_mumug_mass_noFNUF = f.Histo1D({"CMS_mumug_mass_noFNUF", "CMS_mumug_mass", 200u, 80., 100.}, "mass_ScaleSmeared", weight); //no FNUF corrections
  this->h_CMS_mumug_mass_noFNUF_ScaleUp = f.Histo1D({"CMS_mumug_mass_noFNUF_ScaleUp", "CMS_mumug_mass_ScaleUp", 200u, 80., 100.}, "mass_ScaleSmeared_1sigmaUpScale", weight); 
  this->h_CMS_mumug_mass_noFNUF_ScaleDown = f.Histo1D({"CMS_mumug_mass_noFNUF_ScaleDown", "CMS_mumug_mass_ScaleDown", 200u, 80., 100.}, "mass_ScaleSmeared_1sigmaDnScale", weight);
  this->h_CMS_mumug_mass_noFNUF_SmearUp = f.Histo1D({"CMS_mumug_mass_noFNUF_SmearUp", "CMS_mumug_mass_SmearUp", 200u, 80., 100.}, "mass_ScaleSmeared_1sigmaUpSmear", weight); 
  this->h_CMS_mumug_mass_noFNUF_SmearDown = f.Histo1D({"CMS_mumug_mass_noFNUF_SmearDown", "CMS_mumug_mass_SmearDown", 200u, 80., 100.}, "mass_ScaleSmeared_1sigmaDnSmear", weight);
  this->h_CMS_mumug_mass_noFNUF_RochUp = f.Histo1D({"CMS_mumug_mass_noFNUF_RochUp", "CMS_mumug_mass_RochUp", 200u, 80., 100.}, "mass_ScaleSmeared_1sigmaUpMuRoc", weight); 
  this->h_CMS_mumug_mass_noFNUF_RochDown = f.Histo1D({"CMS_mumug_mass_noFNUF_RochDown", "CMS_mumug_mass_RochDown", 200u, 80., 100.}, "mass_ScaleSmeared_1sigmaDnMuRoc", weight);
  
}

std::vector<ROOT::RDF::RResultPtr<TH1D>> Histogrammer::getAllHistograms() {
  return {
    h_CMS_mumug_mass,
    h_CMS_mumug_mass_FNUFUp,
    h_CMS_mumug_mass_FNUFDown,
    h_CMS_mumug_mass_ScaleUp,
    h_CMS_mumug_mass_ScaleDown,
    h_CMS_mumug_mass_SmearUp,
    h_CMS_mumug_mass_SmearDown,
    h_CMS_mumug_mass_RochUp,
    h_CMS_mumug_mass_RochDown,
    h_CMS_mumug_mass_noFNUF,
    h_CMS_mumug_mass_noFNUF_ScaleUp,
    h_CMS_mumug_mass_noFNUF_ScaleDown,
    h_CMS_mumug_mass_noFNUF_SmearUp,
    h_CMS_mumug_mass_noFNUF_SmearDown,
    h_CMS_mumug_mass_noFNUF_RochUp,
    h_CMS_mumug_mass_noFNUF_RochDown
  };
}

void Histogrammer::writeHistos (TString name) {
  //instructions to write histograms here
  this->h_CMS_mumug_mass->Write(TString(this->h_CMS_mumug_mass->GetName())+"_"+name);
  this->h_CMS_mumug_mass_FNUFUp->Write(TString(this->h_CMS_mumug_mass_FNUFUp->GetName())+"_"+name);
  this->h_CMS_mumug_mass_FNUFDown->Write(TString(this->h_CMS_mumug_mass_FNUFDown->GetName())+"_"+name);
  this->h_CMS_mumug_mass_ScaleUp->Write(TString(this->h_CMS_mumug_mass_ScaleUp->GetName())+"_"+name);
  this->h_CMS_mumug_mass_ScaleDown->Write(TString(this->h_CMS_mumug_mass_ScaleDown->GetName())+"_"+name);
  this->h_CMS_mumug_mass_SmearUp->Write(TString(this->h_CMS_mumug_mass_SmearUp->GetName())+"_"+name);
  this->h_CMS_mumug_mass_SmearDown->Write(TString(this->h_CMS_mumug_mass_SmearDown->GetName())+"_"+name);
  this->h_CMS_mumug_mass_RochUp->Write(TString(this->h_CMS_mumug_mass_RochUp->GetName())+"_"+name);
  this->h_CMS_mumug_mass_RochDown->Write(TString(this->h_CMS_mumug_mass_RochDown->GetName())+"_"+name);
  this->h_CMS_mumug_mass_noFNUF->Write(TString(this->h_CMS_mumug_mass_noFNUF->GetName())+"_"+name);
  this->h_CMS_mumug_mass_noFNUF_ScaleUp->Write(TString(this->h_CMS_mumug_mass_noFNUF_ScaleUp->GetName())+"_"+name);
  this->h_CMS_mumug_mass_noFNUF_ScaleDown->Write(TString(this->h_CMS_mumug_mass_noFNUF_ScaleDown->GetName())+"_"+name);
  this->h_CMS_mumug_mass_noFNUF_SmearUp->Write(TString(this->h_CMS_mumug_mass_noFNUF_SmearUp->GetName())+"_"+name);
  this->h_CMS_mumug_mass_noFNUF_SmearDown->Write(TString(this->h_CMS_mumug_mass_noFNUF_SmearDown->GetName())+"_"+name);
  this->h_CMS_mumug_mass_noFNUF_RochUp->Write(TString(this->h_CMS_mumug_mass_noFNUF_RochUp->GetName())+"_"+name);
  this->h_CMS_mumug_mass_noFNUF_RochDown->Write(TString(this->h_CMS_mumug_mass_noFNUF_RochDown->GetName())+"_"+name);
  
}

