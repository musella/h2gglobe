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

using namespace std;

ZMuMuGammaAnalysis::ZMuMuGammaAnalysis(){}
ZMuMuGammaAnalysis::~ZMuMuGammaAnalysis(){}

ZMuMuGammaAnalysis::TreeVariables::TreeVariables() : leadMu(0), subMu(0), photon(0)
{}

// ----------------------------------------------------------------------------------------------------
void ZMuMuGammaAnalysis::Init(LoopAll& l)
{
    l.InitTrees("zmmgAnalysis");
    l.BookExternalTreeBranch( "run",         &treevars_.run, "zmmgAnalysis" );         
    l.BookExternalTreeBranch( "event",       &treevars_.event, "zmmgAnalysis" );         
    l.BookExternalTreeBranch( "lumi",        &treevars_.lumi, "zmmgAnalysis" );         
    l.BookExternalTreeBranch( "mass",        &treevars_.mass, "zmmgAnalysis" );         
    l.BookExternalTreeBranch( "weight",      &treevars_.weight, "zmmgAnalysis" );         
    l.BookExternalTreeBranch( "nvtx",        &treevars_.nvtx, "zmmgAnalysis" );         
    l.BookExternalTreeBranch( "leadMu",      &treevars_.leadMu, "zmmgAnalysis" );         
    l.BookExternalTreeBranch( "subMu",       &treevars_.subMu, "zmmgAnalysis" );         
    l.BookExternalTreeBranch( "photon",      &treevars_.photon, "zmmgAnalysis" );         
    l.BookExternalTreeBranch( "idmva",       &treevars_.idmva, "zmmgAnalysis" );         
    l.BookExternalTreeBranch( "ciclevel",    &treevars_.ciclevel, "zmmgAnalysis" );         

    l.rooContainer->BlindData(false);
    
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
    	    if ( muonSelection (l, imu ) ) {
    		    sorted_mus.push_back(imu);
    	    }
    }

 
    if( sorted_mus.size() < 2 ) { return false; }
    //cout << " After muon selection  size " <<  sorted_mus.size() << endl;    
    //
    std::sort(sorted_mus.begin(),sorted_mus.end(),
    	      ClonesSorter<TLorentzVector,double,std::greater<double> >(l.mu_glo_p4,&TLorentzVector::Pt));
    
    int ileadMu = sorted_mus[0];
    int isubMu  = sorted_mus[1];
    if ( l.mu_glo_charge[ileadMu] * l.mu_glo_charge[isubMu] > 0 ) {return false;}
    //cout << " After muon charge selection " << endl;    

    // The case where there are more than two muons needs to be addressed
    TLorentzVector & leadMu =  *( (TLorentzVector*)l.mu_glo_p4->At(ileadMu));
    TLorentzVector & subMu  =  *( (TLorentzVector*)l.mu_glo_p4->At(isubMu) );    
    TLorentzVector diMu = leadMu + subMu;
    if ( diMu.M() < 35) {return false;}
    //    cout << " After di-muon invariant mass " << endl;    

    
    // Photon selection
    // -------------------------------------------------------------------------------------------------
    
    // First apply corrections and smearing on the single photons
    smeared_pho_energy.clear(); smeared_pho_energy.resize(l.pho_n,0.);
    smeared_pho_r9.clear();     smeared_pho_r9.resize(l.pho_n,0.);
    smeared_pho_weight.clear(); smeared_pho_weight.resize(l.pho_n,1.);
    applySinglePhotonSmearings(smeared_pho_energy, smeared_pho_r9, smeared_pho_weight, cur_type, l, energyCorrected, energyCorrectedError,
    			       phoSys, syst_shift);
    //cout << " After smearing the photons " << endl;    

        
    std::vector<int> sorted_phos;
    TClonesArray phos_p4(TLorentzVector::Class(),l.pho_n);
    for(int ipho=0; ipho<l.pho_n; ++ipho) { 
    	    TLorentzVector p4 = l.get_pho_p4( ipho, 0, &smeared_pho_energy[0]);
    	    // Fill TClonesArray with corrected 4-vectors
    	    new(phos_p4[ipho]) TLorentzVector(p4);
            int iVtx;
	    if( photonSelection ( p4 ) && l.PhotonMITPreSelection( ipho, 0 , &smeared_pho_energy[0] ) ) {
    		    sorted_phos.push_back(ipho);
    	    }
    }
    //cout << " After photon selection photon size  " <<  sorted_phos.size() << endl;    
    if( sorted_phos.size() < 1 ) { return false; }
    std::sort(sorted_phos.begin(),sorted_phos.end(),
    	      ClonesSorter<TLorentzVector,double,std::greater<double> >(&phos_p4,&TLorentzVector::Pt));
    
    int iselPho = sorted_phos[0];
    TLorentzVector & selPho =  *((TLorentzVector*)phos_p4.At(iselPho));
    if ( ! FSRselection (l, ileadMu, isubMu, iselPho, phos_p4  ) ) {return false;}
    //cout << " After FSR selection " << endl;            

    // Three body system
    // -------------------------------------------------------------------------------------------------
    //define near and far muon and select FSR
    //    int iNearMu=ileadMu;
    // int iFarMu=isubMu;
    //
    //float leadMuDPhi = l.DeltaPhi ( leadMu.Phi(), selPho.Phi() );
    // float subleadMuDPhi = l.DeltaPhi ( leadMu.Phi(), selPho.Phi() );
    //float leadMuDEta =  leadMu.Eta() -  selPho.Eta();
    //float subleadMuDEta =  subMu.Eta() -  selPho.Eta();
    //
    //float leadMuDR = sqrt(leadMuDEta*leadMuDEta + leadMuDPhi*leadMuDPhi );
    //float subleadMuDR = sqrt(subleadMuDEta*subleadMuDEta + subleadMuDPhi*subleadMuDPhi );
    //
    //if ( leadMuDR > subleadMuDR ) {
    // iNearMu = isubMu;
    // iFarMu =  ileadMu;
    // }
    //
    //float minDr = min(leadMuDR, subleadMuDR);
    // if ( minDr > 0.8) {return false;}
    // apply isolation on the muons
    //if ( l.mu_glo_chhadiso04[ileadMu]/leadMu.Pt() > 0.2 ) {return false;}
    //if ( l.mu_glo_chhadiso04[isubMu]/subMu.Pt()   > 0.2 ) {return false;}
    //
    //TLorentzVector & farMuP4 =  *( (TLorentzVector*)l.mu_glo_p4->At(iFarMu));
    //TLorentzVector mmg = diMu + selPho; 
    //if ( farMuP4.Pt() < 21) {return false;}
    //if ( mmg.M() < massMin || mmg.M() > massMax ) {return false;}
    //if ( (mmg+diMu).M() > 180 ) {return false;}
    // -----------------------------------------------------------------------------------------------------



    // define categories for plotting
    int etacat = (l.pho_isEB[iselPho]);
    int ptcat  = (selPho.Pt()>30.);
    int r9cat  = (l.pho_r9[iselPho] < 0.94);
    category = r9cat  + 2*etacat + 4*ptcat;
      
    evweight = weight * smeared_pho_weight[iselPho] * genLevWeight;
    if( ! isSyst ) {
    	    l.countersred[diPhoCounter_]++;
    }

    // fill control plots
    fillPlots(0,evweight,l,leadMu,subMu,diMu,iselPho,selPho,this->getMumugP4());
    fillPlots(1+etacat,evweight,l,leadMu,subMu,diMu,iselPho,selPho,this->getMumugP4());
    fillPlots(3+2*etacat+ptcat,evweight,l,leadMu,subMu,diMu,iselPho,selPho,this->getMumugP4());
    fillPlots(7+category,evweight,l,leadMu,subMu,diMu,iselPho,selPho,this->getMumugP4());
    //cout << " After filling the plots " << endl;    
    //return (category >= 0 && mass>=massMin && mass<=massMax);
    return (category >= 0 );
}

void ZMuMuGammaAnalysis::fillPlots(int cat, float evweight, 
				   LoopAll &l, TLorentzVector & leadMu, TLorentzVector & subMu, TLorentzVector & diMu, 
				   int iselPho, TLorentzVector & selPho, TLorentzVector & mmg)
{



  TVector3 & selSc = *((TVector3*)l.sc_xyz->At(l.pho_scind[iselPho]));
  double selScE =  l.sc_raw[l.pho_scind[iselPho]];
  //
  l.FillHist("mmg_pt"       ,cat,mmg.Pt(),evweight);
  l.FillHist("mmg_eta"      ,cat,mmg.Eta(),evweight);
  l.FillHist("mmg_phi"      ,cat,mmg.Phi(),evweight);
  l.FillHist("mmg_mass"     ,cat,mmg.M(),evweight);
  l.FillHist("nvtx"     ,cat,l.vtx_std_n,evweight);
  l.FillHist("pho_n"    ,cat,l.pho_n,evweight);
  l.FillHist("pho_e"    ,cat,selPho.E(),evweight);
  l.FillHist("pho_pt"   ,cat,selPho.Pt(),evweight);
  l.FillHist("pho_eta"  ,cat,selPho.Eta(),evweight);
  l.FillHist("pho_phi"  ,cat,selPho.Phi(),evweight);
  l.FillHist("pho_sce"  ,cat,selScE,evweight);
  l.FillHist("pho_sceta",cat,selSc.Eta(),evweight);
  l.FillHist("pho_r9"   ,cat,l.pho_r9[iselPho],evweight);
  l.FillHist("mu1_pt"   ,cat,leadMu.Pt(),evweight);
  l.FillHist("mu1_eta"  ,cat,leadMu.Eta(),evweight);
  l.FillHist("mu1_phi"  ,cat,leadMu.Phi(),evweight);
  l.FillHist("mu2_pt"   ,cat,subMu.Pt(),evweight);
  l.FillHist("mu2_eta"  ,cat,subMu.Eta(),evweight);
  l.FillHist("mu2_phi"  ,cat,subMu.Phi(),evweight);
  l.FillHist("mumu_pt"  ,cat,diMu.Pt(),evweight);
  l.FillHist("mumu_eta" ,cat,diMu.Eta(),evweight);
  l.FillHist("mumu_phi" ,cat,diMu.Phi(),evweight);
  l.FillHist("mumu_mass",cat,diMu.M(),evweight);
  
  if( cat == 0 ) { 
    treevars_.run       = l.run;
    treevars_.event     = l.event;
    treevars_.lumi      = l.lumis;
    treevars_.mass      = mmg.M();
    treevars_.weight    = evweight;
    treevars_.nvtx      = l.vtx_std_n;
    *(treevars_.leadMu) = leadMu;
    *(treevars_.subMu)  = subMu;
    *(treevars_.photon) = selPho;
    treevars_.idmva     = l.photonIDMVA(iselPho,0,selPho,bdtTrainingType.c_str());
    std::vector<std::vector<bool> > ph_passcut;
    treevars_.ciclevel  = l.PhotonCiCPFSelectionLevel(iselPho, 0, ph_passcut, 4, 0, &smeared_pho_energy[0]);
  }
}

bool ZMuMuGammaAnalysis::muonSelection(LoopAll& l, int iMu) {
  bool result=true;
  TLorentzVector * p4 = (TLorentzVector*)l.mu_glo_p4->At(iMu);

 

  //  cout << " entering Muon Selection Pt " <<  p4->Pt() << " tkLay " <<  l.mu_tkLayers[iMu] << " innerhits " << l.mu_glo_innerhits[iMu] << " Pixel " <<  l.mu_glo_pixelhits[iMu] << " valid chamb " <<  l.mu_glo_validChmbhits[iMu] << " nMatches " << l.mu_glo_nmatches[iMu] << " chi2 " <<l.mu_glo_chi2[iMu]/l.mu_glo_dof[iMu] << " d0 " <<   l.mu_glo_D0Vtx[iMu][0] << " dz " << l.mu_glo_DZVtx[iMu][0] << " gsf " << l.mu_glo_hasgsftrack[iMu] << endl;
  //cout << " cut values " << muPtMin << " " << muTkLayers << " " << muPixelHits << " " << muValidChambers << " " << muNmatches << " " << muNormChi2 << " " << muD0Vtx << " " << muDZVtx << endl;

  if ( p4->Pt() <  muPtMin )                                     result=false;  
  if ( l.mu_tkLayers[iMu] <= muTkLayers  )                       result=false;
  // if ( !l.mu_glo_innerhits[iMu]     )                            result=false;
  if ( l.mu_glo_pixelhits[iMu] < muPixelHits )                   result=false;
  if ( l.mu_glo_validChmbhits[iMu] < muValidChambers )           result=false;
  if ( l.mu_glo_nmatches[iMu] <= muNmatches  )                   result=false;
  if ( l.mu_glo_chi2[iMu]/l.mu_glo_dof[iMu] >= muNormChi2  )     result=false;
  if ( l.mu_glo_D0Vtx[iMu][0] > muD0Vtx )                        result=false;
  if ( l.mu_glo_DZVtx[iMu][0] > muDZVtx )                        result=false;
  if ( l.mu_glo_hasgsftrack[iMu] )                               result=false;

  //cout << " ending Muon Selection result " << result <<  endl;

  return result;

}


bool ZMuMuGammaAnalysis::photonSelection (TLorentzVector& p4) {
  bool result=true;
  if ( fabs(p4.Eta())  > 2.5 )                               result=false;
  if ( fabs(p4.Eta()) > 1.4442 &&  fabs(p4.Eta())  < 1.566 ) result=false;
  if ( p4.Pt() < 10)                                         result=false;

  return result;

}

bool ZMuMuGammaAnalysis::FSRselection ( LoopAll& l, int ileadMu, int isubMu, int iPho, TClonesArray& phos_p4 ) {

  bool result=true;

  int iNearMu=ileadMu;
  int iFarMu=isubMu;
  //
  TLorentzVector & leadMu =  *( (TLorentzVector*)l.mu_glo_p4->At(ileadMu));
  TLorentzVector & subMu  =  *( (TLorentzVector*)l.mu_glo_p4->At(isubMu) );    
  TLorentzVector & selPho =  *((TLorentzVector*)phos_p4.At(iPho));
  //
  float leadMuDPhi = l.DeltaPhi ( leadMu.Phi(), selPho.Phi() );
  float subleadMuDPhi = l.DeltaPhi ( leadMu.Phi(), selPho.Phi() );
  float leadMuDEta =  leadMu.Eta() -  selPho.Eta();
  float subleadMuDEta =  subMu.Eta() -  selPho.Eta();
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
  if ( minDr > 0.8) result=false;
  // apply isolation on the muons
  if ( l.mu_glo_chhadiso04[ileadMu]/leadMu.Pt() > 0.2 ) result=false;
  if ( l.mu_glo_chhadiso04[isubMu]/subMu.Pt()   > 0.2 ) result=false;
  //
  TLorentzVector & farMuP4 =  *( (TLorentzVector*)l.mu_glo_p4->At(iFarMu));

  TLorentzVector diMu = leadMu + subMu;
  mumugMass_ = diMu + selPho; 


  if ( farMuP4.Pt() < 21) result=false;
  if ( mumugMass_.M() < massMin || mumugMass_.M() > massMax ) result=false;
  if ( (mumugMass_+diMu).M() > 180 ) result=false;

  return result;

}
