"""
خدمة الفقاعة العائمة اللي بتفضل شغالة في الخلفية
"""
from android import mActivity
from jnius import autoclass, cast, PythonJavaClass, java_method
from kivy.utils import platform
import time

if platform == 'android':
    Service = autoclass('org.kivy.android.PythonService')
    WindowManager = autoclass('android.view.WindowManager')
    WindowManagerLayoutParams = autoclass('android.view.WindowManager$LayoutParams')
    Gravity = autoclass('android.view.Gravity')
    PixelFormat = autoclass('android.graphics.PixelFormat')
    ImageView = autoclass('android.widget.ImageView')
    LinearLayout = autoclass('android.widget.LinearLayout')
    Color = autoclass('android.graphics.Color')
    Gravity = autoclass('android.view.Gravity')


def start_bubble():
    """إنشاء الفقاعة العائمة"""
    context = mActivity.getApplicationContext()

    # الحصول على WindowManager
    wm = cast(WindowManager, context.getSystemService(context.WINDOW_SERVICE))

    # إعدادات الفقاعة
    params = WindowManagerLayoutParams(
        WindowManagerLayoutParams.WRAP_CONTENT,
        WindowManagerLayoutParams.WRAP_CONTENT,
        WindowManagerLayoutParams.TYPE_APPLICATION_OVERLAY,
        WindowManagerLayoutParams.FLAG_NOT_FOCUSABLE,
        PixelFormat.TRANSLUCENT
    )
    params.gravity = Gravity.TOP | Gravity.START
    params.x = 100
    params.y = 200

    # إنشاء الفقاعة (دائرة ملونة مؤقتًا)
    bubble = ImageView(context)
    bubble.setBackgroundColor(Color.parseColor("#6200EE"))

    # حجم الفقاعة
    size = 120
    bubble.setLayoutParams(
        LinearLayout.LayoutParams(size, size)
    )

    # إضافة الفقاعة للشاشة
    wm.addView(bubble, params)

    print("✅ الفقاعة اشتغلت")
    return wm, bubble, params