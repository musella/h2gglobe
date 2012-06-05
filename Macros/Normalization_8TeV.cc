#include "Normalization_8TeV.h"

Normalization_8TeV::Normalization_8TeV(){
  BranchingRatioMap[90]=0.00123;
  BranchingRatioMap[95]=0.0014;
  BranchingRatioMap[100]=0.00159;
  BranchingRatioMap[105]=0.00178;
  BranchingRatioMap[110]=0.00197;
  BranchingRatioMap[110.5]=0.00199;
  BranchingRatioMap[111]=0.002;
  BranchingRatioMap[111.5]=0.00202;
  BranchingRatioMap[112]=0.00204;
  BranchingRatioMap[112.5]=0.00205;
  BranchingRatioMap[113]=0.00207;
  BranchingRatioMap[113.5]=0.00209;
  BranchingRatioMap[114]=0.0021;
  BranchingRatioMap[114.5]=0.00212;
  BranchingRatioMap[115]=0.00213;
  BranchingRatioMap[115.5]=0.00215;
  BranchingRatioMap[116]=0.00216;
  BranchingRatioMap[116.5]=0.00217;
  BranchingRatioMap[117]=0.00218;
  BranchingRatioMap[117.5]=0.0022;
  BranchingRatioMap[118]=0.00221;
  BranchingRatioMap[118.5]=0.00222;
  BranchingRatioMap[119]=0.00223;
  BranchingRatioMap[119.5]=0.00224;
  BranchingRatioMap[120]=0.00225;
  BranchingRatioMap[120.5]=0.00226;
  BranchingRatioMap[121]=0.00226;
  BranchingRatioMap[121.5]=0.00227;
  BranchingRatioMap[122]=0.00228;
  BranchingRatioMap[122.5]=0.00228;
  BranchingRatioMap[123]=0.00228;
  BranchingRatioMap[123.5]=0.00229;
  BranchingRatioMap[124]=0.00229;
  BranchingRatioMap[124.5]=0.00229;
  BranchingRatioMap[125]=0.00229;
  BranchingRatioMap[125.5]=0.00229;
  BranchingRatioMap[126]=0.00229;
  BranchingRatioMap[126.5]=0.00229;
  BranchingRatioMap[127]=0.00229;
  BranchingRatioMap[127.5]=0.00229;
  BranchingRatioMap[128]=0.00228;
  BranchingRatioMap[128.5]=0.00228;
  BranchingRatioMap[129]=0.00227;
  BranchingRatioMap[129.5]=0.00227;
  BranchingRatioMap[130]=0.00226;
  BranchingRatioMap[130.5]=0.00225;
  BranchingRatioMap[131]=0.00224;
  BranchingRatioMap[131.5]=0.00223;
  BranchingRatioMap[132]=0.00222;
  BranchingRatioMap[132.5]=0.00221;
  BranchingRatioMap[133]=0.00219;
  BranchingRatioMap[133.5]=0.00218;
  BranchingRatioMap[134]=0.00217;
  BranchingRatioMap[134.5]=0.00215;
  BranchingRatioMap[135]=0.00213;
  BranchingRatioMap[135.5]=0.00212;
  BranchingRatioMap[136]=0.0021;
  BranchingRatioMap[136.5]=0.00208;
  BranchingRatioMap[137]=0.00206;
  BranchingRatioMap[137.5]=0.00204;
  BranchingRatioMap[138]=0.00202;
  BranchingRatioMap[138.5]=0.002;
  BranchingRatioMap[139]=0.00198;
  BranchingRatioMap[139.5]=0.00196;
  BranchingRatioMap[140]=0.00193;
  BranchingRatioMap[141]=0.00189;
  BranchingRatioMap[142]=0.00184;
  BranchingRatioMap[143]=0.00178;
  BranchingRatioMap[144]=0.00173;
  BranchingRatioMap[145]=0.00167;
  BranchingRatioMap[146]=0.00162;
  BranchingRatioMap[147]=0.00156;
  BranchingRatioMap[148]=0.00149;
  BranchingRatioMap[149]=0.00143;
  BranchingRatioMap[150]=0.00136;
  BranchingRatioMap[151]=0.0013;
  BranchingRatioMap[152]=0.00123;
  BranchingRatioMap[153]=0.00115;
  BranchingRatioMap[154]=0.00108;
  BranchingRatioMap[155]=0.000999;
  BranchingRatioMap[156]=0.000914;
  BranchingRatioMap[157]=0.000825;
  BranchingRatioMap[158]=0.000729;
  BranchingRatioMap[159]=0.000628;
  BranchingRatioMap[160]=0.000532;
  BranchingRatioMap[162]=0.00037;
  BranchingRatioMap[164]=0.000259;
  BranchingRatioMap[166]=0.000208;
  BranchingRatioMap[168]=0.000178;
  BranchingRatioMap[170]=0.000158;
  BranchingRatioMap[172]=0.000143;
  BranchingRatioMap[174]=0.000132;
  BranchingRatioMap[176]=0.000122;
  BranchingRatioMap[178]=0.000113;
  BranchingRatioMap[180]=0.000105;
  BranchingRatioMap[182]=0.0000968;
  BranchingRatioMap[184]=0.0000881;
  BranchingRatioMap[186]=0.0000809;
  BranchingRatioMap[188]=0.0000752;
  BranchingRatioMap[190]=0.0000705;
  BranchingRatioMap[192]=0.0000666;
  BranchingRatioMap[194]=0.0000632;
  BranchingRatioMap[196]=0.0000602;
  BranchingRatioMap[198]=0.0000575;
  BranchingRatioMap[200]=0.0000551;
  BranchingRatioMap[202]=0.0000529;
  BranchingRatioMap[204]=0.0000508;
  BranchingRatioMap[206]=0.0000489;
  BranchingRatioMap[208]=0.0000471;
  BranchingRatioMap[210]=0.0000454;
  BranchingRatioMap[212]=0.0000439;
  BranchingRatioMap[214]=0.0000424;
  BranchingRatioMap[216]=0.000041;
  BranchingRatioMap[218]=0.0000396;
  BranchingRatioMap[220]=0.0000384;
  BranchingRatioMap[222]=0.0000372;
  BranchingRatioMap[224]=0.000036;
  BranchingRatioMap[226]=0.0000349;
  BranchingRatioMap[228]=0.0000339;
  BranchingRatioMap[230]=0.0000328;
  BranchingRatioMap[232]=0.0000319;
  BranchingRatioMap[234]=0.0000309;
  BranchingRatioMap[236]=0.0000301;
  BranchingRatioMap[238]=0.0000292;
  BranchingRatioMap[240]=0.0000284;
  BranchingRatioMap[242]=0.0000276;
  BranchingRatioMap[244]=0.0000268;
  BranchingRatioMap[246]=0.0000261;
  BranchingRatioMap[248]=0.0000254;
  BranchingRatioMap[250]=0.0000247;

  //GGH X-Sections
  XSectionMap_ggh[80]=46.0593;
  XSectionMap_ggh[81]=44.9777;
  XSectionMap_ggh[82]=43.9344;
  XSectionMap_ggh[83]=42.928;
  XSectionMap_ggh[84]=41.9566;
  XSectionMap_ggh[85]=41.0179;
  XSectionMap_ggh[86]=40.1112;
  XSectionMap_ggh[87]=39.2347;
  XSectionMap_ggh[88]=38.3868;
  XSectionMap_ggh[89]=37.5664;
  XSectionMap_ggh[90]=36.7719;
  XSectionMap_ggh[91]=36.0024;
  XSectionMap_ggh[92]=35.2565;
  XSectionMap_ggh[93]=34.5342;
  XSectionMap_ggh[94]=33.833;
  XSectionMap_ggh[95]=33.1525;
  XSectionMap_ggh[96]=32.4924;
  XSectionMap_ggh[97]=31.8511;
  XSectionMap_ggh[98]=31.2283;
  XSectionMap_ggh[99]=30.6236;
  XSectionMap_ggh[100]=30.0891;
  XSectionMap_ggh[101]=29.5154;
  XSectionMap_ggh[102]=28.9585;
  XSectionMap_ggh[103]=28.4107;
  XSectionMap_ggh[104]=27.8856;
  XSectionMap_ggh[105]=27.3602;
  XSectionMap_ggh[106]=26.8628;
  XSectionMap_ggh[107]=26.3911;
  XSectionMap_ggh[108]=25.9199;
  XSectionMap_ggh[109]=25.4603;
  XSectionMap_ggh[110]=25.0119;
  XSectionMap_ggh[110.5]=24.7918;
  XSectionMap_ggh[111]=24.5743;
  XSectionMap_ggh[111.5]=24.3597;
  XSectionMap_ggh[112]=24.1486;
  XSectionMap_ggh[112.5]=23.9401;
  XSectionMap_ggh[113]=23.7343;
  XSectionMap_ggh[113.5]=23.5312;
  XSectionMap_ggh[114]=23.3306;
  XSectionMap_ggh[114.5]=23.1325;
  XSectionMap_ggh[115]=22.9369;
  XSectionMap_ggh[115.5]=22.7442;
  XSectionMap_ggh[116]=22.5534;
  XSectionMap_ggh[116.5]=22.3651;
  XSectionMap_ggh[117]=22.179;
  XSectionMap_ggh[117.5]=21.9949;
  XSectionMap_ggh[118]=21.8134;
  XSectionMap_ggh[118.5]=21.6341;
  XSectionMap_ggh[119]=21.457;
  XSectionMap_ggh[119.5]=21.282;
  XSectionMap_ggh[120]=21.109;
  XSectionMap_ggh[120.5]=20.9381;
  XSectionMap_ggh[121]=20.7692;
  XSectionMap_ggh[121.5]=20.6023;
  XSectionMap_ggh[122]=20.4373;
  XSectionMap_ggh[122.5]=20.2742;
  XSectionMap_ggh[123]=20.1131;
  XSectionMap_ggh[123.5]=19.9538;
  XSectionMap_ggh[124]=19.7963;
  XSectionMap_ggh[124.5]=19.6407;
  XSectionMap_ggh[125]=19.4868;
  XSectionMap_ggh[125.5]=19.3347;
  XSectionMap_ggh[126]=19.1843;
  XSectionMap_ggh[126.5]=19.0357;
  XSectionMap_ggh[127]=18.8887;
  XSectionMap_ggh[127.5]=18.7433;
  XSectionMap_ggh[128]=18.5996;
  XSectionMap_ggh[128.5]=18.4574;
  XSectionMap_ggh[129]=18.3169;
  XSectionMap_ggh[129.5]=18.1778;
  XSectionMap_ggh[130]=18.0403;
  XSectionMap_ggh[130.5]=17.9043;
  XSectionMap_ggh[131]=17.7698;
  XSectionMap_ggh[131.5]=17.6368;
  XSectionMap_ggh[132]=17.5053;
  XSectionMap_ggh[132.5]=17.3752;
  XSectionMap_ggh[133]=17.2464;
  XSectionMap_ggh[133.5]=17.1191;
  XSectionMap_ggh[134]=16.993;
  XSectionMap_ggh[134.5]=16.8683;
  XSectionMap_ggh[135]=16.7448;
  XSectionMap_ggh[135.5]=16.6226;
  XSectionMap_ggh[136]=16.5017;
  XSectionMap_ggh[136.5]=16.382;
  XSectionMap_ggh[137]=16.2635;
  XSectionMap_ggh[137.5]=16.1463;
  XSectionMap_ggh[138]=16.0303;
  XSectionMap_ggh[138.5]=15.9155;
  XSectionMap_ggh[139]=15.8019;
  XSectionMap_ggh[139.5]=15.6894;
  XSectionMap_ggh[140]=15.5782;
  XSectionMap_ggh[141]=15.3592;
  XSectionMap_ggh[142]=15.1446;
  XSectionMap_ggh[143]=14.9342;
  XSectionMap_ggh[144]=14.7278;
  XSectionMap_ggh[145]=14.5253;
  XSectionMap_ggh[146]=14.3267;
  XSectionMap_ggh[147]=14.1318;
  XSectionMap_ggh[148]=13.9404;
  XSectionMap_ggh[149]=13.7522;
  XSectionMap_ggh[150]=13.5672;
  XSectionMap_ggh[151]=13.3852;
  XSectionMap_ggh[152]=13.2057;
  XSectionMap_ggh[153]=13.0284;
  XSectionMap_ggh[154]=12.8527;
  XSectionMap_ggh[155]=12.6779;
  XSectionMap_ggh[156]=12.5028;
  XSectionMap_ggh[157]=12.3256;
  XSectionMap_ggh[158]=12.1439;
  XSectionMap_ggh[159]=11.9554;
  XSectionMap_ggh[160]=11.7624;
  XSectionMap_ggh[162]=11.3963;
  XSectionMap_ggh[164]=11.0387;
  XSectionMap_ggh[166]=10.7032;
  XSectionMap_ggh[168]=10.3946;
  XSectionMap_ggh[170]=10.1077;
  XSectionMap_ggh[172]=9.8376;
  XSectionMap_ggh[174]=9.5807;
  XSectionMap_ggh[176]=9.3337;
  XSectionMap_ggh[178]=9.0926;
  XSectionMap_ggh[180]=8.8521;
  XSectionMap_ggh[182]=8.6143;
  XSectionMap_ggh[184]=8.3939;
  XSectionMap_ggh[186]=8.179;
  XSectionMap_ggh[188]=7.9739;
  XSectionMap_ggh[190]=7.7803;
  XSectionMap_ggh[192]=7.5975;
  XSectionMap_ggh[194]=7.4242;
  XSectionMap_ggh[196]=7.259;
  XSectionMap_ggh[198]=7.101;
  XSectionMap_ggh[200]=6.9497;
  XSectionMap_ggh[202]=6.8042;
  XSectionMap_ggh[204]=6.6642;
  XSectionMap_ggh[206]=6.5296;
  XSectionMap_ggh[208]=6.3999;
  XSectionMap_ggh[210]=6.2744;
  XSectionMap_ggh[212]=6.1533;
  XSectionMap_ggh[214]=6.0364;
  XSectionMap_ggh[216]=5.9234;
  XSectionMap_ggh[218]=5.8142;
  XSectionMap_ggh[220]=5.7085;
  XSectionMap_ggh[222]=5.6061;
  XSectionMap_ggh[224]=5.5071;
  XSectionMap_ggh[226]=5.4112;
  XSectionMap_ggh[228]=5.3183;
  XSectionMap_ggh[230]=5.2283;
  XSectionMap_ggh[232]=5.141;
  XSectionMap_ggh[234]=5.0563;
  XSectionMap_ggh[236]=4.974;
  XSectionMap_ggh[238]=4.8944;
  XSectionMap_ggh[240]=4.817;
  XSectionMap_ggh[242]=4.7418;
  XSectionMap_ggh[244]=4.6689;
  XSectionMap_ggh[246]=4.5981;
  XSectionMap_ggh[248]=4.5294;
  XSectionMap_ggh[250]=4.4627;
  XSectionMap_ggh[252]=4.398;
  XSectionMap_ggh[254]=4.3351;
  XSectionMap_ggh[256]=4.2741;
  XSectionMap_ggh[258]=4.2149;
  XSectionMap_ggh[260]=4.1574;
  XSectionMap_ggh[262]=4.1016;
  XSectionMap_ggh[264]=4.0709;
  XSectionMap_ggh[266]=3.9951;
  XSectionMap_ggh[268]=3.9442;
  XSectionMap_ggh[270]=3.8949;
  XSectionMap_ggh[272]=3.8471;
  XSectionMap_ggh[274]=3.8009;
  XSectionMap_ggh[276]=3.7561;
  XSectionMap_ggh[278]=3.7128;
  XSectionMap_ggh[280]=3.6709;
  XSectionMap_ggh[282]=3.6302;
  XSectionMap_ggh[284]=3.591;
  XSectionMap_ggh[286]=3.553;
  XSectionMap_ggh[288]=3.5164;
  XSectionMap_ggh[290]=3.4811;
  XSectionMap_ggh[295]=3.3986;
  XSectionMap_ggh[300]=3.324;
  XSectionMap_ggh[305]=3.539;
  XSectionMap_ggh[310]=3.482;
  XSectionMap_ggh[315]=3.434;
  XSectionMap_ggh[320]=3.392;
  XSectionMap_ggh[325]=3.364;
  XSectionMap_ggh[330]=3.349;
  XSectionMap_ggh[335]=3.349;
  XSectionMap_ggh[340]=3.367;
  XSectionMap_ggh[345]=3.405;
  XSectionMap_ggh[350]=3.406;
  XSectionMap_ggh[360]=3.390;
  XSectionMap_ggh[370]=3.336;
  XSectionMap_ggh[380]=3.235;
  XSectionMap_ggh[390]=3.093;
  XSectionMap_ggh[400]=2.924;
  XSectionMap_ggh[420]=2.552;
  XSectionMap_ggh[440]=2.180;
  XSectionMap_ggh[450]=2.003;
  XSectionMap_ggh[460]=1.837;
  XSectionMap_ggh[480]=1.538;
  XSectionMap_ggh[500]=1.283;
  XSectionMap_ggh[520]=1.069;
  XSectionMap_ggh[540]=0.8912;
  XSectionMap_ggh[550]=0.8141;
  XSectionMap_ggh[560]=0.7442;
  XSectionMap_ggh[580]=0.6229;
  XSectionMap_ggh[600]=0.5230;
  XSectionMap_ggh[620]=0.4403;
  XSectionMap_ggh[640]=0.3718;
  XSectionMap_ggh[650]=0.3423;
  XSectionMap_ggh[660]=0.3152;
  XSectionMap_ggh[680]=0.2680;
  XSectionMap_ggh[700]=0.2288;
  XSectionMap_ggh[720]=0.1962;
  XSectionMap_ggh[740]=0.1687;
  XSectionMap_ggh[750]=0.1566;
  XSectionMap_ggh[760]=0.1455;
  XSectionMap_ggh[780]=0.1260;
  XSectionMap_ggh[800]=0.1095;
  XSectionMap_ggh[820]=0.09547;
  XSectionMap_ggh[840]=0.08346;
  XSectionMap_ggh[850]=0.07811;
  XSectionMap_ggh[860]=0.07321;
  XSectionMap_ggh[880]=0.06443;
  XSectionMap_ggh[900]=0.05684;
  XSectionMap_ggh[920]=0.05030;
  XSectionMap_ggh[940]=0.04463;
  XSectionMap_ggh[950]=0.04206;
  XSectionMap_ggh[960]=0.03969;
  XSectionMap_ggh[980]=0.03539;
  XSectionMap_ggh[1000]=0.03163;
  
  // VBF X-sections
  XSectionMap_vbf[80]=2.410;
  XSectionMap_vbf[81]=2.384;
  XSectionMap_vbf[82]=2.360;
  XSectionMap_vbf[83]=2.336;
  XSectionMap_vbf[84]=2.311;
  XSectionMap_vbf[85]=2.289;
  XSectionMap_vbf[86]=2.265;
  XSectionMap_vbf[87]=2.243;
  XSectionMap_vbf[88]=2.221;
  XSectionMap_vbf[89]=2.199;
  XSectionMap_vbf[90]=2.176;
  XSectionMap_vbf[91]=2.154;
  XSectionMap_vbf[92]=2.133;
  XSectionMap_vbf[93]=2.112;
  XSectionMap_vbf[94]=2.090;
  XSectionMap_vbf[95]=2.071;
  XSectionMap_vbf[96]=2.050;
  XSectionMap_vbf[97]=2.030;
  XSectionMap_vbf[98]=2.010;
  XSectionMap_vbf[99]=1.991;
  XSectionMap_vbf[100]=1.971;
  XSectionMap_vbf[101]=1.952;
  XSectionMap_vbf[102]=1.934;
  XSectionMap_vbf[103]=1.915;
  XSectionMap_vbf[104]=1.897;
  XSectionMap_vbf[105]=1.878;
  XSectionMap_vbf[106]=1.860;
  XSectionMap_vbf[107]=1.843;
  XSectionMap_vbf[108]=1.826;
  XSectionMap_vbf[109]=1.808;
  XSectionMap_vbf[110]=1.791;
  XSectionMap_vbf[110.5]=1.783;
  XSectionMap_vbf[111]=1.775;
  XSectionMap_vbf[111.5]=1.766;
  XSectionMap_vbf[112]=1.758;
  XSectionMap_vbf[112.5]=1.750;
  XSectionMap_vbf[113]=1.742;
  XSectionMap_vbf[113.5]=1.733;
  XSectionMap_vbf[114]=1.725;
  XSectionMap_vbf[114.5]=1.717;
  XSectionMap_vbf[115]=1.709;
  XSectionMap_vbf[115.5]=1.701;
  XSectionMap_vbf[116]=1.693;
  XSectionMap_vbf[116.5]=1.686;
  XSectionMap_vbf[117]=1.678;
  XSectionMap_vbf[117.5]=1.670;
  XSectionMap_vbf[118]=1.661;
  XSectionMap_vbf[118.5]=1.654;
  XSectionMap_vbf[119]=1.647;
  XSectionMap_vbf[119.5]=1.639;
  XSectionMap_vbf[120]=1.632;
  XSectionMap_vbf[120.5]=1.624;
  XSectionMap_vbf[121]=1.617;
  XSectionMap_vbf[121.5]=1.609;
  XSectionMap_vbf[122]=1.602;
  XSectionMap_vbf[122.5]=1.595;
  XSectionMap_vbf[123]=1.588;
  XSectionMap_vbf[123.5]=1.580;
  XSectionMap_vbf[124]=1.573;
  XSectionMap_vbf[124.5]=1.566;
  XSectionMap_vbf[125]=1.559;
  XSectionMap_vbf[125.5]=1.552;
  XSectionMap_vbf[126]=1.544;
  XSectionMap_vbf[126.5]=1.539;
  XSectionMap_vbf[127]=1.531;
  XSectionMap_vbf[127.5]=1.524;
  XSectionMap_vbf[128]=1.517;
  XSectionMap_vbf[128.5]=1.511;
  XSectionMap_vbf[129]=1.504;
  XSectionMap_vbf[129.5]=1.497;
  XSectionMap_vbf[130]=1.490;
  XSectionMap_vbf[130.5]=1.483;
  XSectionMap_vbf[131]=1.477;
  XSectionMap_vbf[131.5]=1.470;
  XSectionMap_vbf[132]=1.463;
  XSectionMap_vbf[132.5]=1.458;
  XSectionMap_vbf[133]=1.451;
  XSectionMap_vbf[133.5]=1.444;
  XSectionMap_vbf[134]=1.439;
  XSectionMap_vbf[134.5]=1.432;
  XSectionMap_vbf[135]=1.425;
  XSectionMap_vbf[135.5]=1.419;
  XSectionMap_vbf[136]=1.413;
  XSectionMap_vbf[136.5]=1.407;
  XSectionMap_vbf[137]=1.401;
  XSectionMap_vbf[137.5]=1.395;
  XSectionMap_vbf[138]=1.388;
  XSectionMap_vbf[138.5]=1.382;
  XSectionMap_vbf[139]=1.376;
  XSectionMap_vbf[139.5]=1.370;
  XSectionMap_vbf[140]=1.365;
  XSectionMap_vbf[141]=1.352;
  XSectionMap_vbf[142]=1.341;
  XSectionMap_vbf[143]=1.329;
  XSectionMap_vbf[144]=1.317;
  XSectionMap_vbf[145]=1.306;
  XSectionMap_vbf[146]=1.295;
  XSectionMap_vbf[147]=1.284;
  XSectionMap_vbf[148]=1.272;
  XSectionMap_vbf[149]=1.261;
  XSectionMap_vbf[150]=1.251;
  XSectionMap_vbf[151]=1.240;
  XSectionMap_vbf[152]=1.229;
  XSectionMap_vbf[153]=1.218;
  XSectionMap_vbf[154]=1.208;
  XSectionMap_vbf[155]=1.197;
  XSectionMap_vbf[156]=1.187;
  XSectionMap_vbf[157]=1.176;
  XSectionMap_vbf[158]=1.166;
  XSectionMap_vbf[159]=1.155;
  XSectionMap_vbf[160]=1.146;
  XSectionMap_vbf[162]=1.136;
  XSectionMap_vbf[164]=1.123;
  XSectionMap_vbf[165]=1.115;
  XSectionMap_vbf[166]=1.106;
  XSectionMap_vbf[168]=1.088;
  XSectionMap_vbf[170]=1.070;
  XSectionMap_vbf[172]=1.052;
  XSectionMap_vbf[174]=1.035;
  XSectionMap_vbf[175]=1.026;
  XSectionMap_vbf[176]=1.017;
  XSectionMap_vbf[178]=1.000;
  XSectionMap_vbf[180]=0.982;
  XSectionMap_vbf[182]=0.967;
  XSectionMap_vbf[184]=0.9558;
  XSectionMap_vbf[185]=0.9496;
  XSectionMap_vbf[186]=0.9429;
  XSectionMap_vbf[188]=0.9286;
  XSectionMap_vbf[190]=0.9139;
  XSectionMap_vbf[192]=0.8998;
  XSectionMap_vbf[194]=0.8854;
  XSectionMap_vbf[195]=0.8783;
  XSectionMap_vbf[196]=0.8714;
  XSectionMap_vbf[198]=0.8574;
  XSectionMap_vbf[200]=0.8441;
  XSectionMap_vbf[202]=0.8309;
  XSectionMap_vbf[204]=0.8178;
  XSectionMap_vbf[206]=0.8051;
  XSectionMap_vbf[208]=0.7927;
  XSectionMap_vbf[210]=0.7805;
  XSectionMap_vbf[212]=0.7687;
  XSectionMap_vbf[214]=0.7568;
  XSectionMap_vbf[216]=0.7452;
  XSectionMap_vbf[218]=0.734;
  XSectionMap_vbf[220]=0.7229;
  XSectionMap_vbf[222]=0.712;
  XSectionMap_vbf[224]=0.7016;
  XSectionMap_vbf[226]=0.6913;
  XSectionMap_vbf[228]=0.6808;
  XSectionMap_vbf[230]=0.6707;
  XSectionMap_vbf[232]=0.661;
  XSectionMap_vbf[234]=0.6513;
  XSectionMap_vbf[236]=0.6418;
  XSectionMap_vbf[238]=0.6326;
  XSectionMap_vbf[240]=0.6234;
  XSectionMap_vbf[242]=0.6144;
  XSectionMap_vbf[244]=0.6056;
  XSectionMap_vbf[246]=0.5969;
  XSectionMap_vbf[248]=0.5885;
  XSectionMap_vbf[250]=0.5802;
  XSectionMap_vbf[252]=0.572;
  XSectionMap_vbf[254]=0.564;
  XSectionMap_vbf[256]=0.5562;
  XSectionMap_vbf[258]=0.5484;
  XSectionMap_vbf[260]=0.5408;
  XSectionMap_vbf[262]=0.5333;
  XSectionMap_vbf[264]=0.5259;
  XSectionMap_vbf[266]=0.5187;
  XSectionMap_vbf[268]=0.5116;
  XSectionMap_vbf[270]=0.5047;
  XSectionMap_vbf[272]=0.4978;
  XSectionMap_vbf[274]=0.491;
  XSectionMap_vbf[276]=0.4845;
  XSectionMap_vbf[278]=0.478;
  XSectionMap_vbf[280]=0.4715;
  XSectionMap_vbf[282]=0.4652;
  XSectionMap_vbf[284]=0.459;
  XSectionMap_vbf[286]=0.453;
  XSectionMap_vbf[288]=0.447;
  XSectionMap_vbf[290]=0.4716;
  XSectionMap_vbf[295]=0.4562;
  XSectionMap_vbf[300]=0.4408;
  XSectionMap_vbf[305]=0.4266;
  XSectionMap_vbf[310]=0.4131;
  XSectionMap_vbf[315]=0.3999;
  XSectionMap_vbf[320]=0.3875;
  XSectionMap_vbf[325]=0.3753;
  XSectionMap_vbf[330]=0.3637;
  XSectionMap_vbf[335]=0.3526;
  XSectionMap_vbf[340]=0.3422;
  XSectionMap_vbf[345]=0.3303;
  XSectionMap_vbf[350]=0.320;
  XSectionMap_vbf[360]=0.3028;
  XSectionMap_vbf[370]=0.2896;
  XSectionMap_vbf[380]=0.2776;
  XSectionMap_vbf[390]=0.266;
  XSectionMap_vbf[400]=0.2543;
  XSectionMap_vbf[420]=0.2317;
  XSectionMap_vbf[440]=0.2103;
  XSectionMap_vbf[450]=0.1751;
  XSectionMap_vbf[460]=0.1905;
  XSectionMap_vbf[480]=0.1724;
  XSectionMap_vbf[500]=0.1561;
  XSectionMap_vbf[520]=0.1414;
  XSectionMap_vbf[540]=0.1283;
  XSectionMap_vbf[550]=0.1038;
  XSectionMap_vbf[560]=0.1166;
  XSectionMap_vbf[580]=0.1062;
  XSectionMap_vbf[600]=0.09688;
  XSectionMap_vbf[620]=0.08861;
  XSectionMap_vbf[640]=0.08121;
  XSectionMap_vbf[650]=0.06397;
  XSectionMap_vbf[660]=0.07459;
  XSectionMap_vbf[680]=0.06865;
  XSectionMap_vbf[700]=0.0633;
  XSectionMap_vbf[720]=0.05853;
  XSectionMap_vbf[740]=0.0542;
  XSectionMap_vbf[750]=0.04058;
  XSectionMap_vbf[760]=0.05032;
  XSectionMap_vbf[780]=0.04682;
  XSectionMap_vbf[800]=0.04365;
  XSectionMap_vbf[820]=0.04078;
  XSectionMap_vbf[840]=0.03815;
  XSectionMap_vbf[850]=0.02632;
  XSectionMap_vbf[860]=0.03579;
  XSectionMap_vbf[880]=0.03363;
  XSectionMap_vbf[900]=0.03164;
  XSectionMap_vbf[920]=0.02986;
  XSectionMap_vbf[940]=0.0282;
  XSectionMap_vbf[950]=0.01719;
  XSectionMap_vbf[960]=0.02669;
  XSectionMap_vbf[980]=0.02524;
  XSectionMap_vbf[1000]=0.02399;
  
  // WH X-Sections
  XSectionMap_wh[80]=2.784;
  XSectionMap_wh[81]=2.687;
  XSectionMap_wh[82]=2.595;
  XSectionMap_wh[83]=2.505;
  XSectionMap_wh[84]=2.420;
  XSectionMap_wh[85]=2.338;
  XSectionMap_wh[86]=2.258;
  XSectionMap_wh[87]=2.183;
  XSectionMap_wh[88]=2.110;
  XSectionMap_wh[89]=2.039;
  XSectionMap_wh[90]=1.972;
  XSectionMap_wh[91]=1.908;
  XSectionMap_wh[92]=1.847;
  XSectionMap_wh[93]=1.787;
  XSectionMap_wh[94]=1.731;
  XSectionMap_wh[95]=1.676;
  XSectionMap_wh[96]=1.623;
  XSectionMap_wh[97]=1.573;
  XSectionMap_wh[98]=1.524;
  XSectionMap_wh[99]=1.477;
  XSectionMap_wh[100]=1.432;
  XSectionMap_wh[101]=1.389;
  XSectionMap_wh[102]=1.347;
  XSectionMap_wh[103]=1.306;
  XSectionMap_wh[104]=1.266;
  XSectionMap_wh[105]=1.229;
  XSectionMap_wh[106]=1.192;
  XSectionMap_wh[107]=1.158;
  XSectionMap_wh[108]=1.124;
  XSectionMap_wh[109]=1.092;
  XSectionMap_wh[110]=1.060;
  XSectionMap_wh[110.5]=1.045;
  XSectionMap_wh[111]=1.030;
  XSectionMap_wh[111.5]=1.015;
  XSectionMap_wh[112]=0.9998;
  XSectionMap_wh[112.5]=0.9852;
  XSectionMap_wh[113]=0.9709;
  XSectionMap_wh[113.5]=0.9570;
  XSectionMap_wh[114]=0.9432;
  XSectionMap_wh[114.5]=0.9297;
  XSectionMap_wh[115]=0.9165;
  XSectionMap_wh[115.5]=0.9035;
  XSectionMap_wh[116]=0.8907;
  XSectionMap_wh[116.5]=0.8782;
  XSectionMap_wh[117]=0.8659;
  XSectionMap_wh[117.5]=0.8538;
  XSectionMap_wh[118]=0.8420;
  XSectionMap_wh[118.5]=0.8303;
  XSectionMap_wh[119]=0.8187;
  XSectionMap_wh[119.5]=0.8075;
  XSectionMap_wh[120]=0.7966;
  XSectionMap_wh[120.5]=0.7859;
  XSectionMap_wh[121]=0.7753;
  XSectionMap_wh[121.5]=0.7649;
  XSectionMap_wh[122]=0.7547;
  XSectionMap_wh[122.5]=0.7446;
  XSectionMap_wh[123]=0.7347;
  XSectionMap_wh[123.5]=0.7249;
  XSectionMap_wh[124]=0.7154;
  XSectionMap_wh[124.5]=0.7060;
  XSectionMap_wh[125]=0.6966;
  XSectionMap_wh[125.5]=0.6873;
  XSectionMap_wh[126]=0.6782;
  XSectionMap_wh[126.5]=0.6691;
  XSectionMap_wh[127]=0.6602;
  XSectionMap_wh[127.5]=0.6515;
  XSectionMap_wh[128]=0.6429;
  XSectionMap_wh[128.5]=0.6344;
  XSectionMap_wh[129]=0.6260;
  XSectionMap_wh[129.5]=0.6177;
  XSectionMap_wh[130]=0.6095;
  XSectionMap_wh[130.5]=0.6015;
  XSectionMap_wh[131]=0.5936;
  XSectionMap_wh[131.5]=0.5859;
  XSectionMap_wh[132]=0.5783;
  XSectionMap_wh[132.5]=0.5708;
  XSectionMap_wh[133]=0.5634;
  XSectionMap_wh[133.5]=0.5562;
  XSectionMap_wh[134]=0.5491;
  XSectionMap_wh[134.5]=0.5420;
  XSectionMap_wh[135]=0.5351;
  XSectionMap_wh[135.5]=0.5283;
  XSectionMap_wh[136]=0.5215;
  XSectionMap_wh[136.5]=0.5149;
  XSectionMap_wh[137]=0.5084;
  XSectionMap_wh[137.5]=0.5020;
  XSectionMap_wh[138]=0.4956;
  XSectionMap_wh[138.5]=0.4894;
  XSectionMap_wh[139]=0.4833;
  XSectionMap_wh[139.5]=0.4772;
  XSectionMap_wh[140]=0.4713;
  XSectionMap_wh[141]=0.4597;
  XSectionMap_wh[142]=0.4484;
  XSectionMap_wh[143]=0.4375;
  XSectionMap_wh[144]=0.4268;
  XSectionMap_wh[145]=0.4164;
  XSectionMap_wh[146]=0.4062;
  XSectionMap_wh[147]=0.3963;
  XSectionMap_wh[148]=0.3867;
  XSectionMap_wh[149]=0.3773;
  XSectionMap_wh[150]=0.3681;
  XSectionMap_wh[151]=0.3593;
  XSectionMap_wh[152]=0.3507;
  XSectionMap_wh[153]=0.3422;
  XSectionMap_wh[154]=0.3337;
  XSectionMap_wh[155]=0.3252;
  XSectionMap_wh[156]=0.3157;
  XSectionMap_wh[157]=0.3064;
  XSectionMap_wh[158]=0.2975;
  XSectionMap_wh[159]=0.2892;
  XSectionMap_wh[160]=0.2817;
  XSectionMap_wh[162]=0.2720;
  XSectionMap_wh[164]=0.2637;
  XSectionMap_wh[166]=0.2543;
  XSectionMap_wh[168]=0.2436;
  XSectionMap_wh[170]=0.2329;
  XSectionMap_wh[172]=0.2229;
  XSectionMap_wh[174]=0.2135;
  XSectionMap_wh[176]=0.2045;
  XSectionMap_wh[178]=0.1961;
  XSectionMap_wh[180]=0.1883;
  XSectionMap_wh[182]=0.1814;
  XSectionMap_wh[184]=0.1748;
  XSectionMap_wh[186]=0.1683;
  XSectionMap_wh[188]=0.1619;
  XSectionMap_wh[190]=0.1556;
  XSectionMap_wh[192]=0.1498;
  XSectionMap_wh[194]=0.1443;
  XSectionMap_wh[196]=0.1389;
  XSectionMap_wh[198]=0.1336;
  XSectionMap_wh[200]=0.1286;
  XSectionMap_wh[202]=0.1238;
  XSectionMap_wh[204]=0.1193;
  XSectionMap_wh[206]=0.1150;
  XSectionMap_wh[208]=0.1109;
  XSectionMap_wh[210]=0.1070;
  XSectionMap_wh[212]=0.1032;
  XSectionMap_wh[214]=0.09958;
  XSectionMap_wh[216]=0.09611;
  XSectionMap_wh[218]=0.09279;
  XSectionMap_wh[220]=0.08961;
  XSectionMap_wh[222]=0.08657;
  XSectionMap_wh[224]=0.08365;
  XSectionMap_wh[226]=0.08085;
  XSectionMap_wh[228]=0.07817;
  XSectionMap_wh[230]=0.07559;
  XSectionMap_wh[232]=0.07308;
  XSectionMap_wh[234]=0.07067;
  XSectionMap_wh[236]=0.06835;
  XSectionMap_wh[238]=0.06612;
  XSectionMap_wh[240]=0.06398;
  XSectionMap_wh[242]=0.06194;
  XSectionMap_wh[244]=0.05997;
  XSectionMap_wh[246]=0.05808;
  XSectionMap_wh[248]=0.05626;
  XSectionMap_wh[250]=0.05450;
  XSectionMap_wh[252]=0.05280;
  XSectionMap_wh[254]=0.05116;
  XSectionMap_wh[256]=0.04958;
  XSectionMap_wh[258]=0.04806;
  XSectionMap_wh[260]=0.04660;
  XSectionMap_wh[262]=0.04522;
  XSectionMap_wh[264]=0.04389;
  XSectionMap_wh[266]=0.04260;
  XSectionMap_wh[268]=0.04136;
  XSectionMap_wh[270]=0.04016;
  XSectionMap_wh[272]=0.03897;
  XSectionMap_wh[274]=0.03782;
  XSectionMap_wh[276]=0.03671;
  XSectionMap_wh[278]=0.03563;
  XSectionMap_wh[280]=0.03459;
  XSectionMap_wh[282]=0.03359;
  XSectionMap_wh[284]=0.03263;
  XSectionMap_wh[286]=0.03170;
  XSectionMap_wh[288]=0.03080;
  XSectionMap_wh[290]=0.02993;
  XSectionMap_wh[295]=0.02789;
  XSectionMap_wh[300]=0.02602;
  
  // ZH X-Sections
  XSectionMap_zh[80]=1.470;
  XSectionMap_zh[81]=1.421;
  XSectionMap_zh[82]=1.374;
  XSectionMap_zh[83]=1.328;
  XSectionMap_zh[84]=1.285;
  XSectionMap_zh[85]=1.243;
  XSectionMap_zh[86]=1.203;
  XSectionMap_zh[87]=1.164;
  XSectionMap_zh[88]=1.127;
  XSectionMap_zh[89]=1.092;
  XSectionMap_zh[90]=1.057;
  XSectionMap_zh[91]=1.025;
  XSectionMap_zh[92]=0.9934;
  XSectionMap_zh[93]=0.9635;
  XSectionMap_zh[94]=0.9341;
  XSectionMap_zh[95]=0.9060;
  XSectionMap_zh[96]=0.8792;
  XSectionMap_zh[97]=0.8533;
  XSectionMap_zh[98]=0.8281;
  XSectionMap_zh[99]=0.8039;
  XSectionMap_zh[100]=0.7807;
  XSectionMap_zh[101]=0.7582;
  XSectionMap_zh[102]=0.7365;
  XSectionMap_zh[103]=0.7154;
  XSectionMap_zh[104]=0.6948;
  XSectionMap_zh[105]=0.6750;
  XSectionMap_zh[106]=0.6561;
  XSectionMap_zh[107]=0.6379;
  XSectionMap_zh[108]=0.6203;
  XSectionMap_zh[109]=0.6033;
  XSectionMap_zh[110]=0.5869;
  XSectionMap_zh[110.5]=0.5788;
  XSectionMap_zh[111]=0.5708;
  XSectionMap_zh[111.5]=0.5629;
  XSectionMap_zh[112]=0.5552;
  XSectionMap_zh[112.5]=0.5476;
  XSectionMap_zh[113]=0.5402;
  XSectionMap_zh[113.5]=0.5329;
  XSectionMap_zh[114]=0.5258;
  XSectionMap_zh[114.5]=0.5187;
  XSectionMap_zh[115]=0.5117;
  XSectionMap_zh[115.5]=0.5049;
  XSectionMap_zh[116]=0.4981;
  XSectionMap_zh[116.5]=0.4916;
  XSectionMap_zh[117]=0.4850;
  XSectionMap_zh[117.5]=0.4787;
  XSectionMap_zh[118]=0.4724;
  XSectionMap_zh[118.5]=0.4662;
  XSectionMap_zh[119]=0.4602;
  XSectionMap_zh[119.5]=0.4542;
  XSectionMap_zh[120]=0.4483;
  XSectionMap_zh[120.5]=0.4426;
  XSectionMap_zh[121]=0.4368;
  XSectionMap_zh[121.5]=0.4312;
  XSectionMap_zh[122]=0.4257;
  XSectionMap_zh[122.5]=0.4203;
  XSectionMap_zh[123]=0.4150;
  XSectionMap_zh[123.5]=0.4096;
  XSectionMap_zh[124]=0.4044;
  XSectionMap_zh[124.5]=0.3993;
  XSectionMap_zh[125]=0.3943;
  XSectionMap_zh[125.5]=0.3893;
  XSectionMap_zh[126]=0.3843;
  XSectionMap_zh[126.5]=0.3794;
  XSectionMap_zh[127]=0.3746;
  XSectionMap_zh[127.5]=0.3699;
  XSectionMap_zh[128]=0.3652;
  XSectionMap_zh[128.5]=0.3606;
  XSectionMap_zh[129]=0.3561;
  XSectionMap_zh[129.5]=0.3516;
  XSectionMap_zh[130]=0.3473;
  XSectionMap_zh[130.5]=0.3430;
  XSectionMap_zh[131]=0.3388;
  XSectionMap_zh[131.5]=0.3347;
  XSectionMap_zh[132]=0.3306;
  XSectionMap_zh[132.5]=0.3266;
  XSectionMap_zh[133]=0.3226;
  XSectionMap_zh[133.5]=0.3188;
  XSectionMap_zh[134]=0.3149;
  XSectionMap_zh[134.5]=0.3112;
  XSectionMap_zh[135]=0.3074;
  XSectionMap_zh[135.5]=0.3038;
  XSectionMap_zh[136]=0.3001;
  XSectionMap_zh[136.5]=0.2966;
  XSectionMap_zh[137]=0.2930;
  XSectionMap_zh[137.5]=0.2895;
  XSectionMap_zh[138]=0.2861;
  XSectionMap_zh[138.5]=0.2827;
  XSectionMap_zh[139]=0.2793;
  XSectionMap_zh[139.5]=0.2760;
  XSectionMap_zh[140]=0.2728;
  XSectionMap_zh[141]=0.2664;
  XSectionMap_zh[142]=0.2601;
  XSectionMap_zh[143]=0.2541;
  XSectionMap_zh[144]=0.2482;
  XSectionMap_zh[145]=0.2424;
  XSectionMap_zh[146]=0.2368;
  XSectionMap_zh[147]=0.2314;
  XSectionMap_zh[148]=0.2261;
  XSectionMap_zh[149]=0.2209;
  XSectionMap_zh[150]=0.2159;
  XSectionMap_zh[151]=0.2110;
  XSectionMap_zh[152]=0.2063;
  XSectionMap_zh[153]=0.2016;
  XSectionMap_zh[154]=0.1969;
  XSectionMap_zh[155]=0.1923;
  XSectionMap_zh[156]=0.1871;
  XSectionMap_zh[157]=0.1821;
  XSectionMap_zh[158]=0.1773;
  XSectionMap_zh[159]=0.1728;
  XSectionMap_zh[160]=0.1687;
  XSectionMap_zh[162]=0.1634;
  XSectionMap_zh[164]=0.1587;
  XSectionMap_zh[166]=0.1533;
  XSectionMap_zh[168]=0.1471;
  XSectionMap_zh[170]=0.1408;
  XSectionMap_zh[172]=0.1350;
  XSectionMap_zh[174]=0.1294;
  XSectionMap_zh[176]=0.1239;
  XSectionMap_zh[178]=0.1186;
  XSectionMap_zh[180]=0.1137;
  XSectionMap_zh[182]=0.1095;
  XSectionMap_zh[184]=0.1057;
  XSectionMap_zh[186]=0.1018;
  XSectionMap_zh[188]=0.09798;
  XSectionMap_zh[190]=0.09428;
  XSectionMap_zh[192]=0.09079;
  XSectionMap_zh[194]=0.08745;
  XSectionMap_zh[196]=0.08426;
  XSectionMap_zh[198]=0.08120;
  XSectionMap_zh[200]=0.07827;
  XSectionMap_zh[202]=0.07545;
  XSectionMap_zh[204]=0.07274;
  XSectionMap_zh[206]=0.07014;
  XSectionMap_zh[208]=0.06765;
  XSectionMap_zh[210]=0.06526;
  XSectionMap_zh[212]=0.06299;
  XSectionMap_zh[214]=0.06080;
  XSectionMap_zh[216]=0.05871;
  XSectionMap_zh[218]=0.05670;
  XSectionMap_zh[220]=0.05476;
  XSectionMap_zh[222]=0.05290;
  XSectionMap_zh[224]=0.05110;
  XSectionMap_zh[226]=0.04937;
  XSectionMap_zh[228]=0.04771;
  XSectionMap_zh[230]=0.04614;
  XSectionMap_zh[232]=0.04460;
  XSectionMap_zh[234]=0.04311;
  XSectionMap_zh[236]=0.04169;
  XSectionMap_zh[238]=0.04032;
  XSectionMap_zh[240]=0.03901;
  XSectionMap_zh[242]=0.03775;
  XSectionMap_zh[244]=0.03653;
  XSectionMap_zh[246]=0.03536;
  XSectionMap_zh[248]=0.03423;
  XSectionMap_zh[250]=0.03314;
  XSectionMap_zh[252]=0.03208;
  XSectionMap_zh[254]=0.03106;
  XSectionMap_zh[256]=0.03007;
  XSectionMap_zh[258]=0.02912;
  XSectionMap_zh[260]=0.02821;
  XSectionMap_zh[262]=0.02734;
  XSectionMap_zh[264]=0.02650;
  XSectionMap_zh[266]=0.02569;
  XSectionMap_zh[268]=0.02491;
  XSectionMap_zh[270]=0.02415;
  XSectionMap_zh[272]=0.02342;
  XSectionMap_zh[274]=0.02272;
  XSectionMap_zh[276]=0.02204;
  XSectionMap_zh[278]=0.02138;
  XSectionMap_zh[280]=0.02075;
  XSectionMap_zh[282]=0.02014;
  XSectionMap_zh[284]=0.01954;
  XSectionMap_zh[286]=0.01897;
  XSectionMap_zh[288]=0.01842;
  XSectionMap_zh[290]=0.01788;
  XSectionMap_zh[295]=0.01662;
  XSectionMap_zh[300]=0.01547;

  //WZH X-Sections
  for (std::map<double, double>::const_iterator iter = XSectionMap_wh.begin(); iter != XSectionMap_wh.end(); ++iter)
    XSectionMap_wzh[iter->first]=iter->second+XSectionMap_zh[iter->first];
  
  //TTH X-Sections
  XSectionMap_tth[90]=0.3233;
  XSectionMap_tth[95]=0.2812;
  XSectionMap_tth[100]=0.2453;
  XSectionMap_tth[105]=0.2148;
  XSectionMap_tth[110]=0.1887;
  XSectionMap_tth[115]=0.1663;
  XSectionMap_tth[120]=0.1470;
  XSectionMap_tth[125]=0.1302;
  XSectionMap_tth[130]=0.1157;
  XSectionMap_tth[135]=0.1031;
  XSectionMap_tth[140]=0.09207;
  XSectionMap_tth[145]=0.08246;
  XSectionMap_tth[150]=0.07403;
  XSectionMap_tth[155]=0.06664;
  XSectionMap_tth[160]=0.06013;
  XSectionMap_tth[165]=0.05439;
  XSectionMap_tth[170]=0.04930;
  XSectionMap_tth[175]=0.04480;
  XSectionMap_tth[180]=0.04080;
  XSectionMap_tth[185]=0.03725;
  XSectionMap_tth[190]=0.03408;
  XSectionMap_tth[195]=0.03125;
  XSectionMap_tth[200]=0.02872;
  XSectionMap_tth[210]=0.02442;
  XSectionMap_tth[220]=0.02094;
  XSectionMap_tth[230]=0.01810;
  XSectionMap_tth[240]=0.01574;
  XSectionMap_tth[250]=0.01380;
  XSectionMap_tth[260]=0.01219;
  XSectionMap_tth[270]=0.01083;
  XSectionMap_tth[280]=0.009686;
  XSectionMap_tth[290]=0.008705;
  XSectionMap_tth[300]=0.007862;
  
}

void Normalization_8TeV::FillSignalTypes(){

  SignalTypeMap[-57]=std::make_pair<TString,double>("ggh",123);
  SignalTypeMap[-58]=std::make_pair<TString,double>("vbf",123);
  SignalTypeMap[-60]=std::make_pair<TString,double>("wzh",123);
  SignalTypeMap[-59]=std::make_pair<TString,double>("tth",123);
  SignalTypeMap[-53]=std::make_pair<TString,double>("ggh",121);
  SignalTypeMap[-54]=std::make_pair<TString,double>("vbf",121);
  SignalTypeMap[-56]=std::make_pair<TString,double>("wzh",121);
  SignalTypeMap[-55]=std::make_pair<TString,double>("tth",121);
  SignalTypeMap[-65]=std::make_pair<TString,double>("ggh",160);
  SignalTypeMap[-66]=std::make_pair<TString,double>("vbf",160);
  SignalTypeMap[-68]=std::make_pair<TString,double>("wzh",160);
  SignalTypeMap[-67]=std::make_pair<TString,double>("tth",160);
  SignalTypeMap[-61]=std::make_pair<TString,double>("ggh",155);
  SignalTypeMap[-62]=std::make_pair<TString,double>("vbf",155);
  SignalTypeMap[-64]=std::make_pair<TString,double>("wzh",155);
  SignalTypeMap[-63]=std::make_pair<TString,double>("tth",155);
  SignalTypeMap[-49]=std::make_pair<TString,double>("ggh",150);
  SignalTypeMap[-50]=std::make_pair<TString,double>("vbf",150);
  SignalTypeMap[-52]=std::make_pair<TString,double>("wzh",150);
  SignalTypeMap[-51]=std::make_pair<TString,double>("tth",150);
  SignalTypeMap[-45]=std::make_pair<TString,double>("ggh",145);
  SignalTypeMap[-46]=std::make_pair<TString,double>("vbf",145);
  SignalTypeMap[-48]=std::make_pair<TString,double>("wzh",145);
  SignalTypeMap[-47]=std::make_pair<TString,double>("tth",145);
  SignalTypeMap[-33]=std::make_pair<TString,double>("ggh",140);
  SignalTypeMap[-34]=std::make_pair<TString,double>("vbf",140);
  SignalTypeMap[-36]=std::make_pair<TString,double>("wzh",140);
  SignalTypeMap[-35]=std::make_pair<TString,double>("tth",140);
  SignalTypeMap[-41]=std::make_pair<TString,double>("ggh",135);
  SignalTypeMap[-42]=std::make_pair<TString,double>("vbf",135);
  SignalTypeMap[-44]=std::make_pair<TString,double>("wzh",135);
  SignalTypeMap[-43]=std::make_pair<TString,double>("tth",135);
  SignalTypeMap[-29]=std::make_pair<TString,double>("ggh",130);
  SignalTypeMap[-30]=std::make_pair<TString,double>("vbf",130);
  SignalTypeMap[-32]=std::make_pair<TString,double>("wzh",130);
  SignalTypeMap[-31]=std::make_pair<TString,double>("tth",130);
  SignalTypeMap[-37]=std::make_pair<TString,double>("ggh",125);
  SignalTypeMap[-38]=std::make_pair<TString,double>("vbf",125);
  SignalTypeMap[-40]=std::make_pair<TString,double>("wzh",125);
  SignalTypeMap[-39]=std::make_pair<TString,double>("tth",125);
  SignalTypeMap[-25]=std::make_pair<TString,double>("ggh",120);
  SignalTypeMap[-26]=std::make_pair<TString,double>("vbf",120);
  SignalTypeMap[-28]=std::make_pair<TString,double>("wzh",120);
  SignalTypeMap[-27]=std::make_pair<TString,double>("tth",120);
  SignalTypeMap[-21]=std::make_pair<TString,double>("ggh",115);
  SignalTypeMap[-22]=std::make_pair<TString,double>("vbf",115);
  SignalTypeMap[-24]=std::make_pair<TString,double>("wzh",115);
  SignalTypeMap[-23]=std::make_pair<TString,double>("tth",115);
  SignalTypeMap[-17]=std::make_pair<TString,double>("ggh",110);
  SignalTypeMap[-18]=std::make_pair<TString,double>("vbf",110);
  SignalTypeMap[-19]=std::make_pair<TString,double>("wzh",110);
  SignalTypeMap[-20]=std::make_pair<TString,double>("tth",110);
  SignalTypeMap[-13]=std::make_pair<TString,double>("ggh",105);
  SignalTypeMap[-14]=std::make_pair<TString,double>("vbf",105);
  SignalTypeMap[-16]=std::make_pair<TString,double>("wzh",105);
  SignalTypeMap[-15]=std::make_pair<TString,double>("tth",105);
  SignalTypeMap[-69]=std::make_pair<TString,double>("ggh",100);
  SignalTypeMap[-70]=std::make_pair<TString,double>("vbf",100);
  SignalTypeMap[-72]=std::make_pair<TString,double>("wzh",100);
  SignalTypeMap[-71]=std::make_pair<TString,double>("tth",100);

}
double Normalization_8TeV::GetBR(double mass) {

  for (std::map<double, double>::const_iterator iter = BranchingRatioMap.begin();  iter != BranchingRatioMap.end(); ++iter) {
    if (mass==iter->first) return iter->second;
    if (mass>iter->first) {
      double lowmass = iter->first;
      double lowbr = iter->second;
      ++iter;
      if (mass<iter->first) {
        double highmass = iter->first;
        double highbr = iter->second;
        double br = (highbr-lowbr)/(highmass-lowmass)*(mass-lowmass)+lowbr;
        return br;
      }
      --iter;
    }
  }
  
  std::cout << "Warning branching ratio outside range of 90-250GeV!!!!" << std::endl;
  //std::exit(1);
  
}


double Normalization_8TeV::GetXsection(double mass, TString HistName) {

  std::map<double,double> *XSectionMap;

  if (HistName.Contains("ggh")) {
    XSectionMap = &XSectionMap_ggh;
  } else if (HistName.Contains("vbf")) {
    XSectionMap = &XSectionMap_vbf;
  } else if (HistName.Contains("wh") && !HistName.Contains("wzh")) {
    XSectionMap = &XSectionMap_wh;
  } else if (HistName.Contains("zh") && !HistName.Contains("wzh")) {
    XSectionMap = &XSectionMap_zh;
  } else if (HistName.Contains("wzh")) {
    XSectionMap = &XSectionMap_wzh;
  } else if (HistName.Contains("tth")) {
    XSectionMap = &XSectionMap_tth;
  } else {
    std::cout << "Warning ggh, vbf, wh, zh, wzh, or tth not found in histname!!!!" << std::endl;
    //exit(1);
  }

  for (std::map<double, double>::const_iterator iter = XSectionMap->begin();  iter != XSectionMap->end(); ++iter) {
    if (mass==iter->first) return iter->second;
    if (mass>iter->first) {
      double lowmass = iter->first;
      double lowxsec = iter->second;
      ++iter;
      if (mass<iter->first) {
        double highmass = iter->first;
        double highxsec = iter->second;
        double xsec = (highxsec-lowxsec)/(highmass-lowmass)*(mass-lowmass)+lowxsec;
        return xsec;
      }
      --iter;
    }
  }

  std::cout << "Warning cross section outside range of 80-300GeV!!!!" << std::endl;
  //exit(1);

}
// Simple accessors
TString Normalization_8TeV::GetProcess(int ty){
  return SignalTypeMap[ty].first;
}

double Normalization_8TeV::GetMass(int ty){
  return SignalTypeMap[ty].second;
}
double Normalization_8TeV::GetXsection(int ty){
  std::pair<TString,double> proc_mass = SignalTypeMap[ty];
  return GetXsection(proc_mass.second,proc_mass.first);
}
double Normalization_8TeV::GetBR(int ty){
  std::pair<TString,double> proc_mass = SignalTypeMap[ty];
  return GetBR(proc_mass.second);
}

double Normalization_8TeV::GetXsection(double mass) {
  return GetXsection(mass,"ggh") + GetXsection(mass,"vbf") + GetXsection(mass,"wh") + GetXsection(mass,"zh") + GetXsection(mass,"tth");
}

double Normalization_8TeV::GetNorm(double mass1, TH1F* hist1, double mass2, TH1F* hist2, double mass) {

  double br = GetBR(mass);
  double br1 = GetBR(mass1);
  double br2 = GetBR(mass2);
  
  double xsec = GetXsection(mass, hist1->GetName());
  double xsec1 = GetXsection(mass1, hist1->GetName());
  double xsec2 = GetXsection(mass2, hist2->GetName());
  
  double alpha = 1.0*(mass-mass1)/(mass2-mass1);
  double effAcc1 = hist1->Integral()/(xsec1*br1);
  double effAcc2 = hist2->Integral()/(xsec2*br2);

  double Normalization = (xsec*br)*(effAcc1 + alpha * (effAcc2 - effAcc1));
  return Normalization;
  
}

void Normalization_8TeV::CheckNorm(double Min, double Max, double Step, TString histname="") {

  vector <double> Mass;
  vector <double> BranchingRatio;
  vector <double> XSection;
  for (double i=Min; i<Max; i+=Step) {
    Mass.push_back(i);
    BranchingRatio.push_back(GetBR(i));
    if (histname=="") XSection.push_back(GetXsection(i));
    else XSection.push_back(GetXsection(i,histname));
  }

  TGraph* BranchGraph = new TGraph(Mass.size(),&Mass[0],&BranchingRatio[0]);
  TGraph* XSectionGraph = new TGraph(Mass.size(),&Mass[0],&XSection[0]);
  BranchGraph->SetTitle("Interpolated Branching Ratios");
  XSectionGraph->SetTitle("Interpolated Cross Sections");
  BranchGraph->SetMarkerStyle(20);
  XSectionGraph->SetMarkerStyle(20);
  BranchGraph->SetMarkerSize(1);
  XSectionGraph->SetMarkerSize(1);

  TCanvas* c1 = new TCanvas("c1","c1",800,650);
  c1->cd();
  BranchGraph->Draw("AP");
  c1->SaveAs("BranchingRatios.png");
  c1->Clear();
  XSectionGraph->Draw("AP");
  TString outfile = "XSections.png";
  if (histname!="") outfile.ReplaceAll(".png",histname.Append(".png"));
  c1->SaveAs(outfile.Data());

  delete BranchGraph;
  delete XSectionGraph;
  delete c1;

}