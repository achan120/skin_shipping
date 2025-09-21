[app]

# (str) Title of your application
title = 发货助手

# (str) Package name
package.name = shippingapp

# (str) Package domain (needed for android/ios packaging)
package.domain = com.shippingapp

# (str) Source code where the main.py live
source.dir = .

# (str) Filename to the main.py
source.main = main_chinese.py

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,txt,docx

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,python-docx

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 30

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 23b

# (str) Android SDK version to use
android.sdk = 30

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = False

# (str) Android entry point, default is ok for Kivy-based app
android.entrypoint = org.kivy.android.PythonActivity

# (list) Pattern to whitelist for the whole project
android.whitelist = 

# (str) Path to a custom whitelist file
android.whitelist_src = 

# (str) Path to a custom blacklist file
android.blacklist_src = 

# (list) List of Java .jar files to add to the libs so they can be imported.
android.add_jars = 

# (list) List of Java files to add to the project (can be java or a directory containing the files)
android.add_src = 

# (list) Android AAR archives to add (currently works only with sdl2_gradle bootstrap)
android.gradle_dependencies = 

# (list) Gradle repositories (can be necessary for some android.gradle_dependencies)
android.gradle_repositories = 

# (str) python-for-android fork to use, defaults to upstream (kivy)
p4a.fork = kivy

# (str) python-for-android branch to use, defaults to master
p4a.branch = master

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
p4a.source_dir = 

# (str) The directory in which python-for-android should look for your own build recipes (if any)
p4a.local_recipes = 

# (str) Filename to the hook for p4a
p4a.hook = 

# (str) Bootstrap to use for android builds
p4a.bootstrap = sdl2

# (int) port number to specify an explicit --port= p4a argument (eg for bootstrap flask)
p4a.port = 

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .ipa) storage
bin_dir = ./bin
