#Modul rumus-rumus perhitungan survey deviasi
#5-4-2020, by Asep Hermawan

from math import *

#end function CalculateSurvey
def FDL(INC0, AZI0, INC1, AZI1):
    DL = acos((cos((INC1+0.000001 - INC0) * pi / 180) - sin(INC0 * pi / 180) * sin((INC1+0.000001) * pi / 180) * (1 - cos((AZI1+0.000001 - AZI0) * pi / 180))))
    DL = DL * 180 / pi
    return DL

def FRF(DL):
    aFRF = (360 / (DL * pi)) * (1 - cos(DL * pi / 180)) / sin(DL * pi / 180)
    return aFRF

def FDepthTVD(MD0, INC0, AZI0, TVD0, DepthMD, INC1, AZI1):
    DL = FDL(INC0, AZI0, INC1, AZI1)
    RF = FRF(DL)
    aFDepthTVD = TVD0 + 0.5 * (DepthMD - MD0) * (cos(INC0 * pi / 180) + cos(INC1 * pi / 180)) * RF
    return aFDepthTVD

def FVertSection(AZVS, EW, NS):
    aFVertSection = cos(AZVS * pi / 180) * (tan(AZVS * pi / 180) * EW + NS)
    return aFVertSection

def FNorthing(MD0, INC0, AZI0, Northing0, DepthMD, INC1, AZI1):
    DL = FDL(INC0, AZI0, INC1, AZI1)
    RF = FRF(DL)
    aFNorthing = Northing0 + 0.5 * (DepthMD - MD0) * (sin(INC0 * pi / 180) * cos(AZI0 * pi / 180) + sin(INC1 * pi / 180) * cos(AZI1 * pi / 180)) * RF
    return aFNorthing

def FEasting(MD0, INC0, AZI0, Easting0, DepthMD, INC1, AZI1):
    DL = FDL(INC0, AZI0, INC1, AZI1)
    RF = FRF(DL)
    aFEasting = Easting0 + 0.5 * (DepthMD - MD0) * (sin(INC0 * pi / 180) * sin(AZI0 * pi / 180) + sin(INC1 * pi / 180) * sin(AZI1 * pi / 180)) * RF
    return aFEasting

def ClosureAz(EW, NS):
    if NS == 0 :
        NS = 1
    ClosAz = atan(EW / NS)
    ClosAz = ClosAz * 180 / pi
    if (EW > 0) and (NS < 0) :
        ClosAz = 180 + ClosAz
    elif (EW < 0) and (NS < 0):
        ClosAz = 180 + ClosAz
    elif (EW < 0) and (NS > 0) :
        ClosAz = 360 + ClosAz
    return ClosAz
