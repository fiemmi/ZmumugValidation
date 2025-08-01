#include "DrawVariable.h"

void DrawVariable(TString VAR,TString YEAR,TString CAT,bool LOG,int iSyst,int REBIN,float XMIN,float XMAX,float RATIOYMIN,float RATIOYMAX,TString XTITLE,TString SEL1,TString SEL2,TString SEL3,TString SEL4, bool isINT,int XNDIV,bool PRINT=false,bool isInclusive=false, bool applyFNUF=true)
{
  gROOT->ForceStyle();
  gROOT->SetBatch(kTRUE); //kTRUE ---> histos are not showed while drawn. You can avoid crashes with this
  
  std::vector<TString> HISTOS = { };
  if(applyFNUF){ 
     HISTOS = {
       VAR+"_"+YEAR+"_"+CAT,
       VAR+"_FNUFUp_"+YEAR+"_"+CAT,
       VAR+"_FNUFDown_"+YEAR+"_"+CAT,
       VAR+"_ScaleUp_"+YEAR+"_"+CAT,
       VAR+"_ScaleDown_"+YEAR+"_"+CAT,
       VAR+"_SmearUp_"+YEAR+"_"+CAT,
       VAR+"_SmearDown_"+YEAR+"_"+CAT,
       VAR+"_RochUp_"+YEAR+"_"+CAT,
       VAR+"_RochDown_"+YEAR+"_"+CAT,    
     };
  }else{  
     HISTOS = {
       VAR+"_"+YEAR+"_"+CAT,
       VAR+"_ScaleUp_"+YEAR+"_"+CAT,
       VAR+"_ScaleDown_"+YEAR+"_"+CAT,
       VAR+"_SmearUp_"+YEAR+"_"+CAT,
       VAR+"_SmearDown_"+YEAR+"_"+CAT,
       VAR+"_RochUp_"+YEAR+"_"+CAT,
       VAR+"_RochDown_"+YEAR+"_"+CAT,    
     };
  }

  TFile *inf_data = new TFile("../makeHistos_output_ZmmgTree_Run2_data.root", "READ");
  TFile *inf_MC = new TFile("../makeHistos_output_ZmmgTree_Run2_MC.root", "READ");
  TH1F  *h[(int)HISTOS.size()*2];

  TCanvas *can = new TCanvas("DataVsMC_"+VAR+"_"+YEAR+"_"+CAT,"DataVsMC_"+VAR+"_"+YEAR+"_"+CAT,800,700);
  can->SetSupportGL(true); //support transparency

  //read histograms for data
  for(int i=0;i<(int)HISTOS.size();i++) {
    //std::cout << i << std::endl;
    //std::cout << HISTOS.at(i) << std::endl;
    h[i] = (TH1F*)inf_data->Get(HISTOS.at(i));
    //std::cout << h[i]->Integral() << std::endl;
    if (!h[i]) {
      cout<<"Histogram does not exist !!!"<<endl;
      break;
    }
    h[i]->SetDirectory(0);
    h[i]->Rebin(REBIN);
    h[i]->SetLineWidth(1);
    h[i]->SetLineColor(kBlack);
  }
  //read histograms for MC
  for(int i=(int)HISTOS.size();i<2*(int)HISTOS.size();i++) {
    //std::cout << i << std::endl;
    //std::cout << HISTOS.at(i-(int)HISTOS.size()) << std::endl;
    h[i] = (TH1F*)inf_MC->Get(HISTOS.at(i-(int)HISTOS.size()));
    //std::cout << h[i]->Integral() << std::endl;
    if (!h[i]) {
      cout<<"Histogram does not exist !!!"<<endl;
      break;
    }
    h[i]->SetDirectory(0);
    h[i]->Rebin(REBIN);
    h[i]->SetLineWidth(1);
    h[i]->SetLineColor(kBlack);
  }

  inf_data->Close();
  inf_MC->Close();
  
  h[0]->SetLineWidth(2);//data
  h[(int)HISTOS.size()]->SetFillColor(kGreen-3);//Zmumug
  
  cout<<"======== "<<VAR+"_"+YEAR+"_"+CAT<<" ====================="<<endl;
  cout<<"Data events:  "<<h[0]->Integral()<<endl;
  cout<<"Zee events:  "<<h[(int)HISTOS.size()]->Integral()<<endl;


  TH1F * uncBand_stat = (TH1F*)h[(int)HISTOS.size()]->Clone();
  TH1F * uncBand = (TH1F*)h[(int)HISTOS.size()]->Clone();
  TH1F * uncBandRatio_stat = (TH1F*)h[(int)HISTOS.size()]->Clone();
  TH1F * uncBandRatio = (TH1F*)h[(int)HISTOS.size()]->Clone();
  //compute uncertainty bands. Deal with data-to-data and MC-to-MC differences separately
  for (int ibin = 0; ibin < h[0]->GetSize()-2; ibin++){//loop over bins of data histogram; MC histogram has same binning anyway
    float binContentUp = pow(h[0]->GetBinError(ibin+1),2) + pow(h[(int)HISTOS.size()]->GetBinError(ibin+1),2); //statistical component of uncertainty, quad-sum of statistical uncertainty in data and MC
    float binContentDown = pow(h[0]->GetBinError(ibin+1),2) + pow(h[(int)HISTOS.size()]->GetBinError(ibin+1),2); //statistical component of uncertainty, quad-sum of statistical uncertainty in data and MC
    uncBand_stat->SetBinError(ibin+1, (sqrt(binContentUp) + sqrt(binContentDown))/2.);
    uncBandRatio_stat->SetBinContent(ibin+1, 1.);
    uncBandRatio_stat->SetBinError(ibin+1,((sqrt(binContentUp) + sqrt(binContentDown))/2.)/h[(int)HISTOS.size()]->GetBinContent(ibin+1)); //compute relative stat uncertainty wrt MC 
    for (int ihisto = iSyst; ihisto < (int)HISTOS.size(); ihisto++){ //deal with data-to-data differences
      if (h[0]->GetBinContent(ibin+1) <= h[ihisto]->GetBinContent(ibin+1)) binContentUp += pow((h[0]->GetBinContent(ibin+1)-h[ihisto]->GetBinContent(ibin+1)),2); //sum quads of differences between nominal data and shifts
      else binContentDown += pow((h[0]->GetBinContent(ibin+1)-h[ihisto]->GetBinContent(ibin+1)),2);
    }
    for (int ihisto = (int)HISTOS.size()+iSyst; ihisto < 2*(int)HISTOS.size(); ihisto++){ //deal with MC-to-MC differences
      if (h[(int)HISTOS.size()]->GetBinContent(ibin+1) <= h[ihisto]->GetBinContent(ibin+1)) binContentUp += pow((h[(int)HISTOS.size()]->GetBinContent(ibin+1)-h[ihisto]->GetBinContent(ibin+1)),2); //sum quads of differences between nominal MC and shifts
      else binContentDown += pow((h[(int)HISTOS.size()]->GetBinContent(ibin+1)-h[ihisto]->GetBinContent(ibin+1)),2);
    }
    binContentUp = sqrt(binContentUp);
    binContentDown = sqrt(binContentDown);
    float binContent = (binContentUp + binContentDown)/2.;
    uncBand->SetBinError(ibin+1, binContent);
    uncBandRatio->SetBinContent(ibin+1,1);
    uncBandRatio->SetBinError(ibin+1,binContent/h[(int)HISTOS.size()]->GetBinContent(ibin+1));
  }
  
  uncBand_stat->SetFillColorAlpha(kOrange+2, 0.90);
  uncBand->SetFillColorAlpha(kRed, 0.890);
  uncBand->SetLineColor(kRed);
  uncBand->SetLineWidth(2);
  uncBand->SetFillStyle(3001);
  uncBand_stat->SetMarkerSize(0);
  uncBand->SetMarkerSize(0);
  uncBand_stat->Scale(h[0]->Integral()/uncBand_stat->Integral());
  uncBand->Scale(h[0]->Integral()/uncBand->Integral());
  uncBandRatio_stat->SetFillColorAlpha(kOrange+2, 0.90);
  uncBandRatio_stat->SetMarkerSize(0);
  uncBandRatio->SetFillColorAlpha(kRed, 0.90);
  uncBandRatio->SetFillStyle(3001);
  uncBandRatio->SetMarkerSize(0);
  
  TH1F *hRatio = (TH1F*)h[0]->Clone("Ratio");
  hRatio->SetLineWidth(2);
  h[(int)HISTOS.size()]->Scale(h[0]->Integral()/h[(int)HISTOS.size()]->Integral());
  hRatio->Divide(h[(int)HISTOS.size()]);

  TLegend *leg = new TLegend(0.76,0.7,0.89,0.9);
  leg->SetFillColor(0);
  leg->SetTextFont(42);
  leg->SetTextSize(0.03);
  leg->AddEntry(h[0], "Data", "p");
  leg->AddEntry(h[(int)HISTOS.size()],"Z(#mu#mu#gamma)","F");
  leg->AddEntry(uncBand, "Stat. #oplus syst.", "F");
  
  can->SetBottomMargin(0.25);
  TH1F *hAux = (TH1F*)h[0]->Clone("aux");
  hAux->Reset();
  hAux->GetXaxis()->SetNdivisions(XNDIV);
  hAux->GetYaxis()->SetMaxDigits(4); //force scientific notation on y axis after 3 digit numbers
  if (isINT) {
    hAux->GetXaxis()->CenterLabels();
  }
  //properly set range so that uncertainty bands are always contained in canvas
  float m = 0.;
  for (int i = 0; i < uncBand->GetSize()-2; i++) {
    float mym = uncBand->GetBinContent(i+1) + uncBand->GetBinError(i+1);
    if (mym > m) m = mym;
  }
  hAux->GetYaxis()->SetRangeUser(0.5,1.1*m);
  if (LOG) {
    gPad->SetLogy(); 
    hAux->GetYaxis()->SetRangeUser(0.5,2*m);
  }
  hAux->GetXaxis()->SetRangeUser(XMIN,XMAX);
  //compute bin width
  float binwidth;
  int n = binwOOM(h[(int)HISTOS.size()], binwidth);
  string unit;
  if (XTITLE.Index("GeV")!=-1) unit = "GeV";
  else unit = "";
  if (n==0) hAux->GetYaxis()->SetTitle(TString::Format("Events / %1.0f %s",binwidth, unit.c_str()));
  else if (n==-1) hAux->GetYaxis()->SetTitle(TString::Format("Events / %1.1f %s",binwidth, unit.c_str()));
  else if (n==-2) hAux->GetYaxis()->SetTitle(TString::Format("Events / %1.2f %s",binwidth, unit.c_str()));
  else if (n==-3) hAux->GetYaxis()->SetTitle(TString::Format("Events / %1.3f %s",binwidth, unit.c_str()));
  else hAux->GetYaxis()->SetTitle(TString::Format("Events / %1.4f %s",binwidth, unit.c_str()));
  hAux->GetXaxis()->SetTitle("");
  hAux->GetXaxis()->SetLabelSize(0.0);
  hAux->Draw();

  h[(int)HISTOS.size()]->Draw("hist same");
  //uncBand_stat->Draw("same E2");
  uncBand->Draw("same E2");
  h[0]->Draw("sames EX0");

  leg->Draw();
  gPad->RedrawAxis();

  /*
  //Fit peak positions in data and MC and find difference
  TF1 * g_d = new TF1("g_d","gaus",h[0]->GetMean()-0.5*h[0]->GetRMS(),h[0]->GetMean()+0.5*h[0]->GetRMS());
  TF1 * g_mc = new TF1("g_mc","gaus",h[(int)HISTOS.size()]->GetMean()-0.5*h[(int)HISTOS.size()]->GetRMS(),h[(int)HISTOS.size()]->GetMean()+0.5*h[(int)HISTOS.size()]->GetRMS());
  auto result_d = h[0]->Fit("g_d", "R");
  auto result_mc = h[(int)HISTOS.size()]->Fit("g_mc", "R");
  float mean_d = g_d->GetParameter(1);
  float mean_d_err = g_d->GetParError(1);
  float mean_mc = g_mc->GetParameter(1);
  float mean_mc_err = g_mc->GetParError(1);
  TLatex dm;
  dm.SetTextFont(61);
  dm.SetTextSize(0.05);
  std::cout << Form("#Delta m = %f #pm %f", mean_d - mean_mc, sqrt(pow(mean_d_err,2) + pow(mean_mc_err,2))) << std::endl;
  dm.DrawLatexNDC(0.20,0.57,Form("#Delta m = %f #pm %f", mean_d - mean_mc, sqrt(pow(mean_d_err,2) + pow(mean_mc_err,2))));
  */
  
  TPad *pad = new TPad("pad","pad",0.,0.,1.,1.);
  pad->SetTopMargin(0.77);
  pad->SetFillColor(0);
  pad->SetFillStyle(0);
  pad->Draw();
  pad->cd(0);
  pad->SetGridy();
  hRatio->GetXaxis()->SetTitleOffset(0.95);
  hRatio->GetYaxis()->SetTitleOffset(1.5);
  hRatio->GetYaxis()->SetTickLength(0.06);
  hRatio->GetYaxis()->SetTitleSize(0.03);
  hRatio->GetYaxis()->SetLabelSize(0.04);
  hRatio->GetYaxis()->SetTitle("Data/MC");
  hRatio->GetXaxis()->SetTitle(XTITLE);
  hRatio->GetXaxis()->SetRangeUser(XMIN,XMAX);
  

  //properly set range so that uncertainty bands are always contained in canvas
  /*
  float mm = 0.;
  for (int i = 0; i < uncBand->GetSize()-2; i++) {
    float mym = uncBandRatio->GetBinContent(i+1) + uncBandRatio->GetBinError(i+1);
    if (mym > mm) mm = mym;
  }
  if (abs(mm-1)>0.4) mm = 0.4;
  hRatio->GetYaxis()->SetRangeUser(1-1.25*abs(1-mm),1+1.25*abs(1-mm));
  */

  
  hRatio->GetYaxis()->SetRangeUser(RATIOYMIN, RATIOYMAX);
  hRatio->GetYaxis()->SetNdivisions(505);
  hRatio->GetXaxis()->SetNdivisions(XNDIV);
  hRatio->GetYaxis()->SetLabelSize(0.03);
  if (isINT) {
    hRatio->GetXaxis()->CenterLabels();
  }
  hRatio->Draw("same EX0");
  uncBandRatio->Draw("same E2");
  uncBandRatio_stat->Draw("same E2");
  hRatio->Draw("same EX0");

  TLegend *legRatio = new TLegend(0.56,0.14,0.89,0.17);
  legRatio->SetNColumns(2);
  legRatio->SetFillColor(0);
  legRatio->SetFillStyle(0);
  legRatio->SetTextFont(42);
  legRatio->SetTextSize(0.03);
  legRatio->AddEntry(uncBandRatio_stat, "Stat.", "F");
  legRatio->AddEntry(uncBandRatio,"Stat. #oplus syst.","F");
  legRatio->Draw();
  
  
  TLatex CMS;
  CMS.SetTextFont(61);
  CMS.SetTextSize(0.05);
  CMS.DrawLatexNDC(0.20,0.87,"CMS");
  CMS.SetTextFont(52);
  CMS.DrawLatexNDC(0.31,0.87,"Preliminary");
  TString year;
  if (YEAR.Index("pre") != -1) year = "2016_preVFP";
  else if (YEAR.Index("post") != -1) year = "2016_postVFP";
  else if (YEAR.Index("2017") != -1) year = "2017";
  else if (YEAR.Index("2018") != -1) year = "2018";
  else if (YEAR.Index("Run2") != -1) year = "Run2";
  else year = "XXX";
  TLatex lumi;
  lumi.SetTextSize(0.04);
  lumi.SetTextFont(42);
  lumi.DrawLatexNDC(0.715,0.95, Form("%1.1f fb^{-1} (13 TeV)", lumis[year]));

  TLatex sel;
  sel.SetTextFont(42);
  TString region;
  if (CAT.Index("notEBEB") != -1) region = "notEBEB";
  else region = "EBEB";
  sel.SetTextSize(0.03);
  sel.DrawLatexNDC(0.2, 0.8, SEL1);
  TString ETcut;
  if (CAT.Index("ETg") != -1) ETcut = "E^{e}_{T} > 80 GeV";
  else ETcut = "E^{e}_{T} < 80 GeV";
  sel.DrawLatexNDC(0.2, 0.75, SEL2);
  TString BDTcut;
  if (CAT.Index("BDTg") != -1) BDTcut = "diphotonBDT > 0.3";
  else BDTcut = "XXXXXX";
  sel.DrawLatexNDC(0.2, 0.70, SEL3);

  //compute Chi2/ndof
  TH1F * hd = (TH1F*)h[0]->Clone();
  TH1F * hmc = (TH1F*)h[(int)HISTOS.size()]->Clone();
  double chi2 = 0.;
  int ndf = 0;
  int igood = 0;
  /*
  for (int ibin = 0; ibin < hd->GetSize()-2; ibin++) {
    hmc->SetBinError(ibin, sqrt(pow(hmc->GetBinError(ibin),2) + pow(hd->GetBinError(ibin),2))); //assign quad-sum of errors in data and MC to MC
    hd->SetBinError(ibin+1,0); //assign 0 error to data
  }
  */
  double p_val = hd->Chi2TestX(hmc,chi2,ndf,igood,"WW");
  sel.DrawLatexNDC(0.2, 0.65, SEL4 + Form("#chi^{2}/dof = %.2f/%i", chi2, hd->GetSize()-3));
  
  TString isInclusive_str = "";
  if (isInclusive) isInclusive_str = "inclusive";
  else isInclusive_str = "exclusive"; 
  
  TString applyFNUF_str = "";
  if (applyFNUF) applyFNUF_str = "withFNUF";
  else applyFNUF_str = "noFNUF"; 
  
  if (PRINT) {//save plots
    can->SaveAs(VAR+"_"+YEAR+"_"+CAT+"_"+isInclusive_str+"_"+applyFNUF_str+".pdf","pdf");
    can->SaveAs(VAR+"_"+YEAR+"_"+CAT+"_"+isInclusive_str+"_"+applyFNUF_str+".png","png");
  }
  
}
