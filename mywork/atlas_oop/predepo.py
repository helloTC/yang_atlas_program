# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode:nil -*-
# vi: set ft=python sts=4 sw=4 et:

import os
import numpy as np
import nibabel as nib

class user_defined_exception(Exception):
    def __init__(self, str):
        Exception.__init__(self)
        self._str = str



class Dataset(object):
    def __init__(self, targ_img_file, mask_img_file, areaname, areanum, gender, sessid):
        self.ftarg_img = targ_img_file
        self.fmask_img = mask_img_file
        self.areaname = areaname
        self.areanum = areanum
        self.gender = gender
        self.affine = []    
        self.targ_data = []
        self.mask_data = []
        self.shape = []
        self.header = []
        self.sessid = sessid
        self.narea = len(areanum)
    def loadfile(self):
    # load targ_img_file and mask_img_file
        targ_img = nib.load(self.ftarg_img)
        if len(targ_img.get_shape()) != 4:
             raise user_defined_exception('targ_img is not a Nifti 4D image!')
        targ_data = targ_img.get_data()
        self.affine = targ_img.get_affine()
        self.header = targ_img.get_header()
        self.shape = targ_img.get_shape()

    # import mask files.Pay attention if masktype is 'subject',mask is a 4D image
    # if masktype is 'mpm',mask is a 3D image for each subjects
        mask_img = nib.load(self.fmask_img)
        mask_data = mask_img.get_data()

        self.targ_data = targ_data
        self.mask_data = mask_data

class cal_index(object):
    def __init__(self, ds, sessid, sessn, gender):
    # nsubj is the number of subjects
    # narea is the number of areas
        self.targ_data = ds.targ_data
        self.mask_data = ds.mask_data
        self.areanum = ds.areanum
        self.affine = ds.affine
        self.sessid = sessid
        self.sessn = sessn
        self.gender = gender

        self.act_volume = []
        self.mean_zstat = []
        self.peak_zstat = []
        self.mean_psc = []
        self.peak_psc = []
        self.peak_coordin = []
        self.mean_alff = []
        self.peak_alff = []
        self.mean_falff = []
        self.peak_falff = []
        self.mean_reho = []
        self.peak_reho = []
        
    def volume_index(self, res=[2,2,2]):
        act_volume = []
        if len(self.mask_data.shape) == 4:
            for i in self.sessn:
                act_volume.append(cal_volume(self.mask_data[:,:,:,i], self.areanum, res))
        elif len(self.mask_data.shape) == 3:
            for i in self.sessn:
                act_volume.append(cal_volume(self.mask_data, self.areanum, res))
        else:
            raise user_defined_exception('mask_data need to be 3D or 4D volume!')
        self.act_volume = act_volume
                               
    def mask_index(self, index):
# for mean and max value of z-values,falff,alff,reho,etc.
        mean_value = []
        peak_value = []
        if len(self.mask_data.shape) == 4:
            for i in self.sessn:
                [mvalue,pvalue] = cal_mask(self.targ_data[:,:,:,i], self.mask_data[:,:,:,i], self.areanum)
                mean_value.append(mvalue)
                peak_value.append(pvalue)
        elif len(self.mask_data.shape) == 3:
            for i in self.sessn:
                [mvalue,pvalue] = cal_mask(self.targ_data[:,:,:,i], self.mask_data, self.areanum)
                mean_value.append(mvalue)
                peak_value.append(pvalue)
        else:
            raise user_defined_exception('mask_data need to be 3D or 4D volume!')

        if index == 'zstat':
            self.mean_zstat = mean_value
            self.peak_zstat = peak_value
        elif index == 'alff':
            self.mean_alff = mean_value
            self_peak_alff = peak_value
        elif index == 'falff':
            self.mean_falff == mean_value
            self.peak_falff == peak_value
        elif index == 'reho':
            self.mean_reho == mean_value
            self.peak_reho == peak_value
        else:
            raise user_defined_exception("please input index as 'zstat' or 'alff' or 'falff' or 'reho'!")
        
    def psc_index(self):
        mean_psc = []
        peak_psc = []
        if len(self.mask_data.shape) == 4:
            for i in self.sessn:
                [mpsc,ppsc] = cal_psc(self.targ_data[:,:,:,i], self.mask_data[:,:,:,i], self.areanum)
                mean_psc.append(mpsc)
                peak_psc.append(ppsc)
        elif len(self.mask_data.shape) == 3:
            for i in self.sessn:
                [mpsc,ppsc] = cal_psc(self.targ_data[:,:,:,i], self.mask_data, self.areanum)
                mean_psc.append(mpsc)
                peak_psc.append(ppsc)
        else:
            raise user_defined_exception('mask_data need to be 3D or 4D volume!')
        self.mean_psc = mean_psc
        self.peak_psc = peak_psc

    def peakcoord_index(self):
        peak_coordin = []
        if len(self.mask_data.shape) == 4:
            for i in self.sessn:
                pcor = cal_coordin(self.targ_data[:,:,:,i], self.mask_data[:,:,:,i], self.areanum, self.affine)
                peak_coordin.append(pcor)
        elif len(self.mask_data.shape) == 3:
            for i in self.sessn:
                pcor = cal_coordin(self.targ_data[:,:,:,i], self.mask_data, self.areanum, self.affine)
                peak_coordin.append(pcor)
        else:
            raise user_defined_exception('mask_data need to be 3D or 4D volume!')
        self.peak_coordin = peak_coordin












#-------------------functions-----------------------#
#-------------------volume--------------------------#
def listinmul(mul_list):
    outnum = reduce(lambda x,y:x*y,mul_list)
    return outnum

def cal_volume(mask_data, areanum, resolu):
    volume = []
    for areai in areanum:
        volume.append(np.sum(mask_data == (areai))*listinmul(resolu))
    return volume       
#-------------------z-value--------------------------#
def cal_mask(targ_data, mask_data, areanum):
    mzstat = []
    pzstat = []
    for areai in areanum:
        if len(targ_data[mask_data == areai])!=0:
            mzstat.append(np.nanmean(targ_data[mask_data == areai]))
            pzstat.append(np.nanmax(targ_data[mask_data == areai]))
        else: 
            mzstat.append(0)
            pzstat.append(0)
    return mzstat,pzstat
#-------------------psc-value-------------------------#
def cal_psc(targ_data, mask_data, areanum):
    mpsc = []
    ppsc = []
    for areai in areanum:
        if len(targ_data[mask_data == areai])!=0:
            mpsc.append(np.nanmean(targ_data[mask_data == areai])/100)
            ppsc.append(np.nanmax(targ_data[mask_data == areai])/100)
        else:
            mpsc.append(0)
            ppsc.append(0)
    return mpsc,ppsc
#--------------------MNI coordinate------------------#
def vox2MNI(vox, affine):
    vox_new = np.ones([4,1])
    vox_new[0:-1,0] = vox[:]
    MNI = affine.dot(vox_new)
    MNI_new = MNI[0:-1].tolist()    # transform array into list
    return sum(MNI_new,[])  # extend multiple list

def cal_coordin(targ_data, mask_data, areanum, affine):
# The final data format will be like this:[[x,y,z],[x,y,z],etc] for each subject
    co_area = []
    for areai in areanum:
        if len(targ_data[mask_data == areai])!=0:
            temp = np.zeros([91,109,91])
            temp[mask_data == areai] = targ_data[mask_data == areai]
            peakcor_vox = np.unravel_index(temp.argmax(), temp.shape)        
            peakcor_mni = list(vox2MNI(peakcor_vox ,affine))
            co_area.append(peakcor_mni)
            peakcor_mni = []
        else:
            co_area.append([])
    return co_area
        


    
     

