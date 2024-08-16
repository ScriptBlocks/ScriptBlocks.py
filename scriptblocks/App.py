import os
import sys

class Objects:
    def __init__(self):
        self.objs = []

    def get(self):
        return self.objs

    def replaceAll(self, newObjs):
        self.objs = newObjs

    def add(self, obj):
        self.objs.append(obj)

    def remove(self, obj):
        self.objs.remove(obj)

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
        from PIL import Image
        import win32gui
        import win32con

        user32 = ctypes.WinDLL('user32', use_last_error=True)
        gdi32 = ctypes.WinDLL('gdi32', use_last_error=True)

        def wnd_proc(hwnd, msg, wparam, lparam):
            if msg == 0x0010:  # WM_CLOSE
                user32.PostQuitMessage(0)
            elif msg == 0x000F:  # WM_PAINT
                hdc = user32.GetDC(hwnd)
                self.__draw_sprites_windows(hdc)
                user32.ReleaseDC(hwnd, hdc)
            else:
                return user32.DefWindowProcW(hwnd, msg, wparam, lparam)
            return 0

        WNDPROCTYPE = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_int)
        WNDCLASS = wintypes.WNDCLASS()
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

    def __draw_sprites_windows(self, hdc):
        import ctypes
        from PIL import Image

        # Iterate over objects and draw the sprites
        for obj in self.objects.get():
            if obj["type"] == "Sprite" and obj["visible"]:
                img = Image.open(obj["image"])
                img = img.resize((obj["width"], obj["height"]))
                hdc_mem = ctypes.windll.gdi32.CreateCompatibleDC(hdc)
                hbitmap = Image.open(obj["image"]).tobitmap()
                ctypes.windll.gdi32.SelectObject(hdc_mem, hbitmap)
                ctypes.windll.gdi32.AlphaBlend(hdc, obj["posX"], obj["posY"], obj["width"], obj["height"], hdc_mem, 0, 0, obj["width"], obj["height"], 0)
                ctypes.windll.gdi32.DeleteObject(hbitmap)

    def __render_macos(self):
        import objc
        from Cocoa import NSApplication, NSWindow, NSWindowStyleMask, NSBackingStoreBuffered, NSRect, NSPoint, NSSize, NSImage, NSView

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

        # Set up a custom view for rendering sprites
        class CustomView(NSView):
            def drawRect_(self, rect):
                for obj in self.objects.get():
                    if obj["type"] == "Sprite" and obj["visible"]:
                        image = NSImage.alloc().initWithContentsOfFile_(obj["image"])
                        image.drawInRect_(NSRect(NSPoint(obj["posX"], obj["posY"]), NSSize(obj["width"], obj["height"])))

        view = CustomView.alloc().initWithFrame_(rect)
        window.setContentView_(view)

        app.run()

    def __render_linux(self):
        from Xlib import X, display
        from PIL import Image

        d = display.Display()
        root = d.screen().root

        window = root.create_window(100, 100, self.width, self.height, 2, d.screen().root_depth)
        window.set_wm_name(self.name)
        window.set_wm_class(self.name, self.name)
        window.map()

        if self.mode == "fullscreen":
            window.configure(width=d.screen().width_in_pixels, height=d.screen().height_in_pixels)
            window.change_property(d.intern_atom('_NET_WM_STATE', False),
                                   Xatom.ATOM, 32, [d.intern_atom('_NET_WM_STATE_FULLSCREEN', False)])

        elif self.mode == "fullscreen_windowed":
            window.configure(width=d.screen().width_in_pixels, height=d.screen().height_in_pixels)

        gc = window.create_gc()

        while True:
            event = d.next_event()
            if event.type == X.Expose:
                self.__draw_sprites_linux(window, gc, d)
            elif event.type == X.DestroyNotify:
                break  # Window closed

    def __draw_sprites_linux(self, window, gc, d):
        for obj in self.objects.get():
            if obj["type"] == "Sprite" and obj["visible"]:
                img = Image.open(obj["image"])
                img = img.resize((obj["width"], obj["height"]))

                # Convert the image to RGB and then to a format suitable for Xlib
                img = img.convert('RGB')
                data = img.tobytes("raw", "RGB")

                # Create an XImage
                ximage = d.display.screen().root.create_image(self.width, self.height, 24, X.ZPixmap, data)

                # Put the image on the window
                window.put_image(gc, ximage, 0, 0, obj["posX"], obj["posY"], obj["width"], obj["height"])

                # Clean up
                ximage.destroy()

    def getWinSize(self):
        return {"width": self.width, "height": self.height}