#include <map>
using namespace std;

map<TString,float> lumis = {{"2016_preVFP",19.5}, {"2016_postVFP",16.8}, {"2017",41.5}, {"2018",59.8}, {"Run2",138.0}};

int binwOOM (TH1F*h, float& binwidth) {//compute order of magnitude of bin width; used to show correct number of decimals when plotting bin width on y axis

  int nbins = h->GetSize()-2;
  int xmin = h->GetBinLowEdge(1); int xmax = h->GetBinLowEdge(nbins+1);
  binwidth = (xmax - xmin)/(float(nbins));
  std::string s_binwidth = to_string(binwidth);
  s_binwidth.erase(s_binwidth.find_last_not_of('0') + 1, std::string::npos); //remove trailing zeros from tstring
  std::string::difference_type n = std::count(s_binwidth.begin(), s_binwidth.end(), '0'); //count number of zeros
  if (s_binwidth.at(0)!='0') return 0; //order of magnitude is 1
  else return -1*n;
  
}

float roundToDecimals(float value, int decimals) {
    float factor = std::pow(10.0f, decimals);
    return std::round(value * factor) / factor;
}
