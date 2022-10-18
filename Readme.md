# About

**mwatoi** is a python-based project which can automatically extract WhatsApp chats from android devices and copy them to an iPhone backup.

*Note:* It can't copy media files.

This project is tested only in windows environment.

# Prerequisite

1. python3

# How to run

1. Installing dependencies.

    `> pip install -r requirements.txt`

2. Starting transfer process:

    `> python main.py`



# mwatoi workaround by @dtiziano



# How, after many hours of struggle, I finally managed to port whatsapp messages from android to iPhone
This workaround consists in using an Android emulator, as it is easy to root it without messing up stuff on a real phone.

0-8 can either be executed on mac or windows, but for 9 you will need a windows computer

0. Download the mwatoi repo to your computer 

1. Install the android SDK 

2. Open the SDK, then create an Android emulator (plenty of tutorials online), I used Pixel 5 with API 32.

3. Either directly from the SDK or from a terminal, start the emulator `> /Users/user/Library/Android/sdk/emulator/emulator -avd "Pixel_5_API_32"`
Now the emulated phone should pop up on your screen.

4. On your Android phone, make a complete backup of Whatsapp (Settings -> Chats -> Chat backup) on Google Drive.

5. In the emulated phone, navigate to https://www.apkmirror.com/apk/whatsapp-inc/whatsapp/whatsapp-2-22-8-78-release/whatsapp-messenger-2-22-8-78-android-apk-download/ and 
download and install the Whatsapp apk. Alternatively, the apk is located under mwatoi/bin (I added the apk file in the new branch and also adb file that can be run on mac (although the resoring part of the iphone only works on windows), let's see if it gets forked), and is called Whatsapp222878.apk.  Install it using via terminal `> bin/adb.exe install -r -d Whatsapp222878.apk`

6. Once Whatsapp is installed, run it, log-in, and restore Whatsapp from the Google Drive backup.

7. On the computer, start a new terminal and 'cd' to the mwatoi folder, and get the data from Whatsapp as follows 
(On windows, of course use `bin\adb.exe`)
`> bin/adb pull -a /storage/emulated/0/Android/media/com.whatsapp/WhatsApp/Databases/msgstore.db.crypt14`

`> bin/adb root`

`> bin/adb pull -a /data/data/com.whatsapp`

`> bin/adb unroot`


8. Copy the msgstore.db file you can find in mwatoi/com.whatsapp/databases on your computer into mwatoi/out and rename it android.db

9. Run the mwatoi main script, and follow the instructions (the script should now tell you: Android backup file already exists. Path: out\\android.db. Do you want to use the current backup? [y/n]:. Proceed with y)
To run it 'python main.py'

# mwatoi workaround ENDby @dtiziano


# References

1. https://github.com/residentsummer/watoi
2. https://github.com/EliteAndroidApps/WhatsApp-Key-DB-Extractor
3. https://github.com/andreas-mausch/whatsapp-viewer


# Notes
- My python version: 3.9.12
- Please make sure to take complete google drive backup before connecting your android device.
