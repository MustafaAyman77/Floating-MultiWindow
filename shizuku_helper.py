"""
التعامل مع Shizuku عبر pyjnius
"""
from jnius import autoclass, cast
from android import mActivity

# استيراد كلاسات Shizuku
try:
    Shizuku = autoclass('moe.shizuku.api.Shizuku')
    ShizukuProvider = autoclass('moe.shizuku.api.ShizukuProvider')
    SHIZUKU_AVAILABLE = True
except Exception:
    SHIZUKU_AVAILABLE = False


def is_shizuku_ready():
    """التأكد إن Shizuku شغال ومسموح للتطبيق"""
    if not SHIZUKU_AVAILABLE:
        return False
    try:
        return Shizuku.pingBinder()
    except Exception:
        return False


def request_shizuku_permission():
    """طلب إذن Shizuku من المستخدم"""
    if not SHIZUKU_AVAILABLE:
        return False
    try:
        Shizuku.requestPermission(0)  # requestCode
        return True
    except Exception as e:
        print(f"فشل طلب الإذن: {e}")
        return False


def launch_freeform(package_name, activity_name):
    """
    تشغيل تطبيق في وضع Freeform (نافذة عائمة حرة)
    windowingMode = 5 يعني Freeform
    """
    if not is_shizuku_ready():
        return False, "Shizuku مش شغال"

    try:
        # الأمر اللي هننفذه عبر Shizuku
        cmd = [
            "am", "start",
            "--windowingMode", "5",
            "-n", f"{package_name}/{activity_name}"
        ]

        # تحويل القائمة لمصفوفة Java String
        String = autoclass('java.lang.String')
        java_cmd = [String(c) for c in cmd]

        # تنفيذ الأمر عبر Shizuku
        process = Shizuku.newProcess(java_cmd, None, None)
        exit_code = process.waitFor()

        if exit_code == 0:
            return True, "تم التشغيل"
        else:
            return False, f"فشل التنفيذ (كود {exit_code})"
    except Exception as e:
        return False, f"خطأ: {str(e)}"


def get_installed_apps():
    """جلب قائمة التطبيقات المثبتة"""
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    PackageManager = autoclass('android.content.pm.PackageManager')

    activity = PythonActivity.mActivity
    pm = activity.getPackageManager()

    # جلب كل التطبيقات
    apps = pm.getInstalledApplications(PackageManager.GET_META_DATA)

    result = []
    for app in apps:
        # تجاهل تطبيقات النظام
        if pm.getLaunchIntentForPackage(app.packageName) is None:
            continue

        app_name = app.loadLabel(pm).toString()
        result.append({
            "name": app_name,
            "package": app.packageName
        })

    return sorted(result, key=lambda x: x["name"])


def get_main_activity(package_name):
    """جلب اسم النشاط الرئيسي لتطبيق معين"""
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    activity = PythonActivity.mActivity
    pm = activity.getPackageManager()
    intent = pm.getLaunchIntentForPackage(package_name)
    if intent:
        component = intent.getComponent()
        return component.getClassName()
    return None