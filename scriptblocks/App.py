from .Objects import Objects
import os
import sys

class App:
    def __init__(self, width=800, height=600, mode="windowed"):
        self.name = "Unnamed App"
        self.version = "v1.0.0"
        self.developer = "Unknown"
        self.icon = {
            "16x16": "assets/logos/16x16.png",
            "32x32": "assets/logos/32x32.png",
            "64x64": "assets/logos/64x64.png",
            "128x128": "assets/logos/128x128.png",
            "256x256": "assets/logos/256x256.png"
        }
        self.objects = Objects()
        self.width = width
        self.height = height
        self.mode = mode.lower()
        self.os_name = os.name

    def render(self):
        if self.os_name == "nt":  # Windows
            self.__render_windows()
        elif self.os_name == "posix":
            if sys.platform == "darwin":  # macOS
                self.__render_macos()
            else:  # Linux and other Unix-like systems
                self.__render_linux()
        else:
            raise NotImplementedError("Unsupported operating system")

    def __render_windows(self):
        import ctypes
        from ctypes import wintypes

        user32 = ctypes.WinDLL('user32', use_last_error=True)

        def wnd_proc(hwnd, msg, wparam, lparam):
            if msg == 0x0010:  # WM_CLOSE
                user32.PostQuitMessage(0)
            else:
                return user32.DefWindowProcW(hwnd, msg, wparam, lparam)
            return 0

        WNDPROCTYPE = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_int)
        WNDCLASS = ctypes.WINFUNCTYPE(wintypes.HWND, wintypes.HINSTANCE, wintypes.LPCWSTR, WNDPROCTYPE, wintypes.HINSTANCE, wintypes.HWND, wintypes.HBRUSH, wintypes.HCURSOR, wintypes.HICON, wintypes.LPCWSTR, wintypes.LPCWSTR)
        WNDCLASS.lpszClassName = 'MyWindowClass'
        WNDCLASS.lpfnWndProc = WNDPROCTYPE(wnd_proc)
        WNDCLASS.hInstance = user32.GetModuleHandleW(None)

        if not user32.RegisterClassW(ctypes.byref(WNDCLASS)):
            raise ctypes.WinError(ctypes.get_last_error())

        style = 0xcf0000  # WS_OVERLAPPEDWINDOW
        if self.mode == "fullscreen":
            style = 0x80000000  # WS_POPUP
            self.width, self.height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        elif self.mode == "fullscreen_windowed":
            style = 0xcf0000  # WS_OVERLAPPEDWINDOW
            self.width, self.height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

        hwnd = user32.CreateWindowExW(0, WNDCLASS.lpszClassName, self.name, style, 100, 100, self.width, self.height, None, None, WNDCLASS.hInstance, None)
        if not hwnd:
            raise ctypes.WinError(ctypes.get_last_error())

        user32.ShowWindow(hwnd, 1)
        user32.UpdateWindow(hwnd)

        msg = wintypes.MSG()
        while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))

    def __render_macos(self):
        import objc
        from Cocoa import NSApplication, NSWindow, NSWindowStyleMask, NSBackingStoreBuffered, NSRect, NSPoint, NSSize

        app = NSApplication.sharedApplication()

        rect = NSRect(NSPoint(100, 100), NSSize(self.width, self.height))
        style_mask = NSWindowStyleMask.titled | NSWindowStyleMask.closable | NSWindowStyleMask.resizable
        if self.mode == "fullscreen":
            rect = NSRect(NSPoint(0, 0), NSSize(self.width, self.height))
            style_mask = NSWindowStyleMask.fullScreen
        elif self.mode == "fullscreen_windowed":
            rect = NSRect(NSPoint(0, 0), NSSize(self.width, self.height))
            style_mask = NSWindowStyleMask.titled | NSWindowStyleMask.closable | NSWindowStyleMask.resizable

        window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            rect, 
            style_mask,
            NSBackingStoreBuffered,
            False
        )

        window.setTitle_(self.name)
        window.makeKeyAndOrderFront_(None)

        app.run()

    def __render_linux(self):
        from Xlib import X, display

        d = display.Display()
        root = d.screen().root

        window = root.create_window(100, 100, self.width, self.height, 2, d.screen().root_depth)
        window.set_wm_name(self.name)
        window.map()

        if self.mode == "fullscreen":
            window.configure(width=d.screen().width_in_pixels, height=d.screen().height_in_pixels)
            window.set_wm_state('_NET_WM_STATE_FULLSCREEN')

        elif self.mode == "fullscreen_windowed":
            window.configure(width=d.screen().width_in_pixels, height=d.screen().height_in_pixels)

        while True:
            event = d.next_event()
            if event.type == X.Expose:
                pass  # Redraw window
            elif event.type == X.DestroyNotify:
                break  # Window closed

    def getWinSize(self):
        return {"width": self.width, "height": self.height}