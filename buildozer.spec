[app]
title = Floating MultiWindow
package.name = floatingmultiwindow
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

requirements = python3,kivy,pyjnius,android

# صلاحيات أندرويد
android.permissions = SYSTEM_ALERT_WINDOW,FOREGROUND_SERVICE,QUERY_ALL_PACKAGES,PACKAGE_USAGE_STATS

# إصدار أندرويد الأدنى
android.minapi = 24
android.api = 33

# الخدمة
services = Bubble:bubble.py

# إعدادات أخرى
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True