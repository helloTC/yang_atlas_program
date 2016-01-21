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

# Index files
zstat_img_file = '/nfs/j3/userhome/huangtaicheng/workingdir/parcellation_MT/BAA/results/yang_test/sub/sub_split/mergedata/zstat_combined.nii.gz'
mask_img_file = '/nfs/j3/userhome/huangtaicheng/workingdir/parcellation_MT/BAA/results/yang_test/sub/sub_split/mergedata/mt_z5.0.nii.gz'
psc_img_file = '/nfs/j3/userhome/huangtaicheng/workingdir/parcellation_MT/BAA/results/yang_test/sub/sub_split/mergedata/psc_combined.nii.gz'
alff_img_file = '/nfs/j3/userhome/huangtaicheng/workingdir/parcellation_MT/BAA/results/yang_test/sub/sub_split/mergedata/alff_combined.nii.gz'
falff_img_file = '/nfs/j3/userhome/huangtaicheng/workingdir/parcellation_MT/BAA/results/yang_test/sub/sub_split/mergedata/falff_combined.nii.gz'
reho_img_file = '/nfs/j3/userhome/huangtaicheng/workingdir/parcellation_MT/BAA/results/yang_test/sub/sub_split/mergedata/reho_combined.nii.gz'

areaname = ['rV3','lV3','rMT','lMT']
areanum = [1,2,3,4]
taskname = 'motion'
contrast = 'motion-fix'

pathsex = '/nfs/j3/userhome/huangtaicheng/workingdir/parcellation_MT/doc/dfsf/modeID'
gender = pd.read_csv(os.path.join(pathsex, 'act_sex.csv'))['gender'].tolist()
# gender_rest = pd.read_csv(os.path.join(pathsex, 'interID', 'inter_act_restingsex.csv'))['gender'].tolist()
sessid = open('/nfs/j3/userhome/huangtaicheng/workingdir/parcellation_MT/doc/dfsf/modeID/actID','rU').read().splitlines()
# sessid_rest = open('/nfs/j3/userhome/huangtaicheng/workingdir/parcellation_MT/doc/dfsf/modeID/interID/inter_act_restingID','rU').read().splitlines()
#-----------------------------------------------------------------------------#
# Split sessid into two halves
# pre_enum,post_enum = random_split_list(range(len(list(sessid_act))))
# pre_sessid_act = list(np.array(sessid_act)[pre_enum])
# post_sessid_act = list(np.array(sessid_act)[post_enum])
# pre_gender_act = list(np.array(gender_act)[pre_enum])
# post_gender_act = list(np.array(gender_act)[post_enum])
#-----------------------------------------------------------------------------#
# Prepare data
sessn = range(len(sessid))
# sessn_rest = range(len(sessid_rest))
# zstat
zstat_rawdata = Dataset(zstat_img_file, mask_img_file, areaname, areanum, gender, sessid, taskname, contrast)
zstat_rawdata.loadfile()
# psc
psc_rawdata = Dataset(psc_img_file, mask_img_file, areaname, areanum, gender, sessid, taskname, contrast)
psc_rawdata.loadfile()
# alff
alff_rawdata = Dataset(alff_img_file, mask_img_file, areaname, areanum, gender, sessid, taskname, contrast)
alff_rawdata.loadfile()
# falff
falff_rawdata = Dataset(falff_img_file, mask_img_file, areaname, areanum, gender, sessid, taskname, contrast)
falff_rawdata.loadfile()
# reho
reho_rawdata = Dataset(reho_img_file, mask_img_file, areaname, areanum, gender, sessid, taskname, contrast)
reho_rawdata.loadfile()

#---------------------------calculate index for whole data---------------------#
zstat_index = cal_index(zstat_rawdata, sessid, sessn, gender)
zstat_index.volume_index()
zstat_index.mask_index('zstat')
zstat_index.peakcoord_index()

psc_index = cal_index(psc_rawdata, sessid, sessn, gender)
psc_index.psc_index()
psc_index.peakcoord_index()

alff_index = cal_index(alff_rawdata, sessid, sessn, gender)
alff_index.mask_index('alff')
alff_index.peakcoord_index()

falff_index = cal_index(falff_rawdata, sessid, sessn, gender)
falff_index.mask_index('falff')
falff_index.peakcoord_index()

reho_index = cal_index(reho_rawdata, sessid, sessn, gender)
reho_index.mask_index('reho')
reho_index.peakcoord_index()
#---------------------------calculate PM and MPM------------------------------#
getprob = make_atlas(zstat_rawdata, sessid, sessn)
getprob.probatlas()
getprob.MPM(0.2)



