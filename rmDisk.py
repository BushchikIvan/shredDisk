import os
_lsblkOutputPATH = os.popen('/bin/lsblk -o PATH')
_lsblkOutputTYPE = os.popen('/bin/lsblk -o FSTYPE')
lsblkOutputPATH = _lsblkOutputPATH.read().split('\n')
lsblkOutputFSTYPE = _lsblkOutputTYPE.read().split('\n')

drivesTormPATH = []
drivesTormFSTYPE = []
for i in range(len(lsblkOutputPATH)-1):
    if str(lsblkOutputPATH[i])[-1:].isdigit() and not('loop' in str(lsblkOutputPATH[i])) and not('sr' in str(lsblkOutputPATH[i])):
        drivesTormPATH.append(lsblkOutputPATH[i])
        drivesTormFSTYPE.append(lsblkOutputFSTYPE[i])

counter = 0
for i in range(len(drivesTormPATH)):
    currentMountPath = '/mnt/' + str(counter)
    os.mkdir(currentMountPath)
    if drivesTormFSTYPE[i] == 'ntfs':
        os.system('/bin/ntfs-3g ' + drivesTormPATH[i] + ' ' + currentMountPath)
    else:
        os.system('/bin/mount ' + drivesTormPATH[i] + ' ' + currentMountPath)
    counter += 1

os.system('rm -rf /mnt/')

for i in os.listdir('/mnt/'):
    currentPartition = '/mnt/' + i
    os.system('/bin/unmount ' + currentPartition)

os.system('/sbin/reboot')
