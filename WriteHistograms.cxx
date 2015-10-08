#include <iostream>
#include <string>
#include <vector>
#include "TCut.h"
#include "TFile.h"
#include "TTree.h"
#include "Utilities.h"
#include "TMath.h"
//#include "gROOT.h"
using namespace std;

void WriteHistograms(){
	gROOT->SetBatch();
	TCut weight = "weight_norm*weight_xsec*weight_mc*weight_reco*weight_trigger*weight_chargemisid*weight_pileup*weight_mxm*weight_btag_eff85";
	TCut signalCut = "isSignal==1";
	TCut bgCut = "isBG==1";

	TFile *predictionFile = new TFile("output/output.root");
	TTree *tree = (TTree*)predictionFile->Get("physics");
	TFile *dataFile = new TFile("output/dataoutput.root");
	TTree *dataTree = (TTree*)dataFile->Get("physics");



	
	double lumi = 20.3;
	TFile *outFile = new TFile("output/histograms.root","recreate");
	outFile->cd();

	int nbins = 30;
	double bins[nbins+1];
	getLogBins(nbins,bins,20.,1000.);
	double longbins[nbins+1];
	getLogBins(nbins,longbins,100.,10000.);
	//so that bins are split around zmass of 91.1876 GeV
	double massBinLow = 1.1876;
	double massBinHigh = 201.1876;

	TCanvas *canvas = new TCanvas("canvas","canvas",800,800);

        TH1F *hSignalNSFOS = new TH1F("signal_nsfos","signal_nsfos; N_{SFOS}; Events",3,-.5,2.5);
        TH1F *hSignalPt = new TH1F("signal_pt","signal_pt; p_{T}(lll) [GeV]; Events",nbins,bins);
        TH1F *hSignalMt = new TH1F("signal_mt","signal_mt; m_{T}(lll) [GeV]; Events",nbins,bins);
        TH1F *hSignalEta = new TH1F("signal_eta","signal_eta; #eta(lll); Events",15,-2.5,2.5);
        TH1F *hSignalPhi = new TH1F("signal_phi","signal_phi; #phi(lll); Events",16,-TMath::Pi(),TMath::Pi());
        TH1F *hSignalDeltaPhi = new TH1F("signal_deltaphi","signal_deltaphi; #Delta#phi(lll,E_{T}^{Miss}); Events",16,-TMath::Pi(),TMath::Pi());
        TH1F *hSignalCharge = new TH1F("signal_charge","signal_charge; #Sigma Q; Events",7,-3.5,3.5);
        TH1F *hSignalNMuons = new TH1F("signal_nmuons","signal_nmuons; N_{#mu}; Events",4,-.5,3.5);
        TH1F *hSignalNJets = new TH1F("signal_njets","signal_njets; N_{Jet}; Events",10,-.5,9.5);
        TH1F *hSignalNBJets = new TH1F("signal_nbjets","signal_nbjets; N_{b-Jet}; Events",4,-.5,3.5);
        TH1F *hSignalMET = new TH1F("signal_met","signal_met; E_{T}^{Miss} [GeV]; Events",nbins,bins);
        TH1F *hSignalMETPhi = new TH1F("signal_metphi","signal_metphi; #phi(E_{T}^{Miss}); Events",16,-TMath::Pi(),TMath::Pi());
        TH1F *hSignalMETSumEt = new TH1F("signal_metsumet","signal_metsumet; #Sigma E_{T} [GeV]; Events",nbins,longbins);
        TH1F *hSignalMassElEl = new TH1F("signal_masselel","signal_masselel; m_{ee} [GeV]; Events",20,massBinLow,massBinHigh);
        TH1F *hSignalMassElMu = new TH1F("signal_masselmu","signal_masselmu; m_{e#mu} [GeV]; Events",20,massBinLow,massBinHigh);
        TH1F *hSignalMassMuMu = new TH1F("signal_massmumu","signal_massmumu; m_{#mu#mu} [GeV]; Events",20,massBinLow,massBinHigh);
        TH1F *hSignalMassSFOS = new TH1F("signal_masssfos","signal_masssfos; m_{SFOS} [GeV]; Events",20,massBinLow,massBinHigh);

        TH1F *hBGNSFOS = new TH1F("bg_nsfos","bg_nsfos; N_{SFOS}; Events",3,-.5,2.5);
        TH1F *hBGPt = new TH1F("bg_pt","bg_pt; p_{T}(lll) [GeV]; Events",nbins,bins);
        TH1F *hBGMt = new TH1F("bg_mt","bg_mt; m_{T}(lll) [GeV]; Events",nbins,bins);
        TH1F *hBGEta = new TH1F("bg_eta","bg_eta; #eta(lll); Events",15,-2.5,2.5);
        TH1F *hBGPhi = new TH1F("bg_phi","bg_phi; #phi(lll); Events",16,-TMath::Pi(),TMath::Pi());
        TH1F *hBGDeltaPhi = new TH1F("bg_deltaphi","bg_deltaphi; #Delta#phi(lll,E_{T}^{Miss}); Events",16,-TMath::Pi(),TMath::Pi());
        TH1F *hBGCharge = new TH1F("bg_charge","bg_charge; #Sigma Q; Events",7,-3.5,3.5);
        TH1F *hBGNMuons = new TH1F("bg_nmuons","bg_nmuons; N_{#mu}; Events",4,-.5,3.5);
        TH1F *hBGNJets = new TH1F("bg_njets","bg_njets; N_{Jet}; Events",10,-.5,9.5);
        TH1F *hBGNBJets = new TH1F("bg_nbjets","bg_nbjets; N_{b-Jet}; Events",4,-.5,3.5);
        TH1F *hBGMET = new TH1F("bg_met","bg_met; E_{T}^{Miss} [GeV]; Events",nbins,bins);
        TH1F *hBGMETPhi = new TH1F("bg_metphi","bg_metphi; #phi(E_{T}^{Miss}); Events",16,-TMath::Pi(),TMath::Pi());
        TH1F *hBGMETSumEt = new TH1F("bg_metsumet","bg_metsumet; #Sigma E_{T} [GeV]; Events",nbins,longbins);
        TH1F *hBGMassElEl = new TH1F("bg_masselel","bg_masselel; m_{ee} [GeV]; Events",20,massBinLow,massBinHigh);
        TH1F *hBGMassElMu = new TH1F("bg_masselmu","bg_masselmu; m_{e#mu} [GeV]; Events",20,massBinLow,massBinHigh);
        TH1F *hBGMassMuMu = new TH1F("bg_massmumu","bg_massmumu; m_{#mu#mu} [GeV]; Events",20,massBinLow,massBinHigh);
        TH1F *hBGMassSFOS = new TH1F("bg_masssfos","bg_masssfos; m_{SFOS} [GeV]; Events",20,massBinLow,massBinHigh);


        TH1F *hDataNSFOS = new TH1F("data_nsfos","data_nsfos; N_{SFOS}; Events",3,-.5,2.5);
        TH1F *hDataPt = new TH1F("data_pt","data_pt; p_{T}(lll) [GeV]; Events",nbins,bins);
        TH1F *hDataMt = new TH1F("data_mt","data_mt; m_{T}(lll) [GeV]; Events",nbins,bins);
        TH1F *hDataEta = new TH1F("data_eta","data_eta; #eta(lll); Events",15,-2.5,2.5);
        TH1F *hDataPhi = new TH1F("data_phi","data_phi; #phi(lll); Events",16,-TMath::Pi(),TMath::Pi());
        TH1F *hDataDeltaPhi = new TH1F("data_deltaphi","data_deltaphi; #Delta#phi(lll,E_{T}^{Miss}); Events",16,-TMath::Pi(),TMath::Pi());
        TH1F *hDataCharge = new TH1F("data_charge","data_charge; #Sigma Q; Events",7,-3.5,3.5);
        TH1F *hDataNMuons = new TH1F("data_nmuons","data_nmuons; N_{#mu}; Events",4,-.5,3.5);
        TH1F *hDataNJets = new TH1F("data_njets","data_njets; N_{Jet}; Events",10,-.5,9.5);
        TH1F *hDataNBJets = new TH1F("data_nbjets","data_nbjets; N_{b-Jet}; Events",4,-.5,3.5);
        TH1F *hDataMET = new TH1F("data_met","data_met; E_{T}^{Miss} [GeV]; Events",nbins,bins);
        TH1F *hDataMETPhi = new TH1F("data_metphi","data_metphi; #phi(E_{T}^{Miss}); Events",16,-TMath::Pi(),TMath::Pi());
        TH1F *hDataMETSumEt = new TH1F("data_metsumet","data_metsumet; #Sigma E_{T} [GeV]; Events",nbins,longbins);
        TH1F *hDataMassElEl = new TH1F("data_masselel","data_masselel; m_{ee} [GeV]; Events",20,massBinLow,massBinHigh);
        TH1F *hDataMassElMu = new TH1F("data_masselmu","data_masselmu; m_{e#mu} [GeV]; Events",20,massBinLow,massBinHigh);
        TH1F *hDataMassMuMu = new TH1F("data_massmumu","data_massmumu; m_{#mu#mu} [GeV]; Events",20,massBinLow,massBinHigh);
        TH1F *hDataMassSFOS = new TH1F("data_masssfos","data_masssfos; m_{SFOS} [GeV]; Events",20,massBinLow,massBinHigh);


        tree->Draw("nSFOS>>signal_nsfos",signalCut*weight);
	tree->Draw("lep_pt/1000.>>signal_pt",signalCut*weight);
	tree->Draw("allLep_mt/1000.>>signal_mt",signalCut*weight);
	tree->Draw("lep_eta>>signal_eta",signalCut*weight);
	tree->Draw("lep_phi>>signal_phi",signalCut*weight);
	tree->Draw("allLep_deltaPhiMET>>signal_deltaphi",signalCut*weight);
	tree->Draw("lep_charge>>signal_charge",signalCut*weight);
	tree->Draw("Sum$(lep_isMuon)>>signal_nmuons",signalCut*weight);
	tree->Draw("@jets_btagged.size()>>signal_njets",signalCut*weight);
	tree->Draw("btagEff85>>signal_nbjets",signalCut*weight);
	tree->Draw("MET_final_Et/1000.>>signal_met",signalCut*weight);
	tree->Draw("MET_final_phi>>signal_metphi",signalCut*weight);
	tree->Draw("MET_final_sumEt/1000.>>signal_metsumet",signalCut*weight);
	tree->Draw("masses_ElEl/1000.>>signal_masselel",signalCut*weight);
	tree->Draw("masses_ElMu/1000.>>signal_masselmu",signalCut*weight);
	tree->Draw("masses_MuMu/1000.>>signal_massmumu",signalCut*weight);
	tree->Draw("masses_SFOS/1000.>>signal_masssfos",signalCut*weight);

        tree->Draw("nSFOS>>bg_nsfos",bgCut*weight);
	tree->Draw("lep_pt/1000.>>bg_pt",bgCut*weight);
	tree->Draw("allLep_mt/1000.>>bg_mt",bgCut*weight);
	tree->Draw("lep_eta>>bg_eta",bgCut*weight);
	tree->Draw("lep_phi>>bg_phi",bgCut*weight);
	tree->Draw("allLep_deltaPhiMET>>bg_deltaphi",bgCut*weight);
	tree->Draw("lep_charge>>bg_charge",bgCut*weight);
	tree->Draw("Sum$(lep_isMuon)>>bg_nmuons",bgCut*weight);
	tree->Draw("@jets_btagged.size()>>bg_njets",bgCut*weight);
	tree->Draw("btagEff85>>bg_nbjets",bgCut*weight);
	tree->Draw("MET_final_Et/1000.>>bg_met",bgCut*weight);
	tree->Draw("MET_final_phi>>bg_metphi",bgCut*weight);
	tree->Draw("MET_final_sumEt/1000.>>bg_metsumet",bgCut*weight);
	tree->Draw("masses_ElEl/1000.>>bg_masselel",bgCut*weight);
	tree->Draw("masses_ElMu/1000.>>bg_masselmu",bgCut*weight);
	tree->Draw("masses_MuMu/1000.>>bg_massmumu",bgCut*weight);
	tree->Draw("masses_SFOS/1000.>>bg_masssfos",bgCut*weight);

        dataTree->Draw("nSFOS>>data_nsfos");
	dataTree->Draw("lep_pt/1000.>>data_pt");
	dataTree->Draw("allLep_mt/1000.>>data_mt");
	dataTree->Draw("lep_eta>>data_eta");
	dataTree->Draw("lep_phi>>data_phi");
	dataTree->Draw("allLep_deltaPhiMET>>data_deltaphi");
	dataTree->Draw("lep_charge>>data_charge");
	dataTree->Draw("Sum$(lep_isMuon)>>data_nmuons");
	dataTree->Draw("@jets_btagged.size()>>data_njets");
	dataTree->Draw("btagEff85>>data_nbjets");
	dataTree->Draw("MET_final_Et/1000.>>data_met");
	dataTree->Draw("MET_final_phi>>data_metphi");
	dataTree->Draw("MET_final_sumEt/1000.>>data_metsumet");
	dataTree->Draw("masses_ElEl/1000.>>data_masselel");
	dataTree->Draw("masses_ElMu/1000.>>data_masselmu");
	dataTree->Draw("masses_MuMu/1000.>>data_massmumu");
	dataTree->Draw("masses_SFOS/1000.>>data_masssfos");

        hSignalNSFOS->Write();
        hSignalPt->Write();
        hSignalMt->Write();
        hSignalEta->Write();
        hSignalPhi->Write();
        hSignalDeltaPhi->Write();
        hSignalCharge->Write();
        hSignalNMuons->Write();
        hSignalNJets->Write();
        hSignalNBJets->Write();
        hSignalMET->Write();
        hSignalMETPhi->Write();
        hSignalMETSumEt->Write();
        hSignalMassElEl->Write();
        hSignalMassElMu->Write();
        hSignalMassMuMu->Write();
        hSignalMassSFOS->Write();

        hBGNSFOS->Write();
        hBGPt->Write();
        hBGMt->Write();
        hBGEta->Write();
        hBGPhi->Write();
        hBGDeltaPhi->Write();
        hBGCharge->Write();
        hBGNMuons->Write();
        hBGNJets->Write();
        hBGNBJets->Write();
        hBGMET->Write();
        hBGMETPhi->Write();
        hBGMETSumEt->Write();
        hBGMassElEl->Write();
        hBGMassElMu->Write();
        hBGMassMuMu->Write();
        hBGMassSFOS->Write();

        hDataNSFOS->Write();
        hDataPt->Write();
        hDataMt->Write();
        hDataEta->Write();
        hDataPhi->Write();
        hDataDeltaPhi->Write();
        hDataCharge->Write();
        hDataNMuons->Write();
        hDataNJets->Write();
        hDataNBJets->Write();
        hDataMET->Write();
        hDataMETPhi->Write();
        hDataMETSumEt->Write();
        hDataMassElEl->Write();
        hDataMassElMu->Write();
        hDataMassMuMu->Write();
        hDataMassSFOS->Write();




	outFile->Close();
	

}

