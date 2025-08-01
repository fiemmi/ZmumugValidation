#!/usr/bin/python
import argparse
import os
import math
import sys
from array import array
from ROOT import *
import numpy as np

def delta_phi(phi1, phi2):
  dphi = phi1 - phi2
  while dphi > math.pi:
      dphi -= 2 * math.pi
  while dphi <= -math.pi:
      dphi += 2 * math.pi
  return dphi
    
def E(m,pt,eta): 
  return np.sqrt( (pt*np.cosh(eta))**2 + m**2 )
  
def px(pt, phi): 
  return pt * np.cos(phi)
  
def py(pt, phi): 
  return pt * np.sin(phi)
  
def pz(pt, eta): 
  return pt * np.sinh(eta)
  
def dM_dcorr(particles,x,y,z,w,nParticles=3):
  
  # Unpack particles
  m = [p[0] for p in particles]
  pT = [p[1] for p in particles]
  eta = [p[2] for p in particles]
  phi = [p[3] for p in particles]

  E1 = 0.
  px1 = 0.
  py1 = 0.
  pz1 = 0.
  E2 = 0.
  px2 = 0.
  py2 = 0.
  pz2 = 0.
  E3 = 0.
  px3 = 0.
  py3 = 0.
  pz3 = 0.
  if nParticles==3:
    #print("m = ",m[0]," - pT = ",pT[0]," - eta = ",eta[0])
    E1 = E(m[0],pT[0]*x*y,eta[0])
    px1 = px(pT[0]*x*y, phi[0]) 
    py1 = py(pT[0]*x*y, phi[0])
    pz1 = pz(pT[0]*x*y, eta[0])  
    E2 = E(m[1],pT[1]*z,eta[1])
    px2 = px(pT[1]*z, phi[1]) 
    py2 = py(pT[1]*z, phi[1]) 
    pz2 = pz(pT[1]*z, eta[1])
    E3 = E(m[2],pT[2]*w,eta[2])
    px3 = px(pT[2]*w, phi[2]) 
    py3 = py(pT[2]*w, phi[2]) 
    pz3 = pz(pT[2]*w, eta[2]) 
  else:   
    E1 = E(m[0],pT[0]*x,eta[0])
    px1 = px(pT[0]*x, phi[0]) 
    py1 = py(pT[0]*x, phi[0])
    pz1 = pz(pT[0]*x, eta[0])  
    E2 = E(m[1],pT[1]*y,eta[1])
    px2 = px(pT[1]*y, phi[1]) 
    py2 = py(pT[1]*y, phi[1]) 
    pz2 = pz(pT[1]*y, eta[1])
    
  # Total momenta
  px_tot = 0.
  py_tot = 0.
  pz_tot = 0.
  E_tot = 0.
  if nParticles==3:
    px_tot = px1 + px2 + px3
    py_tot = py1 + py2 + py3
    pz_tot = pz1 + pz2 + pz3
    E_tot = E1 + E2 + E3
  else:
    px_tot = px1 + px2
    py_tot = py1 + py2 
    pz_tot = pz1 + pz2 
    E_tot = E1 + E2 
    
  M = np.sqrt( E_tot**2 - (px_tot**2 + py_tot**2 + pz_tot**2) )
  
  dm_dx = 0.
  dm_dy = 0.
  dm_dz = 0.
  dm_dw = 0.
  if nParticles==3:
    dm_dx = ( E_tot/E1*(pT[0]*y*np.cosh(eta[0]))**2 * x - pT[0]*y*( px_tot*np.cos(phi[0]) + py_tot*np.sin(phi[0]) + pz_tot*np.sinh(eta[0]) ) )/M
    dm_dy = ( E_tot/E1*(pT[0]*x*np.cosh(eta[0]))**2 * y - pT[0]*x*( px_tot*np.cos(phi[0]) + py_tot*np.sin(phi[0]) + pz_tot*np.sinh(eta[0]) ) )/M
    dm_dz = ( E_tot/E2*(pT[1]*np.cosh(eta[1]))**2   * z - pT[1] * ( px_tot*np.cos(phi[1]) + py_tot*np.sin(phi[1]) + pz_tot*np.sinh(eta[1]) ) )/M
    dm_dw = ( E_tot/E3*(pT[2]*np.cosh(eta[2]))**2   * w - pT[2] * ( px_tot*np.cos(phi[2]) + py_tot*np.sin(phi[2]) + pz_tot*np.sinh(eta[2]) ) )/M
  else:
    dm_dx = ( E_tot/E1*(pT[0]*np.cosh(eta[0]))**2   * x - pT[0] * ( px_tot*np.cos(phi[0]) + py_tot*np.sin(phi[0]) + pz_tot*np.sinh(eta[0]) ) )/M
    dm_dy = ( E_tot/E2*(pT[1]*np.cosh(eta[1]))**2   * y - pT[1] * ( px_tot*np.cos(phi[1]) + py_tot*np.sin(phi[1]) + pz_tot*np.sinh(eta[1]) ) )/M
    
  output = []
  if nParticles==3:
    output = [dm_dx,dm_dy,dm_dz,dm_dw]   
  else:  
    output = [dm_dx,dm_dy] 
      
  return output      

def getVal(tree,var):

  val = -999.
  if(var=='runId'): val = tree.event_RunID
  if(var=='pho_energy'): val = tree.pho_energy
  if(var=='pho_EnergyScaleFactorEG'): val = tree.pho_EnergyScaleFactorEG
  if(var=='pho_EnergyScaleFactorEGErr'): val = tree.pho_EnergyScaleFactorEGErr
  if(var=='pho_EnergySmearingSigmaEG'): val = tree.pho_EnergySmearingSigmaEG
  if(var=='pho_energySmeared'): val = tree.pho_energySmeared
  if(var=='pho_energySmeared_1sig'): val = tree.pho_energySmeared_1sig
  if(var=='pho_energySmeared_m1sig'): val = tree.pho_energySmeared_m1sig
  if(var=='pho_energy_ScaleSmeared'): val = tree.pho_energy_ScaleSmeared
  if(var=='pho_pt'): val = tree.pho_pt 
  if(var=='pho_pt_ScaleSmeared'): val = tree.pho_pt_ScaleSmeared 
  if(var=='pho_eta'): val = tree.pho_eta  
  if(var=='pho_sceta'): val = tree.pho_sceta
  if(var=='pho_full5x5_r9Corr'): val = tree.pho_full5x5_r9Corr
  if(var=='pho_phi'): val = tree.pho_phi  
  if(var=='pho_scphi'): val = tree.pho_scphi
  if(var=='muNear_pt'): val = tree.muNear_pt
  if(var=='muNear_eta'): val = tree.muNear_eta
  if(var=='muNear_phi'): val = tree.muNear_phi
  if(var=='muNear_RocCorSF'): val = tree.muNear_RocCorSF
  if(var=='muNear_RocCorSFerr'): val = tree.muNear_RocCorSFerr
  if(var=='muFar_pt'): val = tree.muFar_pt
  if(var=='muFar_eta'): val = tree.muFar_eta
  if(var=='muFar_phi'): val = tree.muFar_phi
  if(var=='muFar_RocCorSF'): val = tree.muFar_RocCorSF
  if(var=='muFar_RocCorSFerr'): val = tree.muFar_RocCorSFerr
  if(var=='dimu_mass'): val = tree.dimu_mass
  if(var=='dimu_massRaw'): val = tree.dimu_massRaw
  if(var=='dimu_mass_1sigmaUpMuRoc'): val = tree.dimu_mass_1sigmaUpMuRoc
  if(var=='dimu_mass_1sigmaDnMuRoc'): val = tree.dimu_mass_1sigmaDnMuRoc
  if(var=='dimu_pt'): val = tree.dimu_pt
  if(var=='dimu_eta'): val = tree.dimu_eta
  if(var=='dimu_phi'): val = tree.dimu_phi
  if(var=='mass_ScaleSmeared'): val = tree.mass_ScaleSmeared
  if(var=='mass_ScaleSmeared_1sigmaUpSmear'): val = tree.mass_ScaleSmeared_1sigmaUpSmear
  if(var=='mass_ScaleSmeared_1sigmaDnSmear'): val = tree.mass_ScaleSmeared_1sigmaDnSmear
  if(var=='mass_ScaleSmeared_1sigmaUpScale'): val = tree.mass_ScaleSmeared_1sigmaUpScale
  if(var=='mass_ScaleSmeared_1sigmaDnScale'): val = tree.mass_ScaleSmeared_1sigmaDnScale
  if(var=='mass_ScaleSmeared_1sigmaUpMuRoc'): val = tree.mass_ScaleSmeared_1sigmaUpMuRoc
  if(var=='mass_ScaleSmeared_1sigmaDnMuRoc'): val = tree.mass_ScaleSmeared_1sigmaDnMuRoc

  #else: print 'getVal --. WARNING MISSING VAR: ',var
  if val<=-998.:
    print("getVal: WARNING MISSING VAR -->",var+" = "+str(val))

  return val

def getRing(eta):
  eta = abs(eta)
  iRing = int(eta*10)
  if eta<1.479 and iRing>14: iRing = 14
  if eta>1.479 and iRing<15: iRing = 15
  if iRing>29: iRing = 29
  return iRing

def getFNUF(lumi,energy,iRing,F_correction):
 relUncertainty_EB = 0.2
 relUncertainty_EE = 0.35
 corr = 1.;
 corrErrUp = 0. 
 corrErrDown = 0. 

 corr = F_correction.Interpolate(energy,lumi) 
 if corr<=0. or corr>1.: 
   corr = 1.
   print("WARNING: corr = 0 --> lumi = "+str(lumi)+" - energy = "+str(energy)+" - iRing = "+str(iRing))

 if abs(iRing)<15: 
   corrErrUp = (1.-corr) * relUncertainty_EB 
   corrErrDown = (1.-corr) * relUncertainty_EB  
 else:
   corrErrUp = (1.-corr) * relUncertainty_EE 
   corrErrDown = (1.-corr) * relUncertainty_EE  
  
 return [corr,corrErrUp,corrErrDown]  

def addBranches(tree,mc):

 copyTree = tree.CopyTree('')
 copyTree.SetBranchStatus('*',1)
 
 muNear_energyRaw = array( 'd', [ -999. ] ) 
 muNear_energy = array( 'd', [ -999. ] ) 
 muNear_energy_1sigmaUpMuRoc = array( 'd', [ -999. ] ) 
 muNear_energy_1sigmaDnMuRoc = array( 'd', [ -999. ] ) 
 muNear_ptRaw = array( 'd', [ -999. ] ) 
 muNear_pt_1sigmaUpMuRoc = array( 'd', [ -999. ] ) 
 muNear_pt_1sigmaDnMuRoc = array( 'd', [ -999. ] ) 
 muFar_energyRaw = array( 'd', [ -999. ] ) 
 muFar_energy = array( 'd', [ -999. ] ) 
 muFar_energy_1sigmaUpMuRoc = array( 'd', [ -999. ] ) 
 muFar_energy_1sigmaDnMuRoc = array( 'd', [ -999. ] ) 
 muFar_ptRaw = array( 'd', [ -999. ] ) 
 muFar_pt_1sigmaUpMuRoc = array( 'd', [ -999. ] ) 
 muFar_pt_1sigmaDnMuRoc = array( 'd', [ -999. ] ) 
 dimu_energyRaw = array( 'd', [ -999. ] )
 dimu_energy = array( 'd', [ -999. ] ) 
 dimu_energy_1sigmaUpMuRoc = array( 'd', [ -999. ] )
 dimu_energy_1sigmaDnMuRoc = array( 'd', [ -999. ] )
 dimu_ptRaw = array( 'd', [ -999. ] )
 dimu_pt_1sigmaUpMuRoc = array( 'd', [ -999. ] )
 dimu_pt_1sigmaDnMuRoc = array( 'd', [ -999. ] )
 dimu_mass_errMuRocFullPropagation = array( 'd', [ -999. ] )
 dimu_mass_1SigmaUpErrMuRocFullPropagation = array( 'd', [ -999. ] )
 dimu_mass_1SigmaDnErrMuRocFullPropagation = array( 'd', [ -999. ] )
 pho_FnufCorr = array( 'd', [ -999. ] ) 
 pho_FnufCorrErr = array( 'd', [ -999. ] ) 
 pho_energy_ScaleSmeared_FnufCorrected = array( 'd', [ -999. ] )
 pho_energy_ScaleSmeared_FnufCorrected_1sigmaUpFnuf = array( 'd', [ -999. ] )
 pho_energy_ScaleSmeared_FnufCorrected_1sigmaDnFnuf = array( 'd', [ -999. ] )
 pho_pt_ScaleSmeared_FnufCorrected = array( 'd', [ -999. ] )
 pho_pt_ScaleSmeared_FnufCorrected_1sigmaUpFnuf = array( 'd', [ -999. ] )
 pho_pt_ScaleSmeared_FnufCorrected_1sigmaDnFnuf = array( 'd', [ -999. ] )
 mass_ScaleSmeared_FnufCorrected_errFullPropagNoSmear = array( 'd', [ -999. ] )
 mass_ScaleSmeared_FnufCorrected_errFnufFullPropagation = array( 'd', [ -999. ] )
 mass_ScaleSmeared_FnufCorrected_errScaleFullPropagation = array( 'd', [ -999. ] )
 mass_ScaleSmeared_FnufCorrected_errMuRocFullPropagation = array( 'd', [ -999. ] )
 mass_ScaleSmeared_allUp = array( 'd', [ -999. ] ) 
 mass_ScaleSmeared_allDown = array( 'd', [ -999. ] ) 
 mass_ScaleSmeared_FnufCorrected = array( 'd', [ -999. ] ) 
 mass_ScaleSmeared_FnufCorrected_approx = array( 'd', [ -999. ] ) 
 mass_ScaleSmeared_FnufCorrected_allUp = array( 'd', [ -999. ] ) 
 mass_ScaleSmeared_FnufCorrected_allDown = array( 'd', [ -999. ] )  
 mass_ScaleSmeared_FnufCorrected_1sigmaUpFnuf = array( 'd', [ -999. ] ) 
 mass_ScaleSmeared_FnufCorrected_1sigmaDnFnuf = array( 'd', [ -999. ] )  
 mass_ScaleSmeared_FnufCorrected_1sigmaUpSmear = array( 'd', [ -999. ] ) 
 mass_ScaleSmeared_FnufCorrected_1sigmaDnSmear = array( 'd', [ -999. ] )  
 mass_ScaleSmeared_FnufCorrected_1sigmaUpScale = array( 'd', [ -999. ] ) 
 mass_ScaleSmeared_FnufCorrected_1sigmaDnScale = array( 'd', [ -999. ] )  
 mass_ScaleSmeared_FnufCorrected_1sigmaUpMuRoc = array( 'd', [ -999. ] ) 
 mass_ScaleSmeared_FnufCorrected_1sigmaDnMuRoc = array( 'd', [ -999. ] )  
 mass_ScaleSmeared_FnufCorrected_1SigmaUpErrFullPropagNoSmear = array( 'd', [ -999. ] ) 
 mass_ScaleSmeared_FnufCorrected_1SigmaDnErrFullPropagNoSmear = array( 'd', [ -999. ] ) 
 mass_ScaleSmeared_FnufCorrected_1SigmaUpFnufFullPropagation = array( 'd', [ -999. ] ) 
 mass_ScaleSmeared_FnufCorrected_1SigmaDnFnufFullPropagation = array( 'd', [ -999. ] ) 
 mass_ScaleSmeared_FnufCorrected_1SigmaUpScaleFullPropagation = array( 'd', [ -999. ] ) 
 mass_ScaleSmeared_FnufCorrected_1SigmaDnScaleFullPropagation = array( 'd', [ -999. ] ) 
 mass_ScaleSmeared_FnufCorrected_1SigmaUpMuRocFullPropagation = array( 'd', [ -999. ] ) 
 mass_ScaleSmeared_FnufCorrected_1SigmaDnMuRocFullPropagation = array( 'd', [ -999. ] ) 

 muNear_energyRaw_branch = copyTree.Branch('muNear_energyRaw', muNear_energyRaw, 'muNear_energyRaw/D') 
 muNear_energy_branch = copyTree.Branch('muNear_energy', muNear_energy, 'muNear_energy/D') 
 muNear_energy_1sigmaUpMuRoc_branch = copyTree.Branch('muNear_energy_1sigmaUpMuRoc', muNear_energy_1sigmaUpMuRoc, 'muNear_energy_1sigmaUpMuRoc/D') 
 muNear_energy_1sigmaDnMuRoc_branch = copyTree.Branch('muNear_energy_1sigmaDnMuRoc', muNear_energy_1sigmaDnMuRoc, 'muNear_energy_1sigmaDnMuRoc/D') 
 muNear_ptRaw_branch = copyTree.Branch('muNear_ptRaw', muNear_ptRaw, 'muNear_ptRaw/D') 
 muNear_pt_1sigmaUpMuRoc_branch = copyTree.Branch('muNear_pt_1sigmaUpMuRoc', muNear_pt_1sigmaUpMuRoc, 'muNear_pt_1sigmaUpMuRoc/D') 
 muNear_pt_1sigmaDnMuRoc_branch = copyTree.Branch('muNear_pt_1sigmaDnMuRoc', muNear_pt_1sigmaDnMuRoc, 'muNear_pt_1sigmaDnMuRoc/D') 
 muFar_energyRaw_branch = copyTree.Branch('muFar_energyRaw', muFar_energyRaw, 'muFar_energyRaw/D') 
 muFar_energy_branch = copyTree.Branch('muFar_energy', muFar_energy, 'muFar_energy/D') 
 muFar_energy_1sigmaUpMuRoc_branch = copyTree.Branch('muFar_energy_1sigmaUpMuRoc', muFar_energy_1sigmaUpMuRoc, 'muFar_energy_1sigmaUpMuRoc/D') 
 muFar_energy_1sigmaDnMuRoc_branch = copyTree.Branch('muFar_energy_1sigmaDnMuRoc', muFar_energy_1sigmaDnMuRoc, 'muFar_energy_1sigmaDnMuRoc/D') 
 muFar_ptRaw_branch = copyTree.Branch('muFar_ptRaw', muFar_ptRaw, 'muFar_ptRaw/D') 
 muFar_pt_1sigmaUpMuRoc_branch = copyTree.Branch('muFar_pt_1sigmaUpMuRoc', muFar_pt_1sigmaUpMuRoc, 'muFar_pt_1sigmaUpMuRoc/D') 
 muFar_pt_1sigmaDnMuRoc_branch = copyTree.Branch('muFar_pt_1sigmaDnMuRoc', muFar_pt_1sigmaDnMuRoc, 'muFar_pt_1sigmaDnMuRoc/D') 
 dimu_energyRaw_branch = copyTree.Branch('dimu_energyRaw', dimu_energyRaw, 'dimu_energyRaw/D') 
 dimu_energy_branch = copyTree.Branch('dimu_energy', dimu_energy, 'dimu_energy/D') 
 dimu_energy_1sigmaUpMuRoc_branch = copyTree.Branch('dimu_energy_1sigmaUpMuRoc', dimu_energy_1sigmaUpMuRoc, 'dimu_energy_1sigmaUpMuRoc/D') 
 dimu_energy_1sigmaDnMuRoc_branch = copyTree.Branch('dimu_energy_1sigmaDnMuRoc', dimu_energy_1sigmaDnMuRoc, 'dimu_energy_1sigmaDnMuRoc/D') 
 dimu_ptRaw_branch = copyTree.Branch('dimu_ptRaw', dimu_ptRaw, 'dimu_ptRaw/D') 
 dimu_pt_1sigmaUpMuRoc_branch = copyTree.Branch('dimu_pt_1sigmaUpMuRoc', dimu_pt_1sigmaUpMuRoc, 'dimu_pt_1sigmaUpMuRoc/D') 
 dimu_pt_1sigmaDnMuRoc_branch = copyTree.Branch('dimu_pt_1sigmaDnMuRoc', dimu_pt_1sigmaDnMuRoc, 'dimu_pt_1sigmaDnMuRoc/D') 
 dimu_mass_errMuRocFullPropagation_branch = copyTree.Branch('dimu_mass_errMuRocFullPropagation', dimu_mass_errMuRocFullPropagation, 'dimu_mass_errMuRocFullPropagation/D') 
 dimu_mass_1SigmaUpErrMuRocFullPropagation_branch = copyTree.Branch('dimu_mass_1SigmaUpErrMuRocFullPropagation', dimu_mass_1SigmaUpErrMuRocFullPropagation, 'dimu_mass_1SigmaUpErrMuRocFullPropagation/D') 
 dimu_mass_1SigmaDnErrMuRocFullPropagation_branch = copyTree.Branch('dimu_mass_1SigmaDnErrMuRocFullPropagation', dimu_mass_1SigmaDnErrMuRocFullPropagation, 'dimu_mass_1SigmaDnErrMuRocFullPropagation/D') 
 pho_FnufCorr_branch = copyTree.Branch('pho_FnufCorr', pho_FnufCorr, 'pho_FnufCorr/D')
 pho_FnufCorrErr_branch = copyTree.Branch('pho_FnufCorrErr', pho_FnufCorrErr, 'pho_FnufCorrErr/D')
 pho_energy_ScaleSmeared_FnufCorrected_branch = copyTree.Branch('pho_energy_ScaleSmeared_FnufCorrected', pho_energy_ScaleSmeared_FnufCorrected, 'pho_energy_ScaleSmeared_FnufCorrected/D')
 pho_energy_ScaleSmeared_FnufCorrected_1sigmaUpFnuf_branch = copyTree.Branch('pho_energy_ScaleSmeared_FnufCorrected_1sigmaUpFnuf', pho_energy_ScaleSmeared_FnufCorrected_1sigmaUpFnuf, 'pho_energy_ScaleSmeared_FnufCorrected_1sigmaUpFnuf/D')
 pho_energy_ScaleSmeared_FnufCorrected_1sigmaDnFnuf_branch = copyTree.Branch('pho_energy_ScaleSmeared_FnufCorrected_1sigmaDnFnuf', pho_energy_ScaleSmeared_FnufCorrected_1sigmaDnFnuf, 'pho_energy_ScaleSmeared_FnufCorrected_1sigmaDnFnuf/D')
 pho_pt_ScaleSmeared_FnufCorrected_branch = copyTree.Branch('pho_pt_ScaleSmeared_FnufCorrected', pho_pt_ScaleSmeared_FnufCorrected, 'pho_pt_ScaleSmeared_FnufCorrected/D')
 pho_pt_ScaleSmeared_FnufCorrected_1sigmaUpFnuf_branch = copyTree.Branch('pho_pt_ScaleSmeared_FnufCorrected_1sigmaUpFnuf', pho_pt_ScaleSmeared_FnufCorrected_1sigmaUpFnuf, 'pho_pt_ScaleSmeared_FnufCorrected_1sigmaUpFnuf/D')
 pho_pt_ScaleSmeared_FnufCorrected_1sigmaDnFnuf_branch = copyTree.Branch('pho_pt_ScaleSmeared_FnufCorrected_1sigmaDnFnuf', pho_pt_ScaleSmeared_FnufCorrected_1sigmaDnFnuf, 'pho_pt_ScaleSmeared_FnufCorrected_1sigmaDnFnuf/D')
 mass_ScaleSmeared_FnufCorrected_errFullPropagNoSmear_branch = copyTree.Branch('mass_ScaleSmeared_FnufCorrected_errFullPropagNoSmear', mass_ScaleSmeared_FnufCorrected_errFullPropagNoSmear, 'mass_ScaleSmeared_FnufCorrected_errFullPropagNoSmear/D')
 mass_ScaleSmeared_FnufCorrected_errFnufFullPropagation_branch = copyTree.Branch('mass_ScaleSmeared_FnufCorrected_errFnufFullPropagation', mass_ScaleSmeared_FnufCorrected_errFnufFullPropagation, 'mass_ScaleSmeared_FnufCorrected_errFnufFullPropagation/D')
 mass_ScaleSmeared_FnufCorrected_errScaleFullPropagation_branch = copyTree.Branch('mass_ScaleSmeared_FnufCorrected_errScaleFullPropagation', mass_ScaleSmeared_FnufCorrected_errScaleFullPropagation, 'mass_ScaleSmeared_FnufCorrected_errScaleFullPropagation/D')
 mass_ScaleSmeared_FnufCorrected_errMuRocFullPropagation_branch = copyTree.Branch('mass_ScaleSmeared_FnufCorrected_errMuRocFullPropagation', mass_ScaleSmeared_FnufCorrected_errMuRocFullPropagation, 'mass_ScaleSmeared_FnufCorrected_errMuRocFullPropagation/D')
 mass_ScaleSmeared_allUp_branch = copyTree.Branch('mass_ScaleSmeared_allUp', mass_ScaleSmeared_allUp, 'mass_ScaleSmeared_allUp/D') 
 mass_ScaleSmeared_allDown_branch = copyTree.Branch('mass_ScaleSmeared_allDown', mass_ScaleSmeared_allDown, 'mass_ScaleSmeared_allDown/D') 
 mass_ScaleSmeared_FnufCorrected_branch = copyTree.Branch('mass_ScaleSmeared_FnufCorrected', mass_ScaleSmeared_FnufCorrected, 'mass_ScaleSmeared_FnufCorrected/D')
 mass_ScaleSmeared_FnufCorrected_approx_branch = copyTree.Branch('mass_ScaleSmeared_FnufCorrected_approx', mass_ScaleSmeared_FnufCorrected_approx, 'mass_ScaleSmeared_FnufCorrected_approx/D')
 mass_ScaleSmeared_FnufCorrected_allUp_branch = copyTree.Branch('mass_ScaleSmeared_FnufCorrected_allUp', mass_ScaleSmeared_FnufCorrected_allUp, 'mass_ScaleSmeared_FnufCorrected_allUp/D')
 mass_ScaleSmeared_FnufCorrected_allDown_branch = copyTree.Branch('mass_ScaleSmeared_FnufCorrected_allDown', mass_ScaleSmeared_FnufCorrected_allDown, 'mass_ScaleSmeared_FnufCorrected_allDown/D')
 mass_ScaleSmeared_FnufCorrected_1sigmaUpFnuf_branch = copyTree.Branch('mass_ScaleSmeared_FnufCorrected_1sigmaUpFnuf', mass_ScaleSmeared_FnufCorrected_1sigmaUpFnuf, 'mass_ScaleSmeared_FnufCorrected_1sigmaUpFnuf/D')
 mass_ScaleSmeared_FnufCorrected_1sigmaDnFnuf_branch = copyTree.Branch('mass_ScaleSmeared_FnufCorrected_1sigmaDnFnuf', mass_ScaleSmeared_FnufCorrected_1sigmaDnFnuf, 'mass_ScaleSmeared_FnufCorrected_1sigmaDnFnuf/D')
 mass_ScaleSmeared_FnufCorrected_1sigmaUpSmear_branch = copyTree.Branch('mass_ScaleSmeared_FnufCorrected_1sigmaUpSmear', mass_ScaleSmeared_FnufCorrected_1sigmaUpSmear, 'mass_ScaleSmeared_FnufCorrected_1sigmaUpSmear/D')
 mass_ScaleSmeared_FnufCorrected_1sigmaDnSmear_branch = copyTree.Branch('mass_ScaleSmeared_FnufCorrected_1sigmaDnSmear', mass_ScaleSmeared_FnufCorrected_1sigmaDnSmear, 'mass_ScaleSmeared_FnufCorrected_1sigmaDnSmear/D')
 mass_ScaleSmeared_FnufCorrected_1sigmaUpScale_branch = copyTree.Branch('mass_ScaleSmeared_FnufCorrected_1sigmaUpScale', mass_ScaleSmeared_FnufCorrected_1sigmaUpScale, 'mass_ScaleSmeared_FnufCorrected_1sigmaUpScale/D')
 mass_ScaleSmeared_FnufCorrected_1sigmaDnScale_branch = copyTree.Branch('mass_ScaleSmeared_FnufCorrected_1sigmaDnScale', mass_ScaleSmeared_FnufCorrected_1sigmaDnScale, 'mass_ScaleSmeared_FnufCorrected_1sigmaDnScale/D')
 mass_ScaleSmeared_FnufCorrected_1sigmaUpMuRoc_branch = copyTree.Branch('mass_ScaleSmeared_FnufCorrected_1sigmaUpMuRoc', mass_ScaleSmeared_FnufCorrected_1sigmaUpMuRoc, 'mass_ScaleSmeared_FnufCorrected_1sigmaUpMuRoc/D')
 mass_ScaleSmeared_FnufCorrected_1sigmaDnMuRoc_branch = copyTree.Branch('mass_ScaleSmeared_FnufCorrected_1sigmaDnMuRoc', mass_ScaleSmeared_FnufCorrected_1sigmaDnMuRoc, 'mass_ScaleSmeared_FnufCorrected_1sigmaDnMuRoc/D')
 mass_ScaleSmeared_FnufCorrected_1SigmaUpErrFullPropagNoSmear_branch = copyTree.Branch('mass_ScaleSmeared_FnufCorrected_1SigmaUpErrFullPropagNoSmear', mass_ScaleSmeared_FnufCorrected_1SigmaUpErrFullPropagNoSmear, 'mass_ScaleSmeared_FnufCorrected_1SigmaUpErrFullPropagNoSmear/D')
 mass_ScaleSmeared_FnufCorrected_1SigmaDnErrFullPropagNoSmear_branch = copyTree.Branch('mass_ScaleSmeared_FnufCorrected_1SigmaDnErrFullPropagNoSmear', mass_ScaleSmeared_FnufCorrected_1SigmaDnErrFullPropagNoSmear, 'mass_ScaleSmeared_FnufCorrected_1SigmaDnErrFullPropagNoSmear/D')
 mass_ScaleSmeared_FnufCorrected_1SigmaUpFnufFullPropagation_branch = copyTree.Branch('mass_ScaleSmeared_FnufCorrected_1SigmaUpFnufFullPropagation', mass_ScaleSmeared_FnufCorrected_1SigmaUpFnufFullPropagation, 'mass_ScaleSmeared_FnufCorrected_1SigmaUpFnufFullPropagation/D')
 mass_ScaleSmeared_FnufCorrected_1SigmaDnFnufFullPropagation_branch = copyTree.Branch('mass_ScaleSmeared_FnufCorrected_1SigmaDnFnufFullPropagation', mass_ScaleSmeared_FnufCorrected_1SigmaDnFnufFullPropagation, 'mass_ScaleSmeared_FnufCorrected_1SigmaDnFnufFullPropagation/D')
 mass_ScaleSmeared_FnufCorrected_1SigmaUpScaleFullPropagation_branch = copyTree.Branch('mass_ScaleSmeared_FnufCorrected_1SigmaUpScaleFullPropagation', mass_ScaleSmeared_FnufCorrected_1SigmaUpScaleFullPropagation, 'mass_ScaleSmeared_FnufCorrected_1SigmaUpScaleFullPropagation/D')
 mass_ScaleSmeared_FnufCorrected_1SigmaDnScaleFullPropagation_branch = copyTree.Branch('mass_ScaleSmeared_FnufCorrected_1SigmaDnScaleFullPropagation', mass_ScaleSmeared_FnufCorrected_1SigmaDnScaleFullPropagation, 'mass_ScaleSmeared_FnufCorrected_1SigmaDnScaleFullPropagation/D')
 mass_ScaleSmeared_FnufCorrected_1SigmaUpMuRocFullPropagation_branch = copyTree.Branch('mass_ScaleSmeared_FnufCorrected_1SigmaUpMuRocFullPropagation', mass_ScaleSmeared_FnufCorrected_1SigmaUpMuRocFullPropagation, 'mass_ScaleSmeared_FnufCorrected_1SigmaUpMuRocFullPropagation/D')
 mass_ScaleSmeared_FnufCorrected_1SigmaDnMuRocFullPropagation_branch = copyTree.Branch('mass_ScaleSmeared_FnufCorrected_1SigmaDnMuRocFullPropagation', mass_ScaleSmeared_FnufCorrected_1SigmaDnMuRocFullPropagation, 'mass_ScaleSmeared_FnufCorrected_1SigmaDnMuRocFullPropagation/D')

 average_RR0_2016_preVFP = []
 average_RR0_2016_postVFP = []
 average_RR0_2017 = []
 average_RR0_2018 = []
 file_RR0 = 0
 if era=="2016_preVFP": file_RR0 = TFile.Open("average_RoverR0_2016_preVFP_withPNCorr.root")
 elif era=="2016_postVFP": file_RR0 = TFile.Open("average_RoverR0_2016_postVFP_withPNCorr.root")
 elif era=="2017": file_RR0 = TFile.Open("average_RoverR0_2017_withPNCorr.root")
 elif era=="2018": file_RR0 = TFile.Open("average_RoverR0_2018_withPNCorr.root")
 
 file_RR0 = TFile.Open("average_RoverR0_2016_preVFP_withPNCorr.root")
 for iRing in range(0,30):
   average_RR0_2016_preVFP.append(file_RR0.Get("gr_RoverR0_vs_Run_ring_"+str(iRing)))  
   average_RR0_2016_preVFP[iRing].Sort()
 file_RR0.Close()
 runMin_2016_preVFP = TMath.MinElement(average_RR0_2016_preVFP[iRing].GetN(),average_RR0_2016_preVFP[iRing].GetX()) 
 runMax_2016_preVFP = TMath.MaxElement(average_RR0_2016_preVFP[iRing].GetN(),average_RR0_2016_preVFP[iRing].GetX())
 
 file_RR0 = TFile.Open("average_RoverR0_2016_postVFP_withPNCorr.root")
 for iRing in range(0,30):
   average_RR0_2016_postVFP.append(file_RR0.Get("gr_RoverR0_vs_Run_ring_"+str(iRing)))  
   average_RR0_2016_postVFP[iRing].Sort()
 file_RR0.Close()
 runMin_2016_postVFP = TMath.MinElement(average_RR0_2016_postVFP[iRing].GetN(),average_RR0_2016_postVFP[iRing].GetX()) 
 runMax_2016_postVFP = TMath.MaxElement(average_RR0_2016_postVFP[iRing].GetN(),average_RR0_2016_postVFP[iRing].GetX())
 
 file_RR0 = TFile.Open("average_RoverR0_2017_withPNCorr.root")
 for iRing in range(0,30):
   average_RR0_2017.append(file_RR0.Get("gr_RoverR0_vs_Run_ring_"+str(iRing)))  
   average_RR0_2017[iRing].Sort()
 file_RR0.Close()
 runMin_2017 = TMath.MinElement(average_RR0_2017[iRing].GetN(),average_RR0_2017[iRing].GetX()) 
 runMax_2017 = TMath.MaxElement(average_RR0_2017[iRing].GetN(),average_RR0_2017[iRing].GetX())
 
 file_RR0 = TFile.Open("average_RoverR0_2018_withPNCorr.root")
 for iRing in range(0,30):
   average_RR0_2018.append(file_RR0.Get("gr_RoverR0_vs_Run_ring_"+str(iRing)))  
   average_RR0_2018[iRing].Sort()
 file_RR0.Close()
 runMin_2018 = TMath.MinElement(average_RR0_2018[iRing].GetN(),average_RR0_2018[iRing].GetX()) 
 runMax_2018 = TMath.MaxElement(average_RR0_2018[iRing].GetN(),average_RR0_2018[iRing].GetX())

 gr_L_vs_R = []
 file_RtoL = TFile.Open("231024_HggMass_distributions.root")
 for iRing in range(0,30):
   gr_L_vs_R.append(file_RtoL.Get("Lsim_vs_RR0_fineSteps/gr_Lsim_vs_RR0_ring_"+str(iRing)))
   gr_L_vs_R[iRing].Sort()
 file_RtoL.Close() 
 rr0Min = TMath.MinElement(gr_L_vs_R[iRing].GetN(),gr_L_vs_R[iRing].GetX()); 
 rr0Max = TMath.MaxElement(gr_L_vs_R[iRing].GetN(),gr_L_vs_R[iRing].GetX());
 
 F_correction = []
 file_fnufCorr = TFile.Open("F_vs_E_vs_lumi_energyRef_50p0_LCE0_with_full_Transparency_iR9_13.root")
 for iRing in range(0,30):
   gr2 = file_fnufCorr.Get("F_vs_E_vs_Lumi_ring_"+str(iRing)+"_iR9_13")
   F_correction.append(gr2) 
 #file_fnufCorr.Close() 
 
 count=0  
 for i,event in enumerate(copyTree):
   if i>copyTree.GetEntries():
   #if i>2:
     break 
   if i%100000==0:
     print("Reading Entry - ",i)   

   runId = getVal(copyTree,'runId')
   pho_energy = getVal(copyTree,'pho_energy')
   pho_EnergyScaleFactorEG = getVal(copyTree,'pho_EnergyScaleFactorEG')
   pho_EnergyScaleFactorEGErr = getVal(copyTree,'pho_EnergyScaleFactorEGErr')
   pho_energySmeared = getVal(copyTree,'pho_energySmeared')
   pho_energySmeared_1sig = getVal(copyTree,'pho_energySmeared_1sig')
   pho_energySmeared_m1sig = getVal(copyTree,'pho_energySmeared_m1sig')
   pho_EnergySmearingSigmaEG = getVal(copyTree,'pho_EnergySmearingSigmaEG')
   pho_energy_ScaleSmeared = getVal(copyTree,'pho_energy_ScaleSmeared')
   pho_pt = getVal(copyTree,'pho_pt') 
   pho_pt_ScaleSmeared = getVal(copyTree,'pho_pt_ScaleSmeared') 
   pho_eta = getVal(copyTree,'pho_eta') 
   pho_phi = getVal(copyTree,'pho_phi') 
   pho_full5x5_r9Corr = getVal(copyTree,'pho_full5x5_r9Corr') 
   muNear_pt = getVal(copyTree,'muNear_pt') 
   muNear_eta = getVal(copyTree,'muNear_eta') 
   muNear_phi = getVal(copyTree,'muNear_phi') 
   muNear_RocCorSF = getVal(copyTree,'muNear_RocCorSF') 
   muNear_RocCorSFerr = getVal(copyTree,'muNear_RocCorSFerr') 
   muFar_pt = getVal(copyTree,'muFar_pt') 
   muFar_eta = getVal(copyTree,'muFar_eta') 
   muFar_phi = getVal(copyTree,'muFar_phi') 
   muFar_RocCorSF = getVal(copyTree,'muFar_RocCorSF') 
   muFar_RocCorSFerr = getVal(copyTree,'muFar_RocCorSFerr') 
   dimu_mass = getVal(copyTree,'dimu_mass') 
   dimu_massRaw = getVal(copyTree,'dimu_massRaw') 
   dimu_mass_1sigmaUpMuRoc = getVal(copyTree,'dimu_mass_1sigmaUpMuRoc') 
   dimu_mass_1sigmaDnMuRoc = getVal(copyTree,'dimu_mass_1sigmaDnMuRoc') 
   dimu_pt = getVal(copyTree,'dimu_pt') 
   dimu_eta = getVal(copyTree,'dimu_eta') 
   dimu_phi = getVal(copyTree,'dimu_phi')
   mass_ScaleSmeared = getVal(copyTree,'mass_ScaleSmeared')
   mass_ScaleSmeared_1sigmaUpSmear = getVal(copyTree,'mass_ScaleSmeared_1sigmaUpSmear')
   mass_ScaleSmeared_1sigmaDnSmear = getVal(copyTree,'mass_ScaleSmeared_1sigmaDnSmear')
   mass_ScaleSmeared_1sigmaUpScale = getVal(copyTree,'mass_ScaleSmeared_1sigmaUpScale')
   mass_ScaleSmeared_1sigmaDnScale = getVal(copyTree,'mass_ScaleSmeared_1sigmaDnScale')
   mass_ScaleSmeared_1sigmaUpMuRoc = getVal(copyTree,'mass_ScaleSmeared_1sigmaUpMuRoc')
   mass_ScaleSmeared_1sigmaDnMuRoc = getVal(copyTree,'mass_ScaleSmeared_1sigmaDnMuRoc')

   iRing = getRing(pho_eta)
   rr0Min = TMath.MinElement(gr_L_vs_R[iRing].GetN(),gr_L_vs_R[iRing].GetX()); 
   rr0Max = TMath.MaxElement(gr_L_vs_R[iRing].GetN(),gr_L_vs_R[iRing].GetX());

   runId_eval = runId
   if runId_eval<=runMin_2016_preVFP: runId_eval = runMin_2016_preVFP+1.0e-11
   if runId_eval>=runMax_2018: runId_eval = runMax_2018-1.0e-11
   
   if mc: runId_eval = int((float(runMin_2016_preVFP)+float(runMax_2018))/2.)

   rr0 = -1.
   if runId_eval>=runMin_2016_preVFP and runId_eval<=runMax_2016_preVFP:
     runMin_2016_preVFP = TMath.MinElement(average_RR0_2016_preVFP[iRing].GetN(),average_RR0_2016_preVFP[iRing].GetX()) 
     runMax_2016_preVFP = TMath.MaxElement(average_RR0_2016_preVFP[iRing].GetN(),average_RR0_2016_preVFP[iRing].GetX())
     if runId_eval<=runMin_2016_preVFP: runId_eval = runMin_2016_preVFP+1.0e-11
     if runId_eval>=runMax_2016_preVFP: runId_eval = runMax_2016_preVFP-1.0e-11
     rr0 = average_RR0_2016_preVFP[iRing].Eval(runId_eval)
   elif runId_eval>=runMin_2016_postVFP and runId_eval<=runMax_2016_postVFP:
     runMin_2016_postVFP = TMath.MinElement(average_RR0_2016_postVFP[iRing].GetN(),average_RR0_2016_postVFP[iRing].GetX()) 
     runMax_2016_postVFP = TMath.MaxElement(average_RR0_2016_postVFP[iRing].GetN(),average_RR0_2016_postVFP[iRing].GetX())
     if runId_eval<=runMin_2016_postVFP: runId_eval = runMin_2016_postVFP+1.0e-11
     if runId_eval>=runMax_2016_postVFP: runId_eval = runMax_2016_postVFP-1.0e-11  
     rr0 = average_RR0_2016_postVFP[iRing].Eval(runId_eval) 
   elif runId_eval>=runMin_2017 and runId_eval<=runMax_2017:
     runMin_2017 = TMath.MinElement(average_RR0_2017[iRing].GetN(),average_RR0_2017[iRing].GetX()) 
     runMax_2017 = TMath.MaxElement(average_RR0_2017[iRing].GetN(),average_RR0_2017[iRing].GetX())
     if runId_eval<=runMin_2017: runId_eval = runMin_2017+1.0e-11
     if runId_eval>=runMax_2017: runId_eval = runMax_2017-1.0e-11  
     rr0 = average_RR0_2017[iRing].Eval(runId_eval) 
   elif runId_eval>=runMin_2018 and runId_eval<=runMax_2018:
     runMin_2018 = TMath.MinElement(average_RR0_2018[iRing].GetN(),average_RR0_2018[iRing].GetX()) 
     runMax_2018 = TMath.MaxElement(average_RR0_2018[iRing].GetN(),average_RR0_2018[iRing].GetX())
     if runId_eval<=runMin_2018: runId_eval = runMin_2018+1.0e-11
     if runId_eval>=runMax_2018: runId_eval = runMax_2018-1.0e-11  
     rr0 = average_RR0_2018[iRing].Eval(runId_eval)    
   
   if rr0>=0:     
     if rr0<=rr0Min: rr0 = rr0Min+1.0e-11
     if rr0>=rr0Max: rr0 = rr0Max-1.0e-11

   energy = pho_energy_ScaleSmeared
   if energy<=20.: energy = 20.+1.0e-11
   if energy>=1000.: energy = 1000.-1.0e-11

   lumi = -1
   if rr0>=0: 
     lumi = gr_L_vs_R[iRing].Eval(rr0)
   gr2 = F_correction[iRing]
   fnufs = [1.,0.,0.]
     
   if pho_full5x5_r9Corr>0.96:
     if not mc:
       if lumi>=0.:
         fnufs = getFNUF(lumi,energy,iRing,gr2)
       #if runId>=runMax_2017-200 and runId<=runMax_2017:
       #  print("runId = ",runId," - lumi = ",lumi," - energy = ",energy," - iRing = ",iRing," - FnufCorr = ",fnufs[0]," - FnufCorr_Up1Sigma = ",fnufs[1]," - FnufCorr_Down1Sigma = ",fnufs[2])  
       pho_FnufCorr[0] = fnufs[0]
       pho_FnufCorrErr[0] = fnufs[1]
     elif mc:
       pho_FnufCorr[0] = 1.
       pho_FnufCorrErr[0] = 0.
   else:
     pho_FnufCorr[0] = 1.
     pho_FnufCorrErr[0] = 0.
   
   muon_mass = 0.1056583755
   #muon_mass = 0.1058581798
   
   # mass with FNUF
   muNear_p4_raw = TLorentzVector()
   muNear_p4_raw.SetPtEtaPhiM(muNear_pt/muNear_RocCorSF, muNear_eta, muNear_phi, muon_mass)
   
   muFar_p4_raw = TLorentzVector()
   muFar_p4_raw.SetPtEtaPhiM(muFar_pt/muFar_RocCorSF, muFar_eta, muFar_phi, muon_mass)
   
   muNear_p4 = TLorentzVector()
   muNear_p4.SetPtEtaPhiM(muNear_pt, muNear_eta, muNear_phi, muon_mass)
   
   muFar_p4 = TLorentzVector()
   muFar_p4.SetPtEtaPhiM(muFar_pt, muFar_eta, muFar_phi, muon_mass)
   
   #print("muFar_p4: ",muFar_p4_raw.Energy()*muFar_RocCorSF,muFar_p4.Energy(),abs(muFar_p4_raw.Energy()*muFar_RocCorSF-muFar_p4.Energy()))
   #print("muNear_p4: ",muNear_p4_raw.Energy()*muNear_RocCorSF,muNear_p4.Energy(),abs(muNear_p4_raw.Energy()*muNear_RocCorSF-muNear_p4.Energy()))
   
   muNear_p4_1sigmaUpMuRoc = TLorentzVector()
   muNear_p4_1sigmaUpMuRoc.SetPtEtaPhiM(muNear_pt*(muNear_RocCorSF+muNear_RocCorSFerr)/muNear_RocCorSF, muNear_eta, muNear_phi, muon_mass)
   
   muNear_p4_1sigmaDnMuRoc = TLorentzVector()
   muNear_p4_1sigmaDnMuRoc.SetPtEtaPhiM(muNear_pt*(muNear_RocCorSF-muNear_RocCorSFerr)/muNear_RocCorSF, muNear_eta, muNear_phi, muon_mass)
   
   muFar_p4_1sigmaUpMuRoc = TLorentzVector()
   muFar_p4_1sigmaUpMuRoc.SetPtEtaPhiM(muFar_pt*(muFar_RocCorSF+muFar_RocCorSFerr)/muFar_RocCorSF, muFar_eta, muFar_phi, muon_mass)
   
   muFar_p4_1sigmaDnMuRoc = TLorentzVector()
   muFar_p4_1sigmaDnMuRoc.SetPtEtaPhiM(muFar_pt*(muFar_RocCorSF-muFar_RocCorSFerr)/muFar_RocCorSF, muFar_eta, muFar_phi, muon_mass)
   
   dimu_p4_raw = muNear_p4_raw + muFar_p4_raw
   dimu_p4 = muNear_p4 + muFar_p4
   dimu_p4_1sigmaUpMuRoc = muNear_p4_1sigmaUpMuRoc + muFar_p4_1sigmaUpMuRoc
   dimu_p4_1sigmaDnMuRoc = muNear_p4_1sigmaDnMuRoc + muFar_p4_1sigmaDnMuRoc
   
   dimu_p4_default = TLorentzVector()
   dimu_p4_default.SetPtEtaPhiM(dimu_pt,dimu_eta,dimu_phi,dimu_mass)
   
   muNear_energyRaw[0] = muNear_p4_raw.Energy()  
   muNear_energy[0] = muNear_p4.Energy()  
   muNear_energy_1sigmaUpMuRoc[0] = muNear_p4_1sigmaUpMuRoc.Energy()
   muNear_energy_1sigmaDnMuRoc[0] = muNear_p4_1sigmaDnMuRoc.Energy()
   muNear_ptRaw[0] = muNear_p4_raw.Pt()  
   muNear_pt_1sigmaUpMuRoc[0] = muNear_p4_1sigmaUpMuRoc.Pt()
   muNear_pt_1sigmaDnMuRoc[0] = muNear_p4_1sigmaDnMuRoc.Pt()
   muFar_energyRaw[0] = muFar_p4_raw.Energy() 
   muFar_energy[0] = muFar_p4.Energy()
   muFar_energy_1sigmaUpMuRoc[0] = muFar_p4_1sigmaUpMuRoc.Energy()
   muFar_energy_1sigmaDnMuRoc[0] = muFar_p4_1sigmaDnMuRoc.Energy()
   muFar_ptRaw[0] = muFar_p4_raw.Pt()
   muFar_pt_1sigmaUpMuRoc[0] = muFar_p4_1sigmaUpMuRoc.Pt()
   muFar_pt_1sigmaDnMuRoc[0] = muFar_p4_1sigmaDnMuRoc.Pt()
   dimu_energyRaw[0] = dimu_p4_raw.Energy()
   dimu_energy[0] = dimu_p4.Energy()
   dimu_energy_1sigmaUpMuRoc[0] = dimu_p4_1sigmaUpMuRoc.Energy()
   dimu_energy_1sigmaDnMuRoc[0] = dimu_p4_1sigmaDnMuRoc.Energy()
   dimu_ptRaw[0] = dimu_p4_raw.Pt()
   dimu_pt_1sigmaUpMuRoc[0] = dimu_p4_1sigmaUpMuRoc.Pt()
   dimu_pt_1sigmaDnMuRoc[0] = dimu_p4_1sigmaDnMuRoc.Pt()
   
   pho_energy_ScaleSmeared_FnufCorrected[0] = pho_energy_ScaleSmeared*pho_FnufCorr[0]
   pho_energy_ScaleSmeared_FnufCorrected_1sigmaUpFnuf[0] = pho_energy_ScaleSmeared*(pho_FnufCorr[0]+pho_FnufCorrErr[0])
   pho_energy_ScaleSmeared_FnufCorrected_1sigmaDnFnuf[0] = pho_energy_ScaleSmeared*(pho_FnufCorr[0]-pho_FnufCorrErr[0])
   pho_pt_ScaleSmeared_FnufCorrected[0] = pho_pt_ScaleSmeared*pho_FnufCorr[0]
   pho_pt_ScaleSmeared_FnufCorrected_1sigmaUpFnuf[0] = pho_pt_ScaleSmeared*(pho_FnufCorr[0]+pho_FnufCorrErr[0])
   pho_pt_ScaleSmeared_FnufCorrected_1sigmaDnFnuf[0] = pho_pt_ScaleSmeared*(pho_FnufCorr[0]-pho_FnufCorrErr[0])
   
   pho_energy_ScaleSmeared_FnufCorrected_1sigmaUpScale = pho_energy_ScaleSmeared_FnufCorrected[0] 
   pho_energy_ScaleSmeared_FnufCorrected_1sigmaDnScale = pho_energy_ScaleSmeared_FnufCorrected[0] 
   if not mc: 
     pho_energy_ScaleSmeared_FnufCorrected_1sigmaUpScale = pho_energy*(pho_EnergyScaleFactorEG+pho_EnergyScaleFactorEGErr)*pho_FnufCorr[0]
     pho_energy_ScaleSmeared_FnufCorrected_1sigmaDnScale = pho_energy*(pho_EnergyScaleFactorEG-pho_EnergyScaleFactorEGErr)*pho_FnufCorr[0]
   pho_pt_ScaleSmeared_FnufCorrected_1sigmaUpScale = pho_pt_ScaleSmeared_FnufCorrected[0] 
   pho_pt_ScaleSmeared_FnufCorrected_1sigmaDnScale = pho_pt_ScaleSmeared_FnufCorrected[0] 
   if not mc: 
     pho_pt_ScaleSmeared_FnufCorrected_1sigmaUpScale = pho_pt*(pho_EnergyScaleFactorEG+pho_EnergyScaleFactorEGErr)*pho_FnufCorr[0]
     pho_pt_ScaleSmeared_FnufCorrected_1sigmaDnScale = pho_pt*(pho_EnergyScaleFactorEG-pho_EnergyScaleFactorEGErr)*pho_FnufCorr[0]
     
   pho_energy_ScaleSmeared_FnufCorrected_1sigmaUpSmear = pho_energy_ScaleSmeared_FnufCorrected[0] 
   pho_energy_ScaleSmeared_FnufCorrected_1sigmaDnSmear = pho_energy_ScaleSmeared_FnufCorrected[0] 
   if mc: 
     pho_energy_ScaleSmeared_FnufCorrected_1sigmaUpSmear = pho_energy*pho_energySmeared_1sig/pho_energy*pho_FnufCorr[0]
     pho_energy_ScaleSmeared_FnufCorrected_1sigmaDnSmear = pho_energy*pho_energySmeared_m1sig/pho_energy*pho_FnufCorr[0]
   pho_pt_ScaleSmeared_FnufCorrected_1sigmaUpSmear = pho_pt_ScaleSmeared_FnufCorrected[0] 
   pho_pt_ScaleSmeared_FnufCorrected_1sigmaDnSmear = pho_pt_ScaleSmeared_FnufCorrected[0] 
   if mc: 
     pho_pt_ScaleSmeared_FnufCorrected_1sigmaUpSmear = pho_pt*pho_energySmeared_1sig/pho_energy*pho_FnufCorr[0]
     pho_pt_ScaleSmeared_FnufCorrected_1sigmaDnSmear = pho_pt*pho_energySmeared_m1sig/pho_energy*pho_FnufCorr[0]
   
   pho_p4 = TLorentzVector()
   pho_p4.SetPtEtaPhiE(pho_pt_ScaleSmeared, pho_eta, pho_phi, pho_energy_ScaleSmeared)
     
   pho_p4_withFnuf = TLorentzVector()
   pho_p4_withFnuf.SetPtEtaPhiE(pho_pt_ScaleSmeared_FnufCorrected[0], pho_eta, pho_phi, pho_energy_ScaleSmeared_FnufCorrected[0])
   
   pho_p4_withFnuf_1sigmaUpFnuf = TLorentzVector()
   pho_p4_withFnuf_1sigmaUpFnuf.SetPtEtaPhiE(pho_pt_ScaleSmeared_FnufCorrected_1sigmaUpFnuf[0], pho_eta, pho_phi, pho_energy_ScaleSmeared_FnufCorrected_1sigmaUpFnuf[0])
   
   pho_p4_withFnuf_1sigmaDnFnuf = TLorentzVector()
   pho_p4_withFnuf_1sigmaDnFnuf.SetPtEtaPhiE(pho_pt_ScaleSmeared_FnufCorrected_1sigmaDnFnuf[0], pho_eta, pho_phi, pho_energy_ScaleSmeared_FnufCorrected_1sigmaDnFnuf[0])
   
   pho_p4_withFnuf_1sigmaUpScale = TLorentzVector()
   pho_p4_withFnuf_1sigmaUpScale.SetPtEtaPhiE(pho_pt_ScaleSmeared_FnufCorrected_1sigmaUpScale, pho_eta, pho_phi, pho_energy_ScaleSmeared_FnufCorrected_1sigmaUpScale)
   
   pho_p4_withFnuf_1sigmaDnScale = TLorentzVector()
   pho_p4_withFnuf_1sigmaDnScale.SetPtEtaPhiE(pho_pt_ScaleSmeared_FnufCorrected_1sigmaDnScale, pho_eta, pho_phi, pho_energy_ScaleSmeared_FnufCorrected_1sigmaDnScale)
   
   pho_p4_withFnuf_1sigmaUpSmear = TLorentzVector()
   pho_p4_withFnuf_1sigmaUpSmear.SetPtEtaPhiE(pho_pt_ScaleSmeared_FnufCorrected_1sigmaUpSmear, pho_eta, pho_phi, pho_energy_ScaleSmeared_FnufCorrected_1sigmaUpSmear)
   
   pho_p4_withFnuf_1sigmaDnSmear = TLorentzVector()
   pho_p4_withFnuf_1sigmaDnSmear.SetPtEtaPhiE(pho_pt_ScaleSmeared_FnufCorrected_1sigmaDnSmear, pho_eta, pho_phi, pho_energy_ScaleSmeared_FnufCorrected_1sigmaDnSmear)
   
   #pho_p4_withFnuf.SetPtEtaPhiM(pho_pt_ScaleSmeared*pho_FnufCorr[0], pho_eta, pho_phi, 0.)
   if abs(mass_ScaleSmeared-(dimu_p4_default + pho_p4).M())>1.e-9: continue
   mass_ScaleSmeared_FnufCorrected[0] = (dimu_p4_default + pho_p4_withFnuf).M()
   mass_ScaleSmeared_FnufCorrected_approx[0] = math.sqrt(pho_FnufCorr[0])*mass_ScaleSmeared
   
   pho_energy_ScaleSmeared_FnufCorrected_err = 0.;
   pho_pt_ScaleSmeared_FnufCorrected_err = 0.;
   if not mc: 
     pho_energy_ScaleSmeared_FnufCorrected_err = pho_energy_ScaleSmeared_FnufCorrected[0]*math.sqrt( (pho_EnergyScaleFactorEGErr/pho_EnergyScaleFactorEG)**2 + (pho_FnufCorrErr[0]/pho_FnufCorr[0])**2 )
     pho_pt_ScaleSmeared_FnufCorrected_err = pho_pt_ScaleSmeared_FnufCorrected[0]*math.sqrt( (pho_EnergyScaleFactorEGErr/pho_EnergyScaleFactorEG)**2 + (pho_FnufCorrErr[0]/pho_FnufCorr[0])**2 )
   #else:
   #  pho_energy_ScaleSmeared_FnufCorrected_err = pho_energy*pho_EnergySmearingSigmaEG
   #  pho_pt_ScaleSmeared_FnufCorrected_err = pho_pt*pho_EnergySmearingSigmaEG
     
   muNear_pt_RocCorected_err = muNear_pt*muNear_RocCorSFerr
   muFar_pt_RocCorected_err = muFar_pt*muFar_RocCorSFerr
    
   pho_p4_raw_vec = (0.,pho_pt,pho_p4.Eta(),pho_p4.Phi()) 
   muNear_p4_raw_vec = (muon_mass,muNear_p4_raw.Pt(),muNear_p4_raw.Eta(),muNear_p4_raw.Phi())
   muFar_p4_raw_vec = (muon_mass,muFar_p4_raw.Pt(),muFar_p4_raw.Eta(),muFar_p4_raw.Phi())
   dmass_over_dcorr_2particles = dM_dcorr([muNear_p4_raw_vec,muFar_p4_raw_vec],muNear_RocCorSF,muFar_RocCorSF,0.,0.,2)
   dmass_over_dcorr_3particles = dM_dcorr([pho_p4_raw_vec,muNear_p4_raw_vec,muFar_p4_raw_vec],pho_EnergyScaleFactorEG,pho_FnufCorr[0],muNear_RocCorSF,muFar_RocCorSF,3)
   
   dimu_mass_errMuRocFullPropagation[0] = math.sqrt( (dmass_over_dcorr_2particles[0]*muNear_RocCorSFerr)**2 + (dmass_over_dcorr_2particles[1]*muFar_RocCorSFerr)**2 + 2*dmass_over_dcorr_2particles[0]*dmass_over_dcorr_2particles[1]*muNear_RocCorSFerr*muFar_RocCorSFerr )
   dimu_mass_1SigmaUpErrMuRocFullPropagation[0] = dimu_mass + dimu_mass_errMuRocFullPropagation[0]
   dimu_mass_1SigmaDnErrMuRocFullPropagation[0] = dimu_mass - dimu_mass_errMuRocFullPropagation[0]
   
   mass_ScaleSmeared_FnufCorrected_errScaleFullPropagation[0] = 0.
   mass_ScaleSmeared_FnufCorrected_errFnufFullPropagation[0] = 0.
   mass_ScaleSmeared_FnufCorrected_errFullPropagNoSmear[0] = 0.
   mass_ScaleSmeared_FnufCorrected_errMuRocFullPropagation[0] = math.sqrt( (dmass_over_dcorr_3particles[2]*muNear_RocCorSFerr)**2 + (dmass_over_dcorr_3particles[3]*muFar_RocCorSFerr)**2 + 2*dmass_over_dcorr_3particles[2]*dmass_over_dcorr_3particles[3]*muNear_RocCorSFerr*muFar_RocCorSFerr )
   if not mc:
     mass_ScaleSmeared_FnufCorrected_errScaleFullPropagation[0] = math.sqrt( (dmass_over_dcorr_3particles[0]*pho_EnergyScaleFactorEGErr)**2 )
     mass_ScaleSmeared_FnufCorrected_errFnufFullPropagation[0] = math.sqrt( (dmass_over_dcorr_3particles[1]*pho_FnufCorrErr[0])**2 )
     mass_ScaleSmeared_FnufCorrected_errFullPropagNoSmear[0] = math.sqrt( (dmass_over_dcorr_3particles[0]*pho_EnergyScaleFactorEGErr)**2 + (dmass_over_dcorr_3particles[1]*pho_FnufCorrErr[0])**2 + (dmass_over_dcorr_3particles[2]*muNear_RocCorSFerr)**2 + (dmass_over_dcorr_3particles[3]*muFar_RocCorSFerr)**2 + 2*dmass_over_dcorr_3particles[2]*dmass_over_dcorr_3particles[3]*muNear_RocCorSFerr*muFar_RocCorSFerr )
   else:
     mass_ScaleSmeared_FnufCorrected_errFullPropagNoSmear[0] = math.sqrt( (dmass_over_dcorr_3particles[2]*muNear_RocCorSFerr)**2 + (dmass_over_dcorr_3particles[3]*muFar_RocCorSFerr)**2 + 2*dmass_over_dcorr_3particles[2]*dmass_over_dcorr_3particles[3]*muNear_RocCorSFerr*muFar_RocCorSFerr )
  
   #dimu_mass_1sigmaUpMuRoc_new = dimu_p4_1sigmaUpMuRoc.M()
   #dimu_mass_1sigmaDnMuRoc_new = dimu_p4_1sigmaDnMuRoc.M()
   #print("dimu_mass_1sigmaUpMuRoc = ",dimu_mass_1sigmaUpMuRoc,dimu_mass_1sigmaUpMuRoc_new,abs(dimu_mass_1sigmaUpMuRoc-dimu_mass_1sigmaUpMuRoc_new))
   #print("dimu_mass_1sigmaDnMuRoc = ",dimu_mass_1sigmaDnMuRoc,dimu_mass_1sigmaDnMuRoc_new,abs(dimu_mass_1sigmaDnMuRoc-dimu_mass_1sigmaDnMuRoc_new))
   
   # mass with full error propagation (no smearing uncertainties)
   mass_ScaleSmeared_FnufCorrected_1SigmaUpFnufFullPropagation[0] = mass_ScaleSmeared_FnufCorrected[0]+mass_ScaleSmeared_FnufCorrected_errFnufFullPropagation[0]
   mass_ScaleSmeared_FnufCorrected_1SigmaDnFnufFullPropagation[0] = mass_ScaleSmeared_FnufCorrected[0]-mass_ScaleSmeared_FnufCorrected_errFnufFullPropagation[0]
   mass_ScaleSmeared_FnufCorrected_1SigmaUpScaleFullPropagation[0] = mass_ScaleSmeared_FnufCorrected[0]+mass_ScaleSmeared_FnufCorrected_errScaleFullPropagation[0]
   mass_ScaleSmeared_FnufCorrected_1SigmaDnScaleFullPropagation[0] = mass_ScaleSmeared_FnufCorrected[0]-mass_ScaleSmeared_FnufCorrected_errScaleFullPropagation[0]
   mass_ScaleSmeared_FnufCorrected_1SigmaUpMuRocFullPropagation[0] = mass_ScaleSmeared_FnufCorrected[0]+mass_ScaleSmeared_FnufCorrected_errMuRocFullPropagation[0]
   mass_ScaleSmeared_FnufCorrected_1SigmaDnMuRocFullPropagation[0] = mass_ScaleSmeared_FnufCorrected[0]-mass_ScaleSmeared_FnufCorrected_errMuRocFullPropagation[0]
   mass_ScaleSmeared_FnufCorrected_1SigmaUpErrFullPropagNoSmear[0] = mass_ScaleSmeared_FnufCorrected[0]+mass_ScaleSmeared_FnufCorrected_errFullPropagNoSmear[0]
   mass_ScaleSmeared_FnufCorrected_1SigmaDnErrFullPropagNoSmear[0] = mass_ScaleSmeared_FnufCorrected[0]-mass_ScaleSmeared_FnufCorrected_errFullPropagNoSmear[0]
   
   # mass with FNUF+1sigmaUpFnuf
   mass_ScaleSmeared_FnufCorrected_1sigmaUpFnuf[0] = (dimu_p4_default+pho_p4_withFnuf_1sigmaUpFnuf).M()

   # mass with FNUF-1sigmaDnFnuf
   mass_ScaleSmeared_FnufCorrected_1sigmaDnFnuf[0] = (dimu_p4_default+pho_p4_withFnuf_1sigmaDnFnuf).M()
   
   # mass with FNUF+1sigmaUpSmear
   mass_ScaleSmeared_FnufCorrected_1sigmaUpSmear[0] = (dimu_p4_default+pho_p4_withFnuf_1sigmaUpSmear).M()

   # mass with FNUF-1sigmaDownSmear 
   mass_ScaleSmeared_FnufCorrected_1sigmaDnSmear[0] = (dimu_p4_default+pho_p4_withFnuf_1sigmaDnSmear).M()
   
   # mass with FNUF+1sigmaUpScale
   mass_ScaleSmeared_FnufCorrected_1sigmaUpScale[0] = (dimu_p4_default+pho_p4_withFnuf_1sigmaUpScale).M()

   # mass with FNUF-1sigmaDownScale
   mass_ScaleSmeared_FnufCorrected_1sigmaDnScale[0] = (dimu_p4_default+pho_p4_withFnuf_1sigmaDnScale).M()

   # mass with FNUF+1sigmaUpMuRoc
   mass_ScaleSmeared_FnufCorrected_1sigmaUpMuRoc[0] = (dimu_p4_1sigmaUpMuRoc + pho_p4_withFnuf).M()

   # mass with FNUF-1sigmaDnMuRoc
   mass_ScaleSmeared_FnufCorrected_1sigmaDnMuRoc[0] = (dimu_p4_1sigmaDnMuRoc + pho_p4_withFnuf).M()

   # mass full-1sigmaUp
   mass_ScaleSmeared_allUp[0] = mass_ScaleSmeared + ( abs(mass_ScaleSmeared_1sigmaUpSmear-mass_ScaleSmeared) + abs(mass_ScaleSmeared_1sigmaUpScale-mass_ScaleSmeared) + abs(mass_ScaleSmeared_1sigmaUpMuRoc-mass_ScaleSmeared) )

   # mass full-1sigmaDown
   mass_ScaleSmeared_allDown[0] = mass_ScaleSmeared - ( abs(mass_ScaleSmeared_1sigmaDnSmear-mass_ScaleSmeared) + abs(mass_ScaleSmeared_1sigmaDnScale-mass_ScaleSmeared) + abs(mass_ScaleSmeared_1sigmaDnMuRoc-mass_ScaleSmeared) )

   # mass with FNUF full-1sigmaUp
   mass_ScaleSmeared_FnufCorrected_allUp[0] = mass_ScaleSmeared_FnufCorrected[0] + ( abs(mass_ScaleSmeared_FnufCorrected_1sigmaUpSmear[0]-mass_ScaleSmeared_FnufCorrected[0]) + abs(mass_ScaleSmeared_FnufCorrected_1sigmaUpScale[0]-mass_ScaleSmeared_FnufCorrected[0]) + abs(mass_ScaleSmeared_FnufCorrected_1sigmaUpMuRoc[0]-mass_ScaleSmeared_FnufCorrected[0]) + abs(mass_ScaleSmeared_FnufCorrected_1sigmaUpFnuf[0]-mass_ScaleSmeared_FnufCorrected[0]) )

   # mass with FNUF full-1sigmaDown
   mass_ScaleSmeared_FnufCorrected_allDown[0] = mass_ScaleSmeared_FnufCorrected[0] - ( abs(mass_ScaleSmeared_FnufCorrected_1sigmaDnSmear[0]-mass_ScaleSmeared_FnufCorrected[0]) + abs(mass_ScaleSmeared_FnufCorrected_1sigmaDnScale[0]-mass_ScaleSmeared_FnufCorrected[0]) + abs(mass_ScaleSmeared_FnufCorrected_1sigmaDnMuRoc[0]-mass_ScaleSmeared_FnufCorrected[0]) + abs(mass_ScaleSmeared_FnufCorrected_1sigmaDnFnuf[0]-mass_ScaleSmeared_FnufCorrected[0]) )
  
   muNear_energyRaw_branch.Fill() 
   muNear_energy_branch.Fill()
   muNear_energy_1sigmaUpMuRoc_branch.Fill()
   muNear_energy_1sigmaDnMuRoc_branch.Fill()
   muNear_ptRaw_branch.Fill()
   muNear_pt_1sigmaUpMuRoc_branch.Fill()
   muNear_pt_1sigmaDnMuRoc_branch.Fill()
   muFar_energyRaw_branch.Fill()
   muFar_energy_branch.Fill()
   muFar_energy_1sigmaUpMuRoc_branch.Fill()
   muFar_energy_1sigmaDnMuRoc_branch.Fill()
   muFar_ptRaw_branch.Fill()
   muFar_pt_1sigmaUpMuRoc_branch.Fill()
   muFar_pt_1sigmaDnMuRoc_branch.Fill()
   dimu_energyRaw_branch.Fill()
   dimu_energy_branch.Fill()
   dimu_energy_1sigmaUpMuRoc_branch.Fill()
   dimu_energy_1sigmaDnMuRoc_branch.Fill()
   dimu_ptRaw_branch.Fill()
   dimu_pt_1sigmaUpMuRoc_branch.Fill()
   dimu_pt_1sigmaDnMuRoc_branch.Fill()
   dimu_mass_errMuRocFullPropagation_branch.Fill()
   dimu_mass_1SigmaUpErrMuRocFullPropagation_branch.Fill()
   dimu_mass_1SigmaDnErrMuRocFullPropagation_branch.Fill()
   pho_FnufCorr_branch.Fill()
   pho_FnufCorrErr_branch.Fill()
   pho_energy_ScaleSmeared_FnufCorrected_branch.Fill()
   pho_energy_ScaleSmeared_FnufCorrected_1sigmaUpFnuf_branch.Fill()
   pho_energy_ScaleSmeared_FnufCorrected_1sigmaDnFnuf_branch.Fill()
   pho_pt_ScaleSmeared_FnufCorrected_branch.Fill()
   pho_pt_ScaleSmeared_FnufCorrected_1sigmaUpFnuf_branch.Fill()
   pho_pt_ScaleSmeared_FnufCorrected_1sigmaDnFnuf_branch.Fill()
   mass_ScaleSmeared_FnufCorrected_errFullPropagNoSmear_branch.Fill()
   mass_ScaleSmeared_FnufCorrected_errFnufFullPropagation_branch.Fill()
   mass_ScaleSmeared_FnufCorrected_errScaleFullPropagation_branch.Fill()
   mass_ScaleSmeared_FnufCorrected_errMuRocFullPropagation_branch.Fill()
   mass_ScaleSmeared_allUp_branch.Fill()
   mass_ScaleSmeared_allDown_branch.Fill()
   mass_ScaleSmeared_FnufCorrected_branch.Fill()
   mass_ScaleSmeared_FnufCorrected_approx_branch.Fill()
   mass_ScaleSmeared_FnufCorrected_allUp_branch.Fill()
   mass_ScaleSmeared_FnufCorrected_allDown_branch.Fill()
   mass_ScaleSmeared_FnufCorrected_1sigmaUpFnuf_branch.Fill()
   mass_ScaleSmeared_FnufCorrected_1sigmaDnFnuf_branch.Fill()
   mass_ScaleSmeared_FnufCorrected_1sigmaUpSmear_branch.Fill()
   mass_ScaleSmeared_FnufCorrected_1sigmaDnSmear_branch.Fill() 
   mass_ScaleSmeared_FnufCorrected_1sigmaUpScale_branch.Fill()
   mass_ScaleSmeared_FnufCorrected_1sigmaDnScale_branch.Fill()
   mass_ScaleSmeared_FnufCorrected_1sigmaUpMuRoc_branch.Fill()
   mass_ScaleSmeared_FnufCorrected_1sigmaDnMuRoc_branch.Fill() 
   mass_ScaleSmeared_FnufCorrected_1SigmaUpErrFullPropagNoSmear_branch.Fill()
   mass_ScaleSmeared_FnufCorrected_1SigmaDnErrFullPropagNoSmear_branch.Fill()
   mass_ScaleSmeared_FnufCorrected_1SigmaUpFnufFullPropagation_branch.Fill()
   mass_ScaleSmeared_FnufCorrected_1SigmaDnFnufFullPropagation_branch.Fill()
   mass_ScaleSmeared_FnufCorrected_1SigmaUpScaleFullPropagation_branch.Fill()
   mass_ScaleSmeared_FnufCorrected_1SigmaDnScaleFullPropagation_branch.Fill()
   mass_ScaleSmeared_FnufCorrected_1SigmaUpMuRocFullPropagation_branch.Fill()
   mass_ScaleSmeared_FnufCorrected_1SigmaDnMuRocFullPropagation_branch.Fill()
  
if __name__ == '__main__': 

 gROOT.SetBatch(kTRUE)

 parser =  argparse.ArgumentParser(description='Zmmg')
 parser.add_argument('--era', dest='era', required=False,  type=str)
 parser.add_argument('--data', dest='data', action='store_true')
 parser.add_argument('--mc',   dest='mc',   action='store_true')
 parser.set_defaults(data  = False)
 parser.set_defaults(mc    = False)

 args = parser.parse_args()

 era = args.era
 data = args.data
 mc  = args.mc

 treeName = ""
 if mc:
   if era=="2016_preVFP": treeName = "/eos/user/b/bmarzocc/Zmmg_ForFNUF/DY2016_ZpT_preVFP_all.root/ZmmgTree" 
   elif era=="2016_postVFP": treeName = "/eos/user/b/bmarzocc/Zmmg_ForFNUF/DY2016_ZpT_postVFP_all.root/ZmmgTree" 
   elif era=="2017": treeName = "/eos/user/b/bmarzocc/Zmmg_ForFNUF/DY2017_ZpT_all.root/ZmmgTree" 
   elif era=="2018": treeName = "/eos/user/b/bmarzocc/Zmmg_ForFNUF/DY2018_ZpT_all.root/ZmmgTree"
   elif era=="Run2": treeName = "/eos/user/b/bmarzocc/Zmmg_ForFNUF_phoReg_IJazz_SnS/DY_ZpT_S5_Run2.root/ZmmgTree"
   #elif era=="Run2": treeName = "/eos/user/b/bmarzocc/Zmmg_ForFNUF_phoReg_EGM_SnS/DY_ZpT_S5_Run2.root/ZmmgTree"
 if data:
   if era=="2016_preVFP": treeName = "/eos/user/b/bmarzocc/Zmmg_ForFNUF/data2016UL_ZpT_preVFP_all.root/ZmmgTree" 
   elif era=="2016_postVFP": treeName = "/eos/user/b/bmarzocc/Zmmg_ForFNUF/data2016UL_ZpT_postVFP_all.root/ZmmgTree" 
   elif era=="2017": treeName = "/eos/user/b/bmarzocc/Zmmg_ForFNUF/data2017UL_ZpT_all.root/ZmmgTree" 
   elif era=="2018": treeName = "/eos/user/b/bmarzocc/Zmmg_ForFNUF/data2018UL_ZpT_all.root/ZmmgTree" 
   elif era=="Run2": treeName = "/eos/user/b/bmarzocc/Zmmg_ForFNUF_phoReg_IJazz_SnS/data_ZpT_S5_Run2.root/ZmmgTree" 
   #elif era=="Run2": treeName = "/eos/user/b/bmarzocc/Zmmg_ForFNUF_phoReg_EGM_SnS/data_ZpT_S5_Run2.root/ZmmgTree" 
  
 print("treeName = ",treeName)
 tree = TChain()
 tree.Add(treeName) 
 
 outName = treeName
 outName = outName.replace('.root/ZmmgTree','_withFNUF_withPNCorr.root')
 outFile = TFile(outName,'RECREATE')
 outTree = TChain()
 outTree.AddFile(treeName)
 addBranches(outTree,mc)
 outFile.Write()
 outFile.Close()
 
 
   
