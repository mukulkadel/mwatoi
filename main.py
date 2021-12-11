import os
import tarfile
import shutil
import sqlite3

req_file_list = {'bin': ['adb.exe', 'AdbWinApi.dll','AdbWinUsbApi.dll','LegacyWhatsApp.apk'],'.':['migrate.py']}
iphone_backup_root_loc = os.getenv('APPDATA')+'\\Apple Computer\\MobileSync\\Backup'

print('\nWhatsApp android to ios transferrer\n')

for dirname in req_file_list:
    for filename in req_file_list[dirname]:
        path = os.path.join(dirname,filename)
        if not os.path.exists(path):
            print('Missing: {}, terminating!'.format(path))
            exit(1)

use_android_backup = False

if os.path.exists('out\\android.db'):
    print('Android backup file already exists. Path: out\\android.db')
    use_android_backup = input('Do you want to use the current backup? [y/n]: ').upper() == 'Y'

if not use_android_backup:
    print('Please connect your Android device with USB Debugging enabled:')
    os.system('bin\\adb.exe kill-server')
    os.system('bin\\adb.exe start-server')
    os.system('bin\\adb.exe wait-for-device')

    print('\nAndroid device connected!\n')

    print('***********************************************')
    print('Please backup all your whatsapp chats before proceeding.')
    print('***********************************************')
    inp = input('\nDo you want to continue?[y/n]: ')
    if inp.upper() != 'Y':
        print('Exiting.')
        exit()

    print('\nStarting backup process.')

    if not os.path.exists('tmp'):
        print('Creating tmp directory.')
        os.mkdir('tmp')

    print('Uninstalling current apk.')
    os.system('bin\\adb.exe shell pm uninstall -k com.whatsapp')

    print('Installing WhatsApp 2.11.431.')
    os.system('bin\\adb.exe install -r -d bin\\LegacyWhatsApp.apk')
    print('Installation complete!')

    print('Backing up data.')
    print('\nNote: Please don\'t enter any password.\n')
    os.system('bin\\adb.exe backup -f tmp\\whatsapp.ab com.whatsapp')

    print('Extracting tmp\\whatsapp.ab file.')
    with open('tmp/whatsapp.ab','rb') as inp:
        with open('tmp/whatsapp.tar','wb') as out:
            out.write(b'\x1f\x8b\x08\x00\x00\x00\x00\x00')
            inp.read(24)
            while True:
                b = inp.read(512)
                if not b:
                    break
                out.write(b)

    with tarfile.open('tmp\whatsapp.tar') as tp:
        tp.extractall(path='tmp')

    print('Creating out directory.')
    if not os.path.exists('out'):
        os.mkdir('out')

    print('Copying android db')
    shutil.copyfile('tmp\\apps\\com.whatsapp\\db\\msgstore.db','out\\android.db')
    print('Cleaning up...')
    print('Deleting tmp directory.')
    shutil.rmtree('tmp')
    print('Stopping adb.')
    os.system('bin\\adb.exe kill-server')


    print('\nYou can now safely remove your android device.')
print('\nPlease follow below steps to restore whatsapp backup to your iphone:')
print('\t1. Login into whatsapp with the same number in your iphone.')
print('\t   If already logged in, script will preverse iphone chats also.')
print('\n\t2. Disable \'Find My iPhone\' option in your iphone.')
print('\n\t3. Create an unencrypted local backup using iTunes.')

input('Press enter to conitnue...')
print('Looking for iphone backup.')

if not os.path.exists(iphone_backup_root_loc):
    print('Backup directory is missing.')
    exit(2)

dirnames = os.listdir(iphone_backup_root_loc)
if len(dirnames)==0:
    print('No backup found.')
    exit(3)
elif len(dirnames)>1:
    print('Multiple backups found.')
    iphone_backup_loc = input('Please enter backup folder path: ')
else:
    iphone_backup_loc = os.path.join(iphone_backup_root_loc,dirnames[0])

manifest_db_path = os.path.join(iphone_backup_loc,'Manifest.db')
if not os.path.exists(manifest_db_path):
    print('Manifest.db is missing.')
    exit(4)

print('Looking for whatsapp data in iphone backup.')
manifest_db = sqlite3.connect(manifest_db_path)

chatstorge = list(manifest_db.execute("SELECT fileID FROM Files WHERE relativePath LIKE 'ChatStorage.sqlite'"))
if len(chatstorge)!=1:
    print('Error finding whatsapp data. Terminating!')
    exit(5)

chatstorge_path = os.path.join(iphone_backup_loc,chatstorge[0][0][:2],chatstorge[0][0])

shutil.copyfile(chatstorge_path,'out\\ios.db')
print('Backup copied.\n')
uid = input("Enter phone number with country code, eg: 9185XXXXXXXX: ")
print('Starting migration script.')
os.system('python migrate.py -adb out\\android.db -idb out\\ios.db -u {}'.format(uid))

print('Migration complete!')
print('Updating iphone backup')
shutil.copyfile('out\\out.db',chatstorge_path)
print('Deleting out directory.')
shutil.rmtree('out')
print('\n\t4. Restore local backup and start the whatsapp.')
print('\n\n\t   Note: To fix any buggy behaviour after the restoration, backup iphone whatsapp to icloud and reinstall it.')