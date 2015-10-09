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
	TCut threeLepCut = "Sum$(lep_pt > 20000) >= 3";
	cuts += threeLepCut;
	std::cout << "Cuts are:"<<std::endl;
	cuts.Print();


	std::cout << "Signal+BG:" <<std::endl;
	TFile *inputTreeFile = new TFile("input/combined.root");
	//TFile *inputTreeFile = new TFile("input/data.root");
	//TFile *inputTreeFile = new TFile("input/signal.root");
	TTree *inputTree = (TTree*)inputTreeFile->Get("physics");
	TFile *outputTreeFile = new TFile("output/output.root","recreate");
	//TFile *outputTreeFile = new TFile("output/data.root","recreate");
	float  nEventsBefore = inputTree->GetEntries();
	std::cout << "# Entries before cuts: " << nEventsBefore << std::endl;
	string outputTreeName = "physics_cut";
	inputTree->CopyTree(cuts)->Write(outputTreeName.c_str());
	outputTreeFile->Write();
	TTree *outputTree = (TTree*)outputTreeFile->Get(outputTreeName.c_str());
	float  nEventsAfter = outputTree->GetEntries();
	std::cout << "# Entries after cuts: " << nEventsAfter << std::endl;
	if (nEventsBefore!=0.) std::cout << "Filter Efficiency = " <<  nEventsAfter/nEventsBefore << std::endl;
	outputTreeFile->Close();
	inputTreeFile->Close();

	std::cout << "Data:" <<std::endl;
	TFile *inputDataTreeFile = new TFile("input/data.root");
	TTree *inputDataTree = (TTree*)inputDataTreeFile->Get("physics");
	TFile *outputDataTreeFile = new TFile("output/dataoutput.root","recreate");
	//TFile *outputTreeFile = new TFile("output/data.root","recreate");
	nEventsBefore = inputDataTree->GetEntries();
	std::cout << "# Entries before cuts: " << nEventsBefore << std::endl;
	outputTreeName = "physics_cut";
	inputDataTree->CopyTree(cuts)->Write(outputTreeName.c_str());
	outputDataTreeFile->Write();
	TTree *outputDataTree = (TTree*)outputDataTreeFile->Get(outputTreeName.c_str());
	nEventsAfter = outputDataTree->GetEntries();
	std::cout << "# Entries after cuts: " << nEventsAfter << std::endl;
	if (nEventsBefore!=0.) std::cout << "Filter Efficiency = " <<  nEventsAfter/nEventsBefore << std::endl;
	outputDataTreeFile->Close();
	inputDataTreeFile->Close();

	

}

