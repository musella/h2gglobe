#ifndef __JETENERGYSMEARER__
#define __JETENERGYSMEARER__

#include "BaseSmearer.h"
#include <string>
#include <map>
#include <utility>
#include "TFile.h"
#include "TRandom3.h"
#include "TGraphAsymmErrors.h"

class LoopAll;
class PhotonReducedInfo;
class TRandom3;
class JetHandler;

// ------------------------------------------------------------------------------------
class JetEnergySmearer : public BaseSmearer
{
public:

	JetEnergySmearer(LoopAll * lo, JetHandler * jh, bool reInitializeJets);
	virtual ~JetEnergySmearer();
  
	virtual const std::string & name() const { return name_; };
  
	virtual bool smearPhoton(PhotonReducedInfo &, float & weight, int run, float syst_shift) const;
	
	void name(const std::string & x) { name_ = x; };

	virtual void newEvent(LoopAll * l);

	void jerOrJec(bool x) { jerOrJec_ = x; }
	
protected:
	std::string name_;
	LoopAll * l_;
	JetHandler * jetHandler_;
	bool reInitializeJets_;
	TClonesArray * jetP4s_;
	bool jerOrJec_;
	
};


#endif
