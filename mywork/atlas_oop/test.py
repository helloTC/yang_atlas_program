# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 et:1

"Test for atlas extraction and analysis"

from predepo import *
import pandas as pd
import random

def random_split_list(raw_list):
    length_list = len(raw_list)
    split_list = random.sample(raw_list,length_list)
    pre_splitlist = split_list[0:length_list/2]
    post_splitlist = split_list[length_list/2:]
    return pre_splitlist,post_splitlist

zstat_img_file = '/nfs/j3/userhome/huangtaicheng/workingdir/parcellation_MT/BAA/results/yang_test/sub/sub_split/zstat_combined.nii.gz'
mask_img_file = '/nfs/j3/userhome/huangtaicheng/workingdir/parcellation_MT/BAA/results/yang_test/sub/sub_split/mt_z5.0.nii.gz'
psc_img_file = '/nfs/j3/userhome/huangtaicheng/workingdir/parcellation_MT/BAA/results/yang_test/sub/sub_split/psc_combined.nii.gz'
areaname = ['rV3','lV3','rMT','lMT']
areanum = [1,2,3,4]
pathsex = '/nfs/j3/userhome/huangtaicheng/workingdir/parcellation_MT/doc/dfsf/sub/'
gender = pd.read_csv(pathsex+'sex.csv')['gender'].tolist()
sessid = open('/nfs/j3/userhome/huangtaicheng/workingdir/parcellation_MT/doc/dfsf/sub/subjID','rU').read().splitlines()
#-----------------------------------------------------------------------------#
# Split sessid into two halves
pre_enum,post_enum = random_split_list(range(len(list(sessid))))
pre_sessid = list(np.array(sessid)[pre_enum])
post_sessid = list(np.array(sessid)[post_enum])
pre_gender = list(np.array(gender)[pre_enum])
post_gender = list(np.array(gender)[post_enum])
#-----------------------------------------------------------------------------#
# Prepare data
sessn = range(len(sessid))
zstat_rawdata = Dataset(zstat_img_file, mask_img_file, areaname, areanum, gender, sessid)
zstat_rawdata.loadfile()

#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#
# Try to calculate index in the first half

zstat_pre = cal_index(zstat_rawdata, pre_sessid, pre_enum, pre_gender)
# Volume in zstat
zstat_pre.volume_index()
# zstat in zstat
zstat_pre.mask_index('zstat')
# zpeak coordinate in zstat
zstat_pre.peakcoord_index()
#-----------------------------------------------------------------------------#
# Calculate psc_value
psc_rawdata = Dataset(psc_img_file, mask_img_file, areaname, areanum, gender, sessid)
psc_rawdata.loadfile()

psc_pre = cal_index(psc_rawdata, pre_sessid, pre_enum, pre_gender)
# psc in cal_psc
psc_pre.psc_index()
# psc_peak coordinate in psc
psc_pre.peakcoord_index()
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
# Try to calculate index in the second half

zstat_post = cal_index(zstat_rawdata, post_sessid, post_enum, post_gender)
# volume
zstat_post.volume_index()
# zstat values
zstat_post.mask_index('zstat')
# zstat_peak coordinate in zstat
zstat_post.peakcoord_index()

psc_post = cal_index(psc_rawdata, post_sessid, post_enum, post_gender)
# psc values
psc_post.psc_index()
# psc_peak coordinate in psc
psc_post.peakcoord_index()

#------------------------------------------------------------------------------#
#-------------Try to get probatlas and maximum probatlas-----------------------#
getprob = make_atlas(zstat_rawdata, sessid, sessn)
getprob.probatlas()
getprob.MPM(0.2)



