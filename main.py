"""
FloatingMultiWindow - التطبيق الرئيسي
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.utils import platform

if platform == 'android':
    from android.permissions import request_permissions, Permission, check_permission
    from android import mActivity
    import shizuku_helper
    from jnius import autoclass


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)

        # العنوان
        self.add_widget(Label(
            text="Floating MultiWindow",
            font_size='24sp',
            size_hint_y=None,
            height=60,
            color=(0.4, 0.2, 0.8, 1)
        ))

        # حالة Shizuku
        self.shizuku_status = Label(
            text="جاري فحص Shizuku...",
            font_size='16sp',
            size_hint_y=None,
            height=40
        )
        self.add_widget(self.shizuku_status)

        # زر طلب الصلاحيات
        self.perm_btn = Button(
            text="1. طلب صلاحية الرسم فوق التطبيقات",
            size_hint_y=None,
            height=60,
            background_color=(0.3, 0.5, 0.9, 1)
        )
        self.perm_btn.bind(on_press=self.request_overlay_permission)
        self.add_widget(self.perm_btn)

        # زر تفعيل Shizuku
        self.shizuku_btn = Button(
            text="2. تفعيل Shizuku",
            size_hint_y=None,
            height=60,
            background_color=(0.9, 0.5, 0.2, 1)
        )
        self.shizuku_btn.bind(on_press=self.enable_shizuku)
        self.add_widget(self.shizuku_btn)

        # زر عرض التطبيقات
        self.apps_btn = Button(
            text="3. عرض التطبيقات المثبتة",
            size_hint_y=None,
            height=60,
            background_color=(0.2, 0.7, 0.4, 1)
        )
        self.apps_btn.bind(on_press=self.show_apps)
        self.add_widget(self.apps_btn)

        # منطقة عرض التطبيقات
        self.scroll = ScrollView()
        self.apps_grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.apps_grid.bind(minimum_height=self.apps_grid.setter('height'))
        self.scroll.add_widget(self.apps_grid)
        self.add_widget(self.scroll)

        # فحص Shizuku عند البداية
        Clock.schedule_once(self.check_shizuku, 1)

    def check_shizuku(self, dt):
        if platform != 'android':
            return
        if shizuku_helper.is_shizuku_ready():
            self.shizuku_status.text = "✅ Shizuku جاهز"
            self.shizuku_status.color = (0, 1, 0, 1)
        else:
            self.shizuku_status.text = "❌ Shizuku غير مفعّل"
            self.shizuku_status.color = (1, 0, 0, 1)

    def request_overlay_permission(self, *args):
        if platform != 'android':
            return
        request_permissions([Permission.SYSTEM_ALERT_WINDOW])

    def enable_shizuku(self, *args):
        if platform != 'android':
            return
        if shizuku_helper.request_shizuku_permission():
            self.shizuku_status.text = "⏳ انتظر الموافقة..."
        else:
            self.shizuku_status.text = "❌ Shizuku غير مثبت"

    def show_apps(self, *args):
        if platform != 'android':
            return
        self.apps_grid.clear_widgets()

        if not shizuku_helper.is_shizuku_ready():
            self.apps_grid.add_widget(Label(
                text="لازم تفعّل Shizuku الأول",
                color=(1, 0, 0, 1),
                size_hint_y=None,
                height=50
            ))
            return

        apps = shizuku_helper.get_installed_apps()
        for app in apps:
            btn = Button(
                text=app["name"],
                size_hint_y=None,
                height=50,
                background_color=(0.2, 0.2, 0.3, 1)
            )
            btn.bind(on_press=lambda x, p=app["package"]: self.launch_app(p))
            self.apps_grid.add_widget(btn)

    def launch_app(self, package_name):
        activity = shizuku_helper.get_main_activity(package_name)
        if not activity:
            print("❌ مفيش نشاط رئيسي")
            return

        ok, msg = shizuku_helper.launch_freeform(package_name, activity)
        print(f"{'✅' if ok else '❌'} {msg}")


class FloatingMultiWindowApp(App):
    def build(self):
        return MainScreen()


if __name__ == '__main__':
    FloatingMultiWindowApp().run()