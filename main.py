import os
_lsblkOutputPATH = os.popen('/bin/lsblk -o PATH')
_lsblkOutputTYPE = os.popen('/bin/lsblk -o FSTYPE')
lsblkOutputPATH = _lsblkOutputPATH.read().split('\n')
lsblkOutputFSTYPE = _lsblkOutputTYPE.read().split('\n')

drivesToShredPATH = []
drivesToShredFSTYPE = []
for i in range(len(lsblkOutputPATH)-1):
    if str(lsblkOutputPATH[i])[-1:].isdigit() and not('loop' in str(lsblkOutputPATH[i])) and not('sr' in str(lsblkOutputPATH[i])):
        drivesToShredPATH.append(lsblkOutputPATH[i])
        drivesToShredFSTYPE.append(lsblkOutputFSTYPE[i])

counter = 0
for i in range(len(drivesToShredPATH)):
    currentMountPath = '/mnt/' + str(counter)
    os.mkdir(currentMountPath)
    if drivesToShredFSTYPE[i] == 'ntfs':
        os.system('/bin/ntfs-3g ' + drivesToShredPATH[i] + ' ' + currentMountPath)
    else:
        os.system('/bin/mount ' + drivesToShredPATH[i] + ' ' + currentMountPath)
    counter += 1

for root, dirs, files in os.walk('/mnt/'):
    for file in files:
        currentFile = os.path.join(root, file)
        os.system('shred -f -n 8 -u -z ' + currentFile)

for i in os.listdir('/mnt/'):
    currentPartition = '/mnt/' + i
    os.system('/bin/unmount ' + currentPartition)

os.system('/sbin/reboot')