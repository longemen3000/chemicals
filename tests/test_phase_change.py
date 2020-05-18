# -*- coding: utf-8 -*-
'''Chemical Engineering Design Library (ChEDL). Utilities for process modeling.
Copyright (C) 2016, Caleb Bell <Caleb.Andrew.Bell@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''

import pytest

from fluids.numerics import assert_close, assert_close1d
from chemicals.phase_change import *
from chemicals.phase_change import CRCHvap_data, CRCHfus_data, GharagheiziHvap_data, GharagheiziHsub_data, Yaws_data, Tm_ON_data, Perrys2_150, Alibakhshi_Cs, VDI_PPDS_4
from chemicals.miscdata import CRC_inorganic_data, CRC_organic_data
from thermo.identifiers import checkCAS


def test_Watson():
    Hvap = Watson(T=320, Hvap_ref=43908, T_ref=300.0, Tc=647.14)
    assert_close(Hvap, 42928.990094915454, rtol=1e-12)


def test_Clapeyron():
    Hvap = Clapeyron(294.0, 466.0, 5.55E6)
    assert_close(Hvap, 26512.36357131963)

    # Test at 1/2 bar, sZ=0.98
    Hvap = Clapeyron(264.0, 466.0, 5.55E6, 0.98, 5E4)
    assert_close(Hvap, 23370.947571814384)

    
def test_Pitzer():
    Hvap = Pitzer(452, 645.6, 0.35017)
    assert_close(Hvap, 36696.749078320056)

    
def test_SMK():
    Hvap = SMK(553.15, 751.35, 0.302)
    assert_close(Hvap, 39866.18999046232)

    
def test_MK():
    # Problem in article for SMK function.
    Hv1 = MK(553.15, 751.35, 0.302)
    # data in [1]_., should give 26.43 KJ/mol
    Hv2 = MK(298.15, 469.69, 0.2507)
    assert_close(Hv1, 38728.00667307733, rtol=1e-12)
    assert_close(Hv2, 25940.988533726406, rtol=1e-12)

    
def test_Velasco():
    Hv1 = Velasco(553.15, 751.35, 0.302)
    Hv2 = Velasco(333.2, 476.0, 0.5559)
    assert_close(Hv1, 39524.251054691274, rtol=1e-12)
    assert_close(Hv2, 33299.428636069264, rtol=1e-12)


def test_Riedel():
    # same problem as in Perry's examples
    Hv1 = Riedel(294.0, 466.0, 5.55E6)
    # Pyridine, 0.0% err vs. exp: 35090 J/mol; from Poling [2]_.
    Hv2 = Riedel(388.4, 620.0, 56.3E5)
    assert_close(Hv1, 26828.59040728512, rtol=1e-12)
    assert_close(Hv2, 35089.80179000598, rtol=1e-12)

    
def test_Chen():
    Hv1 = Chen(294.0, 466.0, 5.55E6)
    assert_close(Hv1, 26705.902558030946)

    
def test_Liu():
    Hv1 = Liu(294.0, 466.0, 5.55E6)
    assert_close(Hv1, 26378.575260517395)

    
def test_Vetere():
    Hv1 = Vetere(294.0, 466.0, 5.55E6)
    assert_close(Hv1, 26363.43895706672)


def test_Hvap_CRC_data():

    HvapTb_tot = CRCHvap_data['HvapTb'].sum()
    assert_close(HvapTb_tot, 30251890.0)

    Hvap298_tot = CRCHvap_data['Hvap298'].sum()
    assert_close(Hvap298_tot, 29343710.0)

    Tb_tot = CRCHvap_data['Tb'].sum()
    assert_close(Tb_tot, 407502.95600000001)

    assert CRCHvap_data.index.is_unique
    assert CRCHvap_data.shape == (926, 5)

    assert all([checkCAS(i) for i in list(CRCHvap_data.index)])


def test_Hfus_CRC_data():
    Hfus_total = CRCHfus_data['Hfus'].sum()
    assert_close(Hfus_total, 29131241)
    assert CRCHfus_data.index.is_unique
    assert CRCHfus_data.shape == (1112, 3)

    assert all([checkCAS(i) for i in list(CRCHfus_data.index)])


def test_Hfus():
    assert_close(Hfus('462-06-6'), 11310.0, rtol=1e-12)
    assert_close(Hfus(CASRN='75-07-0'), 2310.0)
    assert Hfus(CASRN='75000-07-0') is None

def test_Gharagheizi_Hvap_data():
    # 51 CAS number DO NOT validate
    Hvap298_tot = GharagheiziHvap_data['Hvap298'].sum()
    assert_close(Hvap298_tot, 173584900)

    assert GharagheiziHvap_data.index.is_unique
    assert GharagheiziHvap_data.shape == (2730, 2)


def test_Gharagheizi_Hsub_data():
    tots = [GharagheiziHsub_data[i].sum() for i in ['Hsub', 'error']]
    assert_close(tots[0], 130537650)
    assert_close(tots[1], 1522960.0)

    assert GharagheiziHsub_data.index.is_unique
    assert GharagheiziHsub_data.shape == (1241, 3)


def test_Yaws_Tb_data():
    tot = Yaws_data.sum()
    assert_close(tot, 6631287.51)

    assert Yaws_data.index.is_unique
    assert Yaws_data.shape == (13461, 1)
    assert all([checkCAS(i) for i in Yaws_data.index])


def test_Tm_ON_data():
    tot = Tm_ON_data.sum()
    assert_close(tot, 4059989.425)

    assert Tm_ON_data.shape == (11549, 1)
    assert Tm_ON_data.index.is_unique
    assert all([checkCAS(i) for i in Tm_ON_data.index])

    
def test_Perrys2_312_data():
    # rtol=2E-4 for Tmin; only helium-4 needs a higher tolerance
    # Everything hits 0 at Tmax except Difluoromethane, methane, and water;
    # those needed their Tmax adjusted to their real Tc.
    # C1 is divided by 1000, to give units of J/mol instead of J/kmol
    # Terephthalic acid removed, was a constant value only.
    
    assert all([checkCAS(i) for i in Perrys2_150.index])
    tots_calc = [Perrys2_150[i].abs().sum() for i in [u'Tc', u'C1', u'C2', u'C3', u'C4', u'Tmin', u'Tmax']]
    tots = [189407.42499999999, 18617223.739999998, 174.34494000000001, 112.51209900000001, 63.894040000000004, 70810.849999999991, 189407.005]
    assert_close1d(tots_calc, tots)
    
    assert Perrys2_150.index.is_unique
    assert Perrys2_150.shape == (344, 8)


def test_Alibakhshi_Cs_data():
    # Oops, a bunch of these now-lonely coefficients have an invalid CAS...
#    assert all([checkCAS(i) for i in Alibakhshi_Cs.index])
    tots_calc = [Alibakhshi_Cs[i].abs().sum() for i in [u'C']]
    tots = [28154.361500000003]
    assert_close1d(tots_calc, tots)
    
    assert Alibakhshi_Cs.index.is_unique
    assert Alibakhshi_Cs.shape == (1890, 2)


def test_VDI_PPDS_4_data():
    '''I believe there are no errors here. 
    '''
    assert all([checkCAS(i) for i in VDI_PPDS_4.index])
    tots_calc = [VDI_PPDS_4[i].abs().sum() for i in [u'A', u'B', u'C', u'D', u'E', u'Tc', u'MW']]
    tots = [1974.2929800000002, 2653.9399000000003, 2022.530649, 943.25633100000005, 3124.9258610000002, 150142.28, 27786.919999999998]
    assert_close1d(tots_calc, tots)
    
    assert VDI_PPDS_4.index.is_unique
    assert VDI_PPDS_4.shape == (272, 8)


def test_Tb():
    # CRC_inorg, CRC org, Yaws
    Tbs_calc = Tb('993-50-0'), Tb('626-94-8'), Tb('7631-99-4')
    Tbs = [399.15, 412.15, 653.15]
    assert_close1d(Tbs, Tbs_calc)

    hits = [Tb(i, AvailableMethods=True) for i in ['993-50-0', '626-94-8', '7631-99-4']]
    assert hits == [['CRC_INORG', 'NONE'], ['CRC_ORG', 'NONE'], ['YAWS', 'NONE']]

    s1 = CRC_inorganic_data.loc[CRC_inorganic_data['Tb'].notnull()].index
    s2 = CRC_organic_data.loc[CRC_organic_data['Tb'].notnull()].index
    s3 = Yaws_data.index

    tots = []
    tots_exp = [639213.2310000042, 2280667.079999829, 6631287.510000873]
    # These should match the sums of the respective series
    for s, method in zip([s1, s2, s3], ['CRC_INORG', 'CRC_ORG', 'YAWS']):
        tots.append(sum([Tb(i, Method=method) for i in s]))
    assert_close1d(tots, tots_exp)

    with pytest.raises(Exception):
        Tb('993-50-0', Method='BADMETHOD')

    assert None == Tb('9923443-50-0')
    assert ['NONE'] == Tb('9923443-50-0', AvailableMethods=True)

    s = set(); s.update(s1); s.update(s2); s.update(s3)

    w_methods = Tb('7732-18-5', AvailableMethods=True, IgnoreMethods=[])
    assert w_methods == ['CRC_INORG', 'YAWS', 'NONE']

    Tbs = [Tb('7732-18-5', Method=i) for i in w_methods]
    assert_close1d(Tbs[0:-1], [373.124, 373.15])

    assert None == Tb('7732-18-5', IgnoreMethods=['CRC_ORG', 'CRC_INORG', 'YAWS'])



def test_Tm():
    # Open notebook, CRC organic, CRC inorg
    Tms_calc = Tm('996-50-9'), Tm('999-78-0'), Tm('993-50-0')
    Tms = [263.15, 191.15, 274.15]
    assert_close1d(Tms, Tms_calc)

    hits = [Tm(i, AvailableMethods=True) for i in ['996-50-9', '999-78-0', '993-50-0']]
    assert hits == [['OPEN_NTBKM', 'NONE'], ['CRC_ORG', 'NONE'], ['CRC_INORG', 'NONE']]


    s1 = CRC_inorganic_data.loc[CRC_inorganic_data['Tm'].notnull()].index
    s2 = CRC_organic_data.loc[CRC_organic_data['Tm'].notnull()].index
    s3 = Tm_ON_data.index
    tots = []
    tots_exp = [1543322.6125999668, 2571284.480399755, 4059989.4249993376]
    # These should match the sums of the respective series
    for s, method in zip([s1, s2, s3], ['CRC_INORG', 'CRC_ORG', 'OPEN_NTBKM']):
        tots.append(sum([Tm(i, Method=method) for i in s]))
    assert_close1d(tots, tots_exp)

    with pytest.raises(Exception):
        Tm('993-50-0', Method='BADMETHOD')

    assert None == Tm('9923443-50-0')
    assert ['NONE'] == Tm('9923443-50-0', AvailableMethods=True)


    w_methods = Tm('7732-18-5', AvailableMethods=True)
    assert w_methods == ['OPEN_NTBKM', 'CRC_INORG', 'NONE']

    Tms = [Tm('7732-18-5', Method=i) for i in w_methods]
    assert_close1d(Tms[0:-1], [273.15, 273.15])

    assert None == Tm('7732-18-5', IgnoreMethods=['CRC_ORG', 'CRC_INORG', 'OPEN_NTBKM'])
