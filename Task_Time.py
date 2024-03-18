#!/usr/bin/env python3

import os
import threading
import time
from datetime import datetime, timedelta
from pynput import mouse, keyboard
import logging
import subprocess

class ActivityMonitor:
    def __init__(self):
        # Initialize variables
        self.start_time = datetime.now()
        self.last_action_time = self.start_time
        self.active_time_seconds = 0
        self.inactive_time_seconds = 0
        self.total_active_time_seconds = 0
        self.total_inactive_time_seconds = 0
        self.logger = self.setup_logger()
        self.folder_path = "Task Time Registration"
        self.ensure_folder_exists()
        self.task_name = None
        self.file_path = None
        self.mouse_listener = mouse.Listener(on_move=self.on_move)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.inactivity_threshold = timedelta(minutes=5)
        self.update_interval = 60
        self.console_update_interval = 1
        self.is_monitoring = False

    def setup_logger(self):
        # Configure event logging
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        return logger
    
    def ensure_folder_exists(self):
        # Ensure the existence of the records folder
        os.makedirs(self.folder_path, exist_ok=True)

    def select_or_create_task(self):
        # Select or create a task
        tasks = [f.replace('.txt', '') for f in os.listdir(self.folder_path) if f.endswith('.txt')]
        print("\n========= NurSoftware - Task Time Registration ==========")
        print("\n===================== Tasks Menu =====================")
        print("n. Create a new task")
        for i, task in enumerate(tasks):
            print(f"{i+1}. {task}")
        if self.file_path:
            print(f"{len(tasks) + 1}. Open current file")
        while True:
            choice = input("Enter the task number or 'n' to create a new one: ")
            if choice == 'n':
                new_task_name = input("Enter the new task name: ").strip()
                return new_task_name
            elif choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(tasks):
                    return tasks[choice - 1]
                elif choice == len(tasks) + 1:
                    if self.file_path:
                        self.view_file()
                    else:
                        print("There is no current file.")
            print("Please enter a valid number or 'n'.")

    def read_existing_times(self):
        # Read existing activity times from a task file
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if line.startswith("Total Active Time:"):
                        self.total_active_time_seconds = self.parse_duration_to_seconds(line.split(":", 1)[1].strip())
                    elif line.startswith("Total Inactive Time:"):
                        self.total_inactive_time_seconds = self.parse_duration_to_seconds(line.split(":", 1)[1].strip())

    @staticmethod
    def parse_duration_to_seconds(duration_str):
        # Convert a duration string to seconds
        try:
            hours, minutes, seconds = [int(part) for part in duration_str.split(':')]
            return hours * 3600 + minutes * 60 + seconds
        except ValueError:
            print(f"Error parsing duration string '{duration_str}'. Make sure it is in the format 'HH:MM:SS'.")
            return 0
        
    def create_folder_and_file(self):
        # Create a folder and file for the current task
        self.file_path = os.path.join(self.folder_path, f"{self.task_name}.txt")
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as log_file:
                log_file.write("Start Date: {}\n".format(self.start_time.strftime('%Y-%m-%d Time: %H:%M:%S')))
                log_file.write("Last Activity: {}\n".format(self.start_time.strftime('%Y-%m-%d Time: %H:%M:%S')))
                log_file.write("Total Active Time: 0:0:0\n")
                log_file.write("Total Inactive Time: 0:0:0\n")
        else:
            self.read_existing_times()

    def on_move(self, x, y):
        # Handle mouse movement
        self.update_activity_time(datetime.now())

    def on_press(self, key):
        # Handle key press
        self.update_activity_time(datetime.now())

    def update_activity_time(self, current_time):
        # Update activity time
        elapsed_time = current_time - self.last_action_time
        if elapsed_time > self.inactivity_threshold:
            self.inactive_time_seconds += (elapsed_time - self.inactivity_threshold).total_seconds()
        self.active_time_seconds += min(elapsed_time, self.inactivity_threshold).total_seconds()
        self.last_action_time = current_time

    def format_seconds(self, seconds):
        # Format seconds into HH:MM:SS format
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)}:{int(minutes):02}:{int(seconds):02}"

    def print_timer(self):
        # Print active and inactive time
        while True:
            active_time_str = self.format_seconds(self.active_time_seconds)
            inactive_time_str = self.format_seconds(self.inactive_time_seconds)
            print(f"Active Time: {active_time_str} - Inactive Time: {inactive_time_str}", end="\r")
            time.sleep(1)

    def update_log_file(self):
        # Update the log file
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(f"Start Date: {self.start_time.strftime('%Y-%m-%d Time: %H:%M:%S')}\n")
            file.write(f"Last Activity: {datetime.now().strftime('%Y-%m-%d Time: %H:%M:%S')}\n")
            total_active_time = self.format_seconds(self.total_active_time_seconds + self.active_time_seconds)
            total_inactive_time = self.format_seconds(self.total_inactive_time_seconds + self.inactive_time_seconds)
            file.write(f"Total Active Time: {total_active_time}\n")
            file.write(f"Total Inactive Time: {total_inactive_time}\n")

    def start_update_timer(self):
        # Start timer for periodic update of log file
        threading.Timer(self.update_interval, self.periodic_update).start()

    def periodic_update(self):
        # Periodically update log file
        self.update_log_file()
        self.start_update_timer()

    def stop_monitoring(self):
        # Stop activity monitoring
        self.mouse_listener.stop()
        self.keyboard_listener.stop()
        self.update_log_file()
        self.is_monitoring = False
        print('\nMonitoring stopped. Press Ctrl+C to exit.')

    def view_file(self):
        # View the log file
        if os.name == 'nt':
            subprocess.call(['type', self.file_path], shell=True)
        else:
            subprocess.call(['cat', self.file_path])

    def start_monitoring(self):
        # Start activity monitoring
        self.is_monitoring = True
        self.logger.info("Starting activity monitoring.")
        self.task_name = self.select_or_create_task()
        self.create_folder_and_file()
        print(f"Starting monitoring for task: {self.task_name}")
        self.mouse_listener.start()
        self.keyboard_listener.start()
        threading.Thread(target=self.print_timer).start()
        self.start_update_timer()
        if self.file_path:
            self.view_file()
        while self.is_monitoring:
            time.sleep(self.console_update_interval)

if __name__ == "__main__":
    # Initialize and start the activity monitor
    monitor = ActivityMonitor()
    monitor.start_monitoring()
