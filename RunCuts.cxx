#include <iostream>
#include <string>
#include <vector>
#include "TCut.h"
#include "TFile.h"
#include "TTree.h"
using namespace std;

void RunCuts(){
	ifstream cutsFile;
	string cutsFilename = "output/cuts.txt";
	cutsFile.open(cutsFilename);
	if (!cutsFile.is_open()){
	    std::cerr << "Can't open "<<cutsFilename << std::endl;
	    return;
	}
	std::cout << "Using cuts file: "<<cutsFilename<<std::endl;
	string line;
	TCut cuts;
	while(getline(cutsFile,line)){
	    std::cout << line <<std::endl;
	    TCut cut = line.c_str();
	    cuts+=cut;
	}
	std::cout << "Cuts are:"<<std::endl;
	cuts.Print();

	TCut weight = "weight_xsec*weight_mc*weight_reco*weight_trigger*weight_chargemisid*weight_pileup*weight_mxm*weight_btag_eff85";

	TFile *inputTreeFile = new TFile("input/test.root");
	TTree *inputTree = (TTree*)inputTreeFile->Get("physics");
	TFile *outputTreeFile = new TFile("output/output.root","recreate");
	float  nEventsBefore = inputTree->GetEntries();
	std::cout << "# Entries before cuts: " << nEventsBefore << std::endl;
	string outputTreeName = "physics_cut";
	inputTree->CopyTree(cuts)->Write(outputTreeName.c_str());
	outputTreeFile->Write();
	TTree *outputTree = (TTree*)outputTreeFile->Get(outputTreeName.c_str());
	float  nEventsAfter = outputTree->GetEntries();
	std::cout << "# Entries before cuts: " << nEventsAfter << std::endl;
	if (nEventsBefore!=0.) std::cout << "Filter Efficiency = " <<  nEventsAfter/nEventsBefore << std::endl;
	outputTreeFile->Close();
	inputTreeFile->Close();

	

}

