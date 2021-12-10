import os
import tarfile
import shutil

print('WhatsApp android to ios converter')
idb = input("Enter ios db path: ")
uid = input("Enter phone number with country code, eg: 9185XXXXXXXX: ")
if not os.path.exists('bin'):
    print('bin directory not found!')
    exit(1)

print('Creating tmp directory')
if not os.path.exists('tmp'):
    os.mkdir('tmp')

print('Please connect your Android device with USB Debugging enabled:')
os.system('bin\\adb.exe kill-server')
os.system('bin\\adb.exe start-server')
os.system('bin\\adb.exe wait-for-device')

print('Uninstalling current apk')
os.system('bin\\adb.exe shell pm uninstall -k com.whatsapp')

print('Installing WhatsApp 2.11.431')
os.system('bin\\adb.exe install -r -d bin\LegacyWhatsApp.apk')
print('Installation complete!')

print('Backing up data.')
os.system('bin\\adb.exe backup -f tmp\whatsapp.ab com.whatsapp')

print('Extracting .ab file.')
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

print('Creating out directory')
if not os.path.exists('out'):
    os.mkdir('out')

print('Copying ecryption key')
shutil.copyfile('tmp\\apps\\com.whatsapp\\f\\key','out\\key')
print('Copying android db')
shutil.copyfile('tmp\\apps\\com.whatsapp\\db\\msgstore.db','out\\android.db')

print('Starting migration script.')
os.system('python migrate.py -adb out\\android.db -idb {} -u {}'.format(idb,uid))
print('Cleaning up...')
print('Deleting tmp directory.')
shutil.rmtree('tmp')
print('Stopping adb.')
os.system('bin\\adb.exe kill-server')
print("\n\nios db path: out\\out.db")