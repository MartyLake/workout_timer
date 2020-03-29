#python3
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import ttk

DEFAULT_FONT="Verdana 30 bold"
#example

class ExampleApp(tk.Frame):
    ''' An example application for TkInter.  Instantiate
        and call the run method to run. '''
    def __init__(self, master):
        with open("workout.txt") as file_in:
            self.exercise_text = []
            for line in file_in:
                self.exercise_text.append(line)
            self.workout_duration = len(self.exercise_text)*timedelta(seconds=30)


        # Initialize window using the parent's constructor
        tk.Frame.__init__(self,
                          master,
                          width=720,
                          height=480)
        # Set the title
        self.master.title('Workout Timer')

        # This allows the size specification to take effect
        self.pack_propagate(0)

        # We'll use the flexible pack layout manager
        self.pack()

        self.top_label = tk.Label(text="Workout", font="Verdana 50 bold")
        self.instruction_label = tk.Label(text="", font=DEFAULT_FONT)

        # The recipient text entry control and its StringVar
        self.recipient_var = tk.StringVar()
        self.recipient = tk.Entry(self,
                                  textvariable=self.recipient_var,
                                  font=DEFAULT_FONT)
        self.recipient_var.set('world')

        # The go button
        self.start_time = None
        self.go_button = tk.Button(self,
                                   text='Go',
                                   command=self.go_button_callback)

        self.local_progress = ttk.Progressbar(orient='horizontal',length=100,mode='determinate')
        self.local_progress['value'] = 0
        self.global_progress = ttk.Progressbar(orient='horizontal',length=100,mode='determinate')
        self.global_progress['value'] = 0

        self.label = tk.Label(text="", font=DEFAULT_FONT)
        self.local_label = tk.Label(text="", font=DEFAULT_FONT)

        # Put the controls on the form
        # self.top_label.pack(fill=tk.X, side=tk.TOP)
        # self.local_label.pack(fill=tk.X, side=tk.TOP)
        self.top_label.place(x=10, y=10)
        self.instruction_label.place(x=10, y=120)

        self.go_button.pack(fill=tk.X, side=tk.BOTTOM)
        self.global_progress.pack(fill=tk.X, side=tk.BOTTOM)
        self.label.pack(fill=tk.X, side=tk.BOTTOM)
        self.local_progress.pack(fill=tk.X, side=tk.BOTTOM)
        self.local_label.pack(fill=tk.X, side=tk.BOTTOM)

        # self.recipient.pack(fill=tk.X, side=tk.TOP)

        self.update()

    def go_button_callback(self):
        ''' Print a greeting constructed
            from the selections made by
            the user. '''
        if not self.start_time:
            self.start_time = datetime.now()
        else:
            self.start_time = self.start_time - timedelta(seconds=15)

    def update(self):
        # reschedule update callback
        self.after(50, self.update)
        ''' Update loop '''
        if not self.start_time :
            now = "Ready?"
            self.label.configure(text=now)
            self.local_label.configure(text=now)
        else:
            time = datetime.now() - self.start_time
            # total time
            hours, remainder = divmod(time.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            now_minutes = int(minutes)
            now_seconds = int(seconds)

            hours, remainder = divmod(self.workout_duration.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            total_minutes = int(minutes)
            total_seconds = int(seconds)

            now = "{:02d}:{:02d}/{:02d}:{:02d}".format(now_minutes,now_seconds, total_minutes, total_seconds)
            self.label.configure(text=now)
            self.global_progress['value'] = time.total_seconds() / self.workout_duration.total_seconds() * 100

            # exercise time
            exercice_number, seconds = divmod(time.total_seconds(), 30)
            seconds = 30 - seconds
            if seconds > 5:
                seconds = int(seconds)
            else:
                seconds = int(seconds * 10)/10.0
            now = "{}".format(seconds)
            self.local_label.configure(text=now)
            self.local_progress['value'] = 100 *  (30 - seconds) / 30
            # exercise text
            exercise = self.exercise_text[int(exercice_number)]
            self.top_label.configure(text=exercise)
            # self.instruction_label.configure(text=self.exercise_instruction[exercise])

app = ExampleApp(tk.Tk())
app.mainloop()
