#include "defineFunctions.cpp"

struct SelectionContext {
  std::string name;
  ROOT::RDF::RNode node;
  Histogrammer histo;
};

// Define all selection filters here
std::map<std::string, std::string> baseSelections = {
  {"ptg20", "1>0"}, //just what you have in input dataframe
  {"ptg25", "pho_pt_ScaleSmeared*pho_FnufCorr > 25."},
  {"pt20to35", "pho_pt_ScaleSmeared*pho_FnufCorr >= 20. && pho_pt_ScaleSmeared*pho_FnufCorr < 35."},
  {"pt35to50", "pho_pt_ScaleSmeared*pho_FnufCorr >= 35. && pho_pt_ScaleSmeared*pho_FnufCorr < 50."},
  {"ptg50", "pho_pt_ScaleSmeared*pho_FnufCorr >= 50."}
};

std::map<std::string, std::string> etaCuts = {
  {"", ""},
  {"_etal1p5", "fabs(pho_sceta) < 1.5"},
  {"_etag1p5", "fabs(pho_sceta) >= 1.5"}
};

std::map<std::string, std::string> r9Cuts = {
  {"", ""},
  {"_r9l0p96", "pho_full5x5_r9Corr < 0.96"},
  {"_r9g0p96", "pho_full5x5_r9Corr >= 0.96"}
};

std::vector<SelectionContext> allSelections;

void defineAllSelections(ROOT::RDF::RNode base, std::vector<ROOT::RDF::RResultHandle>& allHistHandles, bool isData, const std::string& year) {
  for (const auto& [ptName, ptCut] : baseSelections) {
    auto df_pt = base.Filter(ptCut);

    for (const auto& [r9Name, r9Cut] : r9Cuts) {
      ROOT::RDF::RNode df_r9 = (r9Cut.empty() ? df_pt : df_pt.Filter(r9Cut));

      for (const auto& [etaName, etaCut] : etaCuts) {
        ROOT::RDF::RNode df_eta = (etaCut.empty() ? df_r9 : df_r9.Filter(etaCut));

        std::string fullName = ptName + r9Name + etaName;
        //std::cout << "dealing with selection " << fullName << std::endl;

        df_eta = defineQuantitiesOfInterest(df_eta); //add any quantity of interest to the input dataframe (e.g., a custom weight to be applied to the events)

        Histogrammer H;
        H.defineHistos(df_eta, isData);
        auto handles = H.getAllHistograms();
        for (auto& h : handles) {
          allHistHandles.push_back(h); // implicit conversion to RResultHandle
        }
        allSelections.push_back({fullName, df_eta, std::move(H)});
      }
    }
  }

  // Trigger the event loop just once
  ROOT::RDF::RunGraphs(allHistHandles);

  // Write histograms after loop
  for (auto& ctx : allSelections) {
    ctx.histo.writeHistos(year + "_Zmumug_" + ctx.name);
  }
}
