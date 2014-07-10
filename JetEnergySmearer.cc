#include "JetEnergySmearer.h"
#include "PhotonReducedInfo.h"
#include "LoopAll.h"
#include "branchdef/Limits.h"
#include "JetAnalysis/interface/JetHandler.h"


JetEnergySmearer::JetEnergySmearer(LoopAll * lo, JetHandler * jh, bool reInitializeJets) :
	l_(lo), jetHandler_(jh), reInitializeJets_(reInitializeJets), jetP4s_( reInitializeJets_ ? new TClonesArray("TLorentzVector",MAX_JETS) : 0 ), 
	jerOrJec_(false)
{
}

JetEnergySmearer::~JetEnergySmearer()
{
	
}

void JetEnergySmearer::newEvent(LoopAll * l)
{
	if( reInitializeJets_ ) {
		jetP4s_->Clear();
		for(int ijet=0; ijet<l_->jet_algoPF1_n; ++ijet) {
			TLorentzVector *p4 = (TLorentzVector*)jetP4s_->ConstructedAt(ijet);
			*p4 = *( (TLorentzVector*)l_->jet_algoPF1_p4->At(ijet) );
		}

	}
}

bool JetEnergySmearer::smearPhoton(PhotonReducedInfo &info, float & weight, int run, float syst_shift) const
{
	int ipho = info.iPho();
	
	if( ipho != 0 ) { return true; }
	if( syst_shift == 0. ) { 
		if( reInitializeJets_ ) {
			for(int ijet=0; ijet<l_->jet_algoPF1_n; ++ijet) {
				TLorentzVector *p4 = (TLorentzVector*)l_->jet_algoPF1_p4->At(ijet);
				*p4 = *( (TLorentzVector*) jetP4s_->At(ijet));
			}
		}
		return true; 
	}

	for(int ijet=0; ijet<l_->jet_algoPF1_n; ++ijet) {
		
		if( jerOrJec_ ) {
			jetHandler_->applyJecUncertainty(ijet, syst_shift);
		} else {
			jetHandler_->applyJerUncertainty(ijet, syst_shift);
		}
	}
	
	return true;
}
