
#include <iostream>
#include <string>
#include <vector>
#include "TCut.h"
#include "TFile.h"
#include "TTree.h"
#include "Utilities.h"
#include "TColor.h"
#include "TMath.h"
//#include "gROOT.h"
using namespace std;

void Draw(){
	gROOT->SetBatch();
	gStyle->SetOptStat(0);
	gStyle->SetOptTitle(0);

	TFile *histFile = new TFile("output/histograms.root","read");
	histFile->cd();

        vector<string> histogramNames;
        histogramNames.push_back("nsfos");
        histogramNames.push_back("pt");
        histogramNames.push_back("mt");
        histogramNames.push_back("eta");
        histogramNames.push_back("phi");
        histogramNames.push_back("deltaphi");
        histogramNames.push_back("charge");
        histogramNames.push_back("nmuons");
        histogramNames.push_back("njets");
        histogramNames.push_back("nbjets");
        histogramNames.push_back("met");
        histogramNames.push_back("metphi");
        histogramNames.push_back("metsumet");
        histogramNames.push_back("masselel");
        histogramNames.push_back("masselmu");
        histogramNames.push_back("massmumu");
        histogramNames.push_back("masssfos");

        TCanvas *canvas = new TCanvas("canvas","canvas",800,800);
	for(int drawData = 0;drawData<2;drawData++){
		for (vector<string>::iterator histit = histogramNames.begin();
		     histit!=histogramNames.end(); histit++){
		     string name = *histit;
		     TH1F* hSignal = (TH1F*)histFile->Get(("signal_"+name).c_str());
		     TH1F* hBG     = (TH1F*)histFile->Get(("bg_"+name).c_str());
		     TH1F* hData = NULL;
		     if (drawData) hData   = (TH1F*)histFile->Get(("data_"+name).c_str());

		     hBG->Draw("HIST");
		     hBG->SetFillColor(kAzure-9);
		     hBG->SetLineColor(kAzure-8);
		     hBG->SetMarkerColor(kAzure-8);
		     hSignal->Draw("HIST same");
		     hSignal->SetFillColor(kMagenta-3);
		     hSignal->SetLineColor(kMagenta-2);
		     hSignal->SetMarkerColor(kMagenta-2);
		     if(drawData and hData){
			     hData->SetFillColor(kWhite);
			     hData->SetLineColor(kBlack);
			     hData->SetMarkerColor(kBlack);
			     hData->SetMarkerStyle(20);
			     hData->Draw("E1 same");
		     }

		     double maxBG=-1;
		     for(int bin = 1; bin<hBG->GetNbinsX()+1; bin++){
			 if (hBG->GetBinContent(bin) > maxBG) 
				maxBG = hBG->GetBinContent(bin);
		     }

		     double maxSignal=-1;
		     double minSignal=100000000;
		     for(int bin = 1; bin<hSignal->GetNbinsX()+1; bin++){
			 if (hSignal->GetBinContent(bin) > maxSignal) 
				maxSignal = hSignal->GetBinContent(bin);
			 if (hSignal->GetBinContent(bin) < minSignal) 
				minSignal = hSignal->GetBinContent(bin);
		     }



		     canvas->SetLogx(false);
		     if (name=="pt" ||
			 name=="mt" ||
			 name=="met" ||
			 name=="metsumet"){

			 canvas->SetLogx(true);
		     }
			
		
		     canvas->SetLogy(false);
		     hBG->GetYaxis()->SetRangeUser(0.,maxBG*1.2);
		     hBG->GetYaxis()->SetTitleOffset(1.2);
		     hBG->GetXaxis()->SetTitleOffset(1.2);
		     canvas->GetPad(0)->SetTopMargin(.02);
		     canvas->GetPad(0)->SetBottomMargin(.10);
		     canvas->GetPad(0)->SetRightMargin(.04);
		     canvas->GetPad(0)->SetLeftMargin(.10);
		     canvas->GetPad(0)->RedrawAxis();
		     if (drawData) canvas->SaveAs(("output/plots/unblinded/linearY/"+name+".png").c_str());
		     else canvas->SaveAs(("output/plots/blinded/linearY/"+name+".png").c_str());
		     canvas->SetLogy(true);
		     double min = (minSignal+(maxSignal-minSignal)*0.1)/10.;
		     std::cout << "min: " << min << std::endl;
		     hBG->GetYaxis()->SetRangeUser(min,maxBG*10.);
		     canvas->GetPad(0)->RedrawAxis();
		     if (drawData) canvas->SaveAs(("output/plots/unblinded/logY/"+name+".png").c_str());
		     else canvas->SaveAs(("output/plots/blinded/logY/"+name+".png").c_str());


		}
	}


}

