# mwatoi

**mwatoi** is a python-based project which can automatically extract WhatsApp chats from Android devices and copy them to an iPhone backup.

Before proceeding please check out the [known issues](#known-issues) and [notes](#notes) sections.

## Requirements

- Python 3+
- iTunes

## How to run

1. Install dependencies.
   - `pip install -r requirements.txt`

2. Start the transfer process:
   - `python main.py`

3. The script will guide you from now on.

## Can't get `msgstore.db` on Android?

This workaround consists in using an Android emulator, as it is easy to root it without messing up stuff on a real phone.

Steps 1 to 8 can be executed on either macOS or Windows, but for step 9 and on a Windows computer is required.

1. Download (or clone) the mwatoi repo to your computer.

2. Install the Android SDK.

3. Open the SDK, then create an Android emulator (plenty of tutorials online)
   - I used Pixel 5 with API 32.

4. Either directly from the SDK or from a terminal, start the emulator
   - `/Users/user/Library/Android/sdk/emulator/emulator -avd "Pixel_5_API_32"`
   - Now the emulated phone should pop up on your screen.

5. On your Android phone, make a complete backup of WhatsApp
   - Settings → Chats → Chat backup on Google Drive.

6. In the emulated phone, navigate to:
   - `https://www.apkmirror.com/apk/whatsapp-inc/whatsapp/whatsapp-2-22-8-78-release/whatsapp-messenger-2-22-8-78-android-apk-download/` 
   - Download and install the WhatsApp APK.
   - Alternatively, the apk is located under [mwatoi/bin/Whatsapp222878.apk](/bin/Whatsapp222878.apk)
   - Install it using via terminal `bin/adb.exe install -r -d Whatsapp222878.apk`

7. Once WhatsApp is installed
   1. Open the app
   2. Log in
   3. Restore WhatsApp from the Google Drive backup.

8. On the computer
   1. Start a new terminal
   2. Go to the mwatoi folder
   3. Get the data from WhatsApp as follows:
      1. `bin\adb.exe pull -a /storage/emulated/0/Android/media/com.whatsapp/WhatsApp/Databases/msgstore.db.crypt14`
      2. `bin\adb.exe root`
      3. `bin\adb.exe pull -a /data/data/com.whatsapp`
      4. `bin\adb.exe unroot`
      5. on macOS use `bin/adb` instead of `bin\adb.exe`

9. Copy the `msgstore.db` file you can find in `mwatoi/com.whatsapp/databases` into `mwatoi/out` and rename it `android.db`

10. Start the transfer process: `python main.py`
    - If needed install the dependencies with: `pip install -r requirements.txt`

11. Follow the instructions
    - The script should now tell you:
       - `Android backup file already exists. Path: out\android.db. Do you want to use the current backup? [y/n]`
       - Proceed with `y`

## Modified version of WhatsApp?

If you are using a modified version of WhatsApp such as *FMWhatsApp* and you cannot backup on Google Drive, here's the solution.

> **NOTE: This was only tested on FMWhatsApp (v9.30)**

1. Press the three dots in WhatsApp

2. Fouad MODS → General → Backup and Restore → Backup WhatsApp Data

3. Connect the phone to the computer and go to `/Android/media/com.whatsapp/
yoBackup/com.whatsapp/databases`

4. Copy the `msgstore.db` file to `mwatoi/out`
   - Rename `msgstore.db` to `android.db`

5. Start the transfer process: `python main.py`
    - If needed install the dependencies with: `pip install -r requirements.txt`

6. Follow the instructions
    - The script should now tell you:
       - `Android backup file already exists. Path: out\android.db. Do you want to use the current backup? [y/n]`
       - Proceed with `y`

## Known issues

- It can't copy media files.
- [Crash when connecting to WhatsApp Web](https://github.com/mukulkadel/mwatoi/issues/7)
  
## Notes

This project is tested only in a Windows environment.

Python versions it was tested with:

- `3.9.12`
- `3.10.4`

**Please make sure to do a complete Google Drive backup before connecting your Android device.**

### References

1. [residentsummer - watoi](https://github.com/residentsummer/watoi)
2. [EliteAndroidApps - WhatsApp Key DB Extractor](https://github.com/EliteAndroidApps/WhatsApp-Key-DB-Extractor)
3. [andreas-mausch - whatsapp-viewer](https://github.com/andreas-mausch/whatsapp-viewer)

### Contributors
<!-- DO NOT EDIT -->
![Contributors](https://contrib.rocks/image?repo=mukulkadel/mwatoi)
