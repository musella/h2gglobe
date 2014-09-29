#include "../interface/ZMuMuGammaAnalysis.h"

#include "PhotonReducedInfo.h"
#include "Sorters.h"
#include <iostream>
#include <iomanip>
#include <fstream>
#include <algorithm>

#include "JetAnalysis/interface/JetHandler.h"
#include "CMGTools/External/interface/PileupJetIdentifier.h"

#define PADEBUG 0

#define ZMASS 91.2

using namespace std;

ZMuMuGammaAnalysis::ZMuMuGammaAnalysis()
{
	muTkLayers 	= 5;
	muPixelHits 	= 0;
	muValidChambers = 0;
	muNmatches 	= 1;
	muNormChi2 	= 10.;
	muD0Vtx 	= 0.2;
	muDZVtx 	= 0.5;
	phoPtMin 	= 20.;
	dEtaMin 	= 0.;
	dRMin 		= 0.05;
	dRMax 		= 0.8;
	muIsoMax 	= 0.2;
	leadMuPtMin 	= 25.;
	subMuPtMin 	= 10.5;
	diMuMassMin 	= 35.;
	farMuPtMin 	= 21.;
	massSumMax 	= 180.;
	applyPhoPresel 	= false;
	doFsr           = true;
	useSvariable    = false;
}

ZMuMuGammaAnalysis::~ZMuMuGammaAnalysis(){}

ZMuMuGammaAnalysis::TreeVariables::TreeVariables() : leadMu(0), subMu(0), photon(0), mm(0), mmg(0)
{}

// ----------------------------------------------------------------------------------------------------
void ZMuMuGammaAnalysis::Init(LoopAll& l)
{
    l.InitTrees("zmmgAnalysis");
    l.BookExternalTreeBranch( "run",         &treevars_.run, "zmmgAnalysis" );         
    l.BookExternalTreeBranch( "event",       &treevars_.event, "zmmgAnalysis" );         
    l.BookExternalTreeBranch( "lumi",        &treevars_.lumi, "zmmgAnalysis" );         
    l.BookExternalTreeBranch( "mass",        &treevars_.mass, "zmmgAnalysis" );         
    l.BookExternalTreeBranch( "category",    &treevars_.category, "zmmgAnalysis" );
    l.BookExternalTreeBranch( "weight",      &treevars_.weight, "zmmgAnalysis" );         
    l.BookExternalTreeBranch( "nvtx",        &treevars_.nvtx, "zmmgAnalysis" );         
    l.BookExternalTreeBranch( "leadMu",      &treevars_.leadMu, "zmmgAnalysis" );         
    l.BookExternalTreeBranch( "subMu",       &treevars_.subMu, "zmmgAnalysis" );         
    l.BookExternalTreeBranch( "photon",      &treevars_.photon, "zmmgAnalysis" );         
    l.BookExternalTreeBranch( "mm",          &treevars_.mm, "zmmgAnalysis" );         
    l.BookExternalTreeBranch( "mmg",         &treevars_.mmg, "zmmgAnalysis" );         
    l.BookExternalTreeBranch( "idmva",       &treevars_.idmva, "zmmgAnalysis" );         
    l.BookExternalTreeBranch( "ciclevel",    &treevars_.ciclevel, "zmmgAnalysis" );         
    // store photon ID MVA inputs
    l.BookExternalTreeBranch( "r9",          &l.tmva_photonid_r9, "zmmgAnalysis" );         
    l.BookExternalTreeBranch("sigietaieta",  &l.tmva_photonid_sieie, "zmmgAnalysis" );
    l.BookExternalTreeBranch("scetawidth",   &l.tmva_photonid_etawidth, "zmmgAnalysis" );
    l.BookExternalTreeBranch("scphiwidth",   &l.tmva_photonid_phiwidth, "zmmgAnalysis" );
    l.BookExternalTreeBranch("idmva_CoviEtaiPhi",   &l.tmva_photonid_sieip, "zmmgAnalysis" );
    l.BookExternalTreeBranch("idmva_s4ratio",   &l.tmva_photonid_s4ratio, "zmmgAnalysis" );
    l.BookExternalTreeBranch("idmva_GammaIso",   &l.tmva_photonid_pfphotoniso03, "zmmgAnalysis" );
    l.BookExternalTreeBranch("idmva_ChargedIso_selvtx",   &l.tmva_photonid_pfchargedisogood03, "zmmgAnalysis" );
    l.BookExternalTreeBranch("idmva_ChargedIso_worstvtx",   &l.tmva_photonid_pfchargedisobad03, "zmmgAnalysis" );
    l.BookExternalTreeBranch("sceta",   &l.tmva_photonid_sceta, "zmmgAnalysis" );
    l.BookExternalTreeBranch("rho",   &l.tmva_photonid_eventrho, "zmmgAnalysis" );
    
    l.rooContainer->BlindData(false);
    l.rooContainer->SaveSystematicsData(true);
    
    // initialize Hgg machinery, forcing     
    StatAnalysis::Init(l);

    // book photon ID MVA
    l.SetAllMVA();
    if( photonLevel2013IDMVA_EB != "" && photonLevel2013IDMVA_EE != "" ) {
	l.tmvaReaderID_2013_Barrel->BookMVA("AdaBoost",photonLevel2013IDMVA_EB.c_str());
	l.tmvaReaderID_2013_Endcap->BookMVA("AdaBoost",photonLevel2013IDMVA_EE.c_str());
    } else if( photonLevel2012IDMVA_EB != "" && photonLevel2012IDMVA_EE != "" ) {
    	l.tmvaReaderID_Single_Barrel->BookMVA("AdaBoost",photonLevel2012IDMVA_EB.c_str());
    	l.tmvaReaderID_Single_Endcap->BookMVA("AdaBoost",photonLevel2012IDMVA_EE.c_str());
	assert( bdtTrainingType == "Moriond2013" ); 
    } else if (photonLevel2013_7TeV_IDMVA_EB != "" && photonLevel2013_7TeV_IDMVA_EE != "" ) {
    	l.tmvaReaderID_2013_7TeV_MIT_Barrel->BookMVA("AdaBoost",photonLevel2013_7TeV_IDMVA_EB.c_str());
    	l.tmvaReaderID_2013_7TeV_MIT_Endcap->BookMVA("AdaBoost",photonLevel2013_7TeV_IDMVA_EE.c_str());
    } else { 
    	assert( run7TeV4Xanalysis );
    }

    // replace trigger selection
    triggerSelections.clear();
    triggerSelections.push_back(TriggerSelection(1,-1));
    triggerSelections.back().addpath("HLT_Mu17_TkMu8");
    triggerOnMc = true;

    l.SetSubJob(true);
}

// ----------------------------------------------------------------------------------------------------
bool ZMuMuGammaAnalysis::AnalyseEvent(LoopAll& l, Int_t jentry, float weight, TLorentzVector & gP4,
        float & mass, float & evweight, int & category, int & diphoton_id, bool & isCorrectVertex,
        float &kinematic_bdtout,
        bool isSyst,
        float syst_shift, bool skipSelection,
        BaseGenLevelSmearer *genSys, BaseSmearer *phoSys, BaseDiPhotonSmearer * diPhoSys)
{
    assert( ! skipSelection );


    int cur_type = l.itype[l.current];
    float sampleweight = l.sampleContainer[l.current_sample_index].weight();
    
    // do gen-level dependent first (e.g. k-factor); only for signal
    genLevWeight=1.;
    
    // event selection
    int leadpho_ind=-1;
    int subleadpho_ind=-1;
    
    // Muon selection
    // -------------------------------------------------------------------------------------------------
    std::vector<int> sorted_mus;
    for(int imu=0; imu<l.mu_glo_n; ++imu) { 
    	    TLorentzVector * p4 = (TLorentzVector*)l.mu_glo_p4->At(imu);
	    //    	    bool passSelection = true;
    	    if ( muonSelection(l, imu ) ) {
    		    sorted_mus.push_back(imu);
    	    }
    }
    
    if( sorted_mus.size() < 2 ) { return false; }
    std::sort(sorted_mus.begin(),sorted_mus.end(),
    	      ClonesSorter<TLorentzVector,double,std::greater<double> >(l.mu_glo_p4,&TLorentzVector::Pt));
    
    int ileadMu = sorted_mus[0];
    int isubMu  = sorted_mus[1];
    if ( l.mu_glo_charge[ileadMu] * l.mu_glo_charge[isubMu] > 0 ) {return false;}

    // If more than two muons pass the ID criteria we look at the two highest pT ones
    //    Fully combinatorial selection would need to be implemented
    TLorentzVector & leadMu =  *( (TLorentzVector*)l.mu_glo_p4->At(ileadMu));
    TLorentzVector & subMu  =  *( (TLorentzVector*)l.mu_glo_p4->At(isubMu) );    
    TLorentzVector diMu = leadMu + subMu;
    if (leadMu.Pt() < leadMuPtMin ){ return false; }
    if ( diMu.M() < diMuMassMin )  { return false; }
    
    // Run simple Z->mumu analysis
    if( ! doFsr ) {
	    mass = diMu.M();
	    evweight = weight * genLevWeight;
	    float maxeta = std::max(fabs(leadMu.Eta()),fabs(subMu.Eta()));
	    category = (maxeta > 0.9) + (maxeta > 1.5);
	    TLorentzVector null(0.,0.,0.,0.);
	    fillPlots(0,evweight,l,leadMu,subMu,diMu,-1,null,null);
	    fillPlots(category+1,evweight,l,leadMu,subMu,diMu,-1,null,null);
	    return ( mass >= massMin && mass <= massMax );
    }
    
    // Photon selection
    // -------------------------------------------------------------------------------------------------
    
    // First apply corrections and smearing on the single photons
    smeared_pho_energy.clear(); smeared_pho_energy.resize(l.pho_n,0.);
    smeared_pho_r9.clear();     smeared_pho_r9.resize(l.pho_n,0.);
    smeared_pho_weight.clear(); smeared_pho_weight.resize(l.pho_n,1.);
    applySinglePhotonSmearings(smeared_pho_energy, smeared_pho_r9, smeared_pho_weight, cur_type, l, energyCorrected, energyCorrectedError,
    			       phoSys, syst_shift);
    
    std::vector<int> sorted_phos;
    std::vector<float> pho_minDr;
    TClonesArray phos_p4(TLorentzVector::Class(),l.pho_n);
    for(int ipho=0; ipho<l.pho_n; ++ipho) { 
    	    TLorentzVector p4 = l.get_pho_p4( ipho, 0, &smeared_pho_energy[0]);
    	    // Fill TClonesArray with corrected 4-vectors
    	    new(phos_p4[ipho]) TLorentzVector(p4);
	    TVector3 & sc = *((TVector3*)l.sc_xyz->At(l.pho_scind[ipho]));
	    
	    pho_minDr.push_back( min(p4.DeltaR(leadMu), p4.DeltaR(subMu)) );
	    if ( photonSelection( p4, sc ) && 
		 ( applyPhoPresel || l.PhotonMITPreSelection( ipho, 0 , &smeared_pho_energy[0] ) ) &&
		 FSRselection (l, ileadMu, isubMu, ipho, phos_p4  )
		    )  {
    		    sorted_phos.push_back(ipho);
    	    }
    }

    if( sorted_phos.size() < 1 ) { return false; }
    std::sort(sorted_phos.begin(),sorted_phos.end(),SimpleSorter<float>(&pho_minDr[0]) );
    //// std::sort(sorted_phos.begin(),sorted_phos.end(),
    //// 	      ClonesSorter<TLorentzVector,double,std::greater<double> >(&phos_p4,&TLorentzVector::Pt));
    
    int iselPho = sorted_phos[0];
    TLorentzVector & selPho =  *((TLorentzVector*)phos_p4.At(iselPho));
    /// if ( ! FSRselection (l, ileadMu, isubMu, iselPho, phos_p4  ) ) {return false;}
    /// // Apply photon pre-selection a la Hgg
    /// if ( applyPhoPresel && ! l.PhotonMITPreSelection( iselPho, 0 , &smeared_pho_energy[0] ) ) {return false;}

    mass = this->getMumugP4().M();
    if( useSvariable ) {
	    mass = ( mass*mass - diMu.M() * diMu.M() ) / (ZMASS*ZMASS - diMu.M() * diMu.M());
    }
    if( mass<massMin || mass>massMax ) { return false; }
    
    // assign event to categories
    int etacat = (!l.pho_isEB[iselPho]);
    int ptcat  = (selPho.Pt()<25.)+(selPho.Pt()<40.);
    int r9cat  = (l.pho_r9[iselPho] < 0.94);
    category = r9cat  + 2*etacat + 4*ptcat;
    evweight = weight * smeared_pho_weight[iselPho] * genLevWeight;
    if( ! isSyst ) {
    	    l.countersred[diPhoCounter_]++;

	    // fill control plots
	    fillPlots(0,evweight,l,leadMu,subMu,diMu,iselPho,selPho,this->getMumugP4());
	    fillPlots(1+etacat,evweight,l,leadMu,subMu,diMu,iselPho,selPho,this->getMumugP4());
	    fillPlots(3+2*etacat+ptcat,evweight,l,leadMu,subMu,diMu,iselPho,selPho,this->getMumugP4());
	    fillPlots(7+category,evweight,l,leadMu,subMu,diMu,iselPho,selPho,this->getMumugP4());
	    //cout << " After filling the plots " << endl;    
	    //return (category >= 0 && mass>=massMin && mass<=massMax);
    }
    
    treevars_.category = category;
    return (category >= 0 );
}

void ZMuMuGammaAnalysis::fillPlots(int cat, float evweight, 
				   LoopAll &l, TLorentzVector & leadMu, TLorentzVector & subMu, TLorentzVector & diMu, 
				   int iselPho, TLorentzVector & selPho, TLorentzVector & mmg)
{



  TVector3 & selSc = *((TVector3*)l.sc_xyz->At(l.pho_scind[iselPho]));
  double selScE =  iselPho >= 0 ? l.sc_raw[l.pho_scind[iselPho]] : 0.;
  double r9     = iselPho >= 0 ? l.pho_r9[iselPho] : 0.;
  //
  l.FillHist("mmg_pt"       	,cat,mmg.Pt(),evweight);
  l.FillHist("mmg_eta"      	,cat,mmg.Eta(),evweight);
  l.FillHist("mmg_phi"      	,cat,mmg.Phi(),evweight);
  l.FillHist("mmg_mass"     	,cat,mmg.M(),evweight);
  l.FillHist("nvtx"     	,cat,l.vtx_std_n,evweight);
  l.FillHist("pho_n"    	,cat,l.pho_n,evweight);
  l.FillHist("pho_e"    	,cat,selPho.E(),evweight);
  l.FillHist("pho_pt"   	,cat,selPho.Pt(),evweight);
  l.FillHist("pho_eta"  	,cat,selPho.Eta(),evweight);
  l.FillHist("pho_phi"  	,cat,selPho.Phi(),evweight);
  l.FillHist("pho_sce"  	,cat,selScE,evweight);
  l.FillHist("pho_sceta"	,cat,selSc.Eta(),evweight);
  l.FillHist("pho_r9"   	,cat,r9,evweight);
  l.FillHist("mu1_pt"   	,cat,leadMu.Pt(),evweight);
  l.FillHist("mu1_eta"  	,cat,leadMu.Eta(),evweight);
  l.FillHist("mu1_phi"  	,cat,leadMu.Phi(),evweight);
  l.FillHist("mu2_pt"   	,cat,subMu.Pt(),evweight);
  l.FillHist("mu2_eta"  	,cat,subMu.Eta(),evweight);
  l.FillHist("mu2_phi"  	,cat,subMu.Phi(),evweight);
  l.FillHist("mumu_pt"  	,cat,diMu.Pt(),evweight);
  l.FillHist("mumu_eta" 	,cat,diMu.Eta(),evweight);
  l.FillHist("mumu_phi" 	,cat,diMu.Phi(),evweight);
  l.FillHist("mumu_mass"	,cat,diMu.M(),evweight);
  
  if( cat == 0 ) { 
	  fillTree(evweight, l, leadMu, subMu, diMu, iselPho, selPho, mmg);
  }
}

void ZMuMuGammaAnalysis::fillTree(float evweight, 
				  LoopAll &l, TLorentzVector & leadMu, TLorentzVector & subMu, TLorentzVector & diMu, 
				  int iselPho, TLorentzVector & selPho, TLorentzVector & mmg)
{
    treevars_.run       = l.run;
    treevars_.event     = l.event;
    treevars_.lumi      = l.lumis;
    treevars_.mass      = ( iselPho >= 0 ? mmg.M() : diMu.M() );
    treevars_.weight    = evweight;
    treevars_.nvtx      = l.vtx_std_n;
    *(treevars_.leadMu) = leadMu;
    *(treevars_.subMu)  = subMu;
    *(treevars_.mm)     = diMu;
    *(treevars_.photon) = selPho;
    *(treevars_.mmg)    = mmg;
    if( iselPho >= 0 ) {
	    treevars_.idmva     = l.photonIDMVA(iselPho,0,selPho,bdtTrainingType.c_str()); // this also sets all the l.tmva_* variables
	    std::vector<std::vector<bool> > ph_passcut;
	    treevars_.ciclevel  = l.PhotonCiCPFSelectionLevel(iselPho, 0, ph_passcut, 4, 0, &smeared_pho_energy[0]);
    } else {
	    treevars_.idmva     		= -2.;
	    l.tmva_photonid_r9 			= 0.;         
	    l.tmva_photonid_sieie 		= 0.;
	    l.tmva_photonid_etawidth 		= 0.;
	    l.tmva_photonid_phiwidth 		= 0.;
	    l.tmva_photonid_sieip 		= 0.;
	    l.tmva_photonid_s4ratio 		= 0.;
	    l.tmva_photonid_pfphotoniso03 	= 0.;
	    l.tmva_photonid_pfchargedisogood03 	= 0.;
	    l.tmva_photonid_pfchargedisobad03 	= 0.;
	    l.tmva_photonid_sceta 		= 0.;
	    l.tmva_photonid_eventrho 		= l.rho_algo1;
	    treevars_.ciclevel  		= -1;
    }
}

bool ZMuMuGammaAnalysis::muonSelection(LoopAll& l, int iMu) {
  bool result=true;
  TLorentzVector * p4 = (TLorentzVector*)l.mu_glo_p4->At(iMu);
  
  //  cout << " entering Muon Selection Pt " <<  p4->Pt() << " tkLay " <<  l.mu_tkLayers[iMu] << " innerhits " << l.mu_glo_innerhits[iMu] << " Pixel " <<  l.mu_glo_pixelhits[iMu] << " valid chamb " <<  l.mu_glo_validChmbhits[iMu] << " nMatches " << l.mu_glo_nmatches[iMu] << " chi2 " <<l.mu_glo_chi2[iMu]/l.mu_glo_dof[iMu] << " d0 " <<   l.mu_glo_D0Vtx[iMu][0] << " dz " << l.mu_glo_DZVtx[iMu][0] << " gsf " << l.mu_glo_hasgsftrack[iMu] << endl;
  //cout << " cut values " << muPtMin << " " << muTkLayers << " " << muPixelHits << " " << muValidChambers << " " << muNmatches << " " << muNormChi2 << " " << muD0Vtx << " " << muDZVtx << endl;

  if ( ( p4->Pt() <  subMuPtMin )                                  ||  
       ( l.mu_tkLayers[iMu] <= muTkLayers  )                       ||
       ( l.mu_glo_pixelhits[iMu] <= muPixelHits )                  ||
       ( l.mu_glo_validChmbhits[iMu] <= muValidChambers )          ||
       ( l.mu_glo_nmatches[iMu] <= muNmatches  )                   ||
       ( l.mu_glo_chi2[iMu]/l.mu_glo_dof[iMu] >= muNormChi2  )     ||
       ( l.mu_glo_D0Vtx[iMu][0] >= muD0Vtx )                       ||
       ( l.mu_glo_DZVtx[iMu][0] >= muDZVtx )                       ||
       ( l.mu_glo_hasgsftrack[iMu] )                               
	  ) { result=false; }
  
  //cout << " ending Muon Selection result " << result <<  endl;

  return result;

}


bool ZMuMuGammaAnalysis::photonSelection (TLorentzVector& p4, TVector3 & sc ) {
  bool result=true;
  if ( fabs(sc.Eta())  > 2.5 )                               result=false;
  if ( fabs(sc.Eta()) > 1.4442 &&  fabs(sc.Eta())  < 1.566 ) result=false;
  if ( p4.Pt() < phoPtMin)                                   result=false;
  
  return result;

}

bool ZMuMuGammaAnalysis::FSRselection ( LoopAll& l, int ileadMu, int isubMu, int iPho, TClonesArray& phos_p4 ) {

  int iNearMu=ileadMu;
  int iFarMu=isubMu;
  //
  TLorentzVector & leadMu =  *( (TLorentzVector*)l.mu_glo_p4->At(ileadMu));
  TLorentzVector & subMu  =  *( (TLorentzVector*)l.mu_glo_p4->At(isubMu) );    
  TLorentzVector & selPho =  *((TLorentzVector*)phos_p4.At(iPho));
  TLorentzVector diMu = leadMu + subMu;
  
  //
  float leadMuDPhi = leadMu.DeltaPhi(selPho);
  float subleadMuDPhi = subMu.DeltaPhi(selPho);
  float leadMuDEta =  fabs(leadMu.Eta() - selPho.Eta());
  float subleadMuDEta =  fabs(subMu.Eta() - selPho.Eta());
  //
  float leadMuDR = sqrt(leadMuDEta*leadMuDEta + leadMuDPhi*leadMuDPhi );
  float subleadMuDR = sqrt(subleadMuDEta*subleadMuDEta + subleadMuDPhi*subleadMuDPhi );
  //
  if ( leadMuDR > subleadMuDR ) {
    iNearMu = isubMu;
    iFarMu =  ileadMu;
  }
  //
  float minDr = min(leadMuDR, subleadMuDR);
  if ( minDr > dRMax || minDr < dRMin ) { return false; };
  float minDeta = min(leadMuDEta, subleadMuDEta);
  if ( minDeta < dEtaMin ) { return false; };
  // apply isolation on the muons
  if ( l.mu_glo_chhadiso04[ileadMu]/leadMu.Pt() > muIsoMax ) { return false; };
  if ( l.mu_glo_chhadiso04[isubMu]/subMu.Pt()   > muIsoMax ) { return false; };
  //
  TLorentzVector & farMuP4 =  *( (TLorentzVector*)l.mu_glo_p4->At(iFarMu));

  mumugMass_ = diMu + selPho; 
    
  if ( farMuP4.Pt() < farMuPtMin ) { return false; };
  /// if ( mumugMass_.M() < massMin || mumugMass_.M() > massMax ) { return false; };
  if ( mumugMass_.M()+diMu.M() > massSumMax ) { return false; };
  
  return true;

}
