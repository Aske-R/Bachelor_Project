// R__LOAD_LIBRARY($ROOTSYS/groups/hep/aske/firstdata_Zee_feb_2020/Data/libEvent.so)

void rootcopy()
{
   TString dir = "$ROOTSYS/groups/hep/aske/firstdata_Zee_feb_2020/Data/Split_0.5M_A_Signal_Zee.root_w_mcmc_mcmcfinal_mcdata_nocut_mcdatafinal";
   gSystem->ExpandPathName(dir);
   const auto filename = gSystem->AccessPathName(dir) ? "./Split_0.5M_A_Signal_Zee.root_w_mcmc_mcmcfinal_mcdata_nocut_mcdatafinal" : "$ROOTSYS/groups/hep/aske/firstdata_Zee_feb_2020/Data/Split_0.5M_A_Signal_Zee.root_w_mcmc_mcmcfinal_mcdata_nocut_mcdatafinal";
   TFile oldfile(filename);
   TTree *oldtree;
   oldfile.GetObject("tree", oldtree);
   // Deactivate all branches
   //oldtree->SetBranchStatus("*", 0);
   // Activate only four of them
   for (auto inactiveBranchName : {"Signal"})
      oldtree->SetBranchStatus(inactiveBranchName, 0);
   // Create a new file + a clone of old tree in new file
   TFile newfile("SignalVarRemoved.root", "recreate");
   auto newtree = oldtree->CloneTree();
   newtree->Print();
   newfile.Write();
}
