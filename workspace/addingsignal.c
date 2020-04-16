void addingsignal() {
TFile
f("SignalVarRemoved.root","update");
 TTree *tree= (TTree*)f.Get("tree");
 
 Char_t Signal=1;
 TBranch *NewSignal = tree->Branch("Signal",&Signal,"Signal/B");

Int_t nentries = tree->GetEntries();
   for (Int_t i=0;i<nentries;i++) {
     tree->GetEvent(i);
     
     NewSignal->Fill();
   }
   tree->Write();
}
