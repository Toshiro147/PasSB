import time
import sys
import os
import threading
import subprocess

class Watcher:
    def __init__(self, controller, interval=1.5):
        self.controller = controller
        self.interval = interval
        self.running = True
        self.last_window = ""
        self.salt_path = "vault_data/.salt"

    def start(self):
        usb_thread = threading.Thread(target=self._usb_sensor, daemon=True)
        usb_thread.start()
        window_thread = threading.Thread(target=self._window_listener, daemon=True)
        window_thread.start()

    def _usb_sensor(self):
        while self.running:
            if not os.path.exists(self.salt_path):
                print("USB Çıkarıldı! Acil Kapanış.")
                self.controller.force_close()
                sys.exit(0)
            time.sleep(1)

    def _window_listener(self):
        while self.running:
            current_window = self._get_active_window_title_mac()
            if current_window and current_window != self.last_window:
                self.last_window = current_window
                print(f"Aktif Pencere: {current_window}")
                self.controller.check_match(current_window)
            
            time.sleep(self.interval)

    def _get_active_window_title_mac(self):
        try:
            cmd_app = 'tell application "System Events" to get name of first application process whose frontmost is true'
            app_name = subprocess.check_output(['osascript', '-e', cmd_app]).decode().strip()
            cmd_title = f'tell application "System Events" to tell process "{app_name}" to get name of front window'
            window_title = subprocess.check_output(['osascript', '-e', cmd_title], stderr=subprocess.DEVNULL).decode().strip()
            
            return f"{app_name} - {window_title}"
        except:
            return None

    def stop(self):
        self.running = False