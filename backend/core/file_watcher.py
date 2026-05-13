import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CityFileHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_modified(self, event):
        if not event.is_directory:
            self.callback("MODIFIED", event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self.callback("CREATED", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self.callback("DELETED", event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            self.callback("MOVED", f"{event.src_path} -> {event.dest_path}")

class CityFileWatcher:
    """Step 51-75: Real-time file system watcher to eliminate polling."""
    def __init__(self, watch_dir, event_callback):
        self.watch_dir = os.path.abspath(watch_dir)
        self.event_callback = event_callback
        self.event_handler = CityFileHandler(self.event_callback)
        self.observer = Observer()

    def start(self):
        if not os.path.exists(self.watch_dir):
            os.makedirs(self.watch_dir)
        self.observer.schedule(self.event_handler, self.watch_dir, recursive=True)
        self.observer.start()
        print(f"[WATCHER] Monitoring {self.watch_dir}")

    def stop(self):
        self.observer.stop()
        self.observer.join()

if __name__ == "__main__":
    # Step 8: Natural Selection Test
    test_dir = os.path.join(os.getcwd(), "test_watch_zone")
    if not os.path.exists(test_dir): os.makedirs(test_dir)
    
    events_detected = []
    def test_callback(type, path):
        print(f"Event: {type} - {os.path.basename(path)}")
        events_detected.append(type)

    watcher = CityFileWatcher(test_dir, test_callback)
    watcher.start()
    
    time.sleep(1)
    print("Triggering OS Event: Creating file...")
    test_file = os.path.join(test_dir, "event_test.txt")
    with open(test_file, "w") as f: f.write("trigger")
    
    time.sleep(2) # Wait for event propagation
    watcher.stop()
    
    # Cleanup
    if os.path.exists(test_file): os.remove(test_file)
    if os.path.exists(test_dir): os.rmdir(test_dir)
    
    if "CREATED" in events_detected:
        print("Test Passed. Winner Selected.")
    else:
        print("Test Failed: No events detected.")
