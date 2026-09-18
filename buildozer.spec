[app]
title = Floating MultiWindow
package.name = floatingmultiwindow
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

requirements = python3,kivy,pyjnius,android

orientation = portrait
fullscreen = 0

android.permissions = SYSTEM_ALERT_WINDOW,FOREGROUND_SERVICE,QUERY_ALL_PACKAGES
android.api = 33
android.minapi = 24
android.archs = arm64-v8a,armeabi-v7a
android.accept_sdk_license = True
android.ndk = 25b

[buildozer]
log_level = 2
warn_on_root = 1
