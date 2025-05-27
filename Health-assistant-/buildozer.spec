[app]
title = Hospital Health Assistant
package.name = hospitalhealthassistant
package.domain = org.hospitalhealthassistant
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,csv
version = 1.0

requirements = python3,kivy,pandas,google-generativeai

orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.arch = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1 