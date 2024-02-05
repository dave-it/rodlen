import time
import json
import threading

class TimerThread(threading.Thread):
    def __init__(self, duration, athlete_data):
        super().__init__()
        self.duration = duration
        self.athlete_data = athlete_data
        self.timer_running = True
        self.start_time = None

    def run(self):
        self.start_time = time.time()
        while self.timer_running:
            elapsed_time = time.time() - self.start_time
            minutes, seconds = divmod(int(elapsed_time), 60)
            self.update_timer_data(minutes, seconds)
            time.sleep(1)

            if elapsed_time >= self.duration:
                break

        print("Timer completed!")

    def update_timer_data(self, minutes, seconds):
        flat_athlete_data = {
            'time': f"{minutes}:{seconds:02d}",
            **self.athlete_data
        }
        timer_data = []
        timer_data.append(flat_athlete_data)
        with open("timer_data.json", 'w') as json_file:
            json.dump(timer_data, json_file)

    def stop_timer(self):
        self.timer_running = False

def start_timer(duration, athlete_data):
    timer_thread = TimerThread(duration, athlete_data)
    timer_thread.start()
    return timer_thread

def stop_timer(timer_thread):
    timer_thread.stop_timer()
    timer_thread.join()