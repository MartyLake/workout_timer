#python3
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import ttk
import os

CHROMA_KEY='#ff00ff'
DEFAULT_FONT="Verdana 20 bold"
INSTRUCTION_FILENAME="current_instruction.txt"
SUBINSTRUCTION_FILENAME="current_subinstruction.txt"
#example

def del_file(filePath):
   if os.path.exists(filePath):
       try:
            os.remove(filePath)
       except:
            print("Error while deleting file ", filePath)

class ExampleApp(tk.Frame):
    ''' An example application for TkInter.  Instantiate
        and call the run method to run. '''
    def __init__(self, master):
        del_file(INSTRUCTION_FILENAME)
        del_file(SUBINSTRUCTION_FILENAME)
        with open("workout.txt", mode='r', encoding="utf-8") as file_in:
            content = file_in.read().splitlines()
        with open("workout.preprocessed.txt", mode='w', encoding="utf-8") as file_out:
            for line_number, line in enumerate(content):
                if not line:
                    #already stripped
                    continue
                if line.startswith('#rep'):
                    #do something
                    line_sp = line.split(';')
                    x_exercices = int(line_sp[1])
                    x_repeat = int(line_sp[2])
                    print("At line {}, Repetition: série de {} exercices, répétés {} fois.".format(line_number, x_exercices, x_repeat))
                    exercises = []
                    for i in range(line_number + 1, line_number + 1 + x_exercices):
                        exercises.append(content[i])
                        content[i] = None #so we don't process twice
                    for i in range(x_repeat):
                        for exercise in exercises:
                            print("{}\\nRépétition{}/{}".format(exercise,i+1,x_repeat), file=file_out)
                    continue
                if line.startswith('#'):
                    print("WARNING at line {}, line starts with # but unknown verb. Using as is.")
                print(line, file=file_out)

        with open("workout.preprocessed.txt", mode='r', encoding="utf-8") as file_in:
            self.exercise_text = []
            self.exercise_subtext = []
            for line in file_in:
                line_sp = line.split(';', 1)
                line_sp[0] = line_sp[0].strip()
                if len(line_sp[0]) > 15:
                    print("WARNING, title too big: {}".format(line_sp[0]))
                self.exercise_text.append(line_sp[0])
                if len(line_sp) > 1:
                    line_sp[1] = line_sp[1].strip()
                    self.exercise_subtext.append(line_sp[1].replace('\\n', '\n'))
                else:
                    self.exercise_subtext.append("")

            self.workout_duration = len(self.exercise_text)*timedelta(seconds=30)


        # Initialize window using the parent's constructor
        tk.Frame.__init__(self,
                          master,
                          width=1280/2 + 210,
                          height=720/2,
                          background=CHROMA_KEY)

        # Set the title
        self.master.title('Workout Timer')

        # This allows the size specification to take effect
        self.pack_propagate(0)

        # We'll use the flexible pack layout manager
        self.pack()

        self.top_label = tk.Label(text="Workout", font="Verdana 30 bold", wraplength=390, justify='left')
        self.top_label.configure(background=CHROMA_KEY)
        self.instruction_label = tk.Label(text="", font=DEFAULT_FONT, wraplength=395, justify='left')
        self.instruction_label.configure(background=CHROMA_KEY)

        # The go button
        self.start_time = None
        self.go_button = tk.Button(self,
                                   text='Go',
                                   command=self.go_button_callback)
        self.go_button.configure(background=CHROMA_KEY)

        self.local_progress = ttk.Progressbar(orient='horizontal',length=100,mode='determinate')
        self.local_progress['value'] = 0
        self.global_progress = ttk.Progressbar(orient='horizontal',length=100,mode='determinate')
        self.global_progress['value'] = 0

        self.label = tk.Label(text="", font=DEFAULT_FONT)
        self.label.configure(background=CHROMA_KEY)
        self.local_label = tk.Label(text="", font=DEFAULT_FONT)
        self.local_label.configure(background=CHROMA_KEY)

        # Put the controls on the form
        # self.top_label.pack(fill=tk.X, side=tk.TOP)
        # self.local_label.pack(fill=tk.X, side=tk.TOP)
        self.top_label.place(x=10, y=0)
        self.instruction_label.place(x=0, y=100)

        self.go_button.pack(fill=tk.X, side=tk.BOTTOM)
        self.global_progress.pack(fill=tk.X, side=tk.BOTTOM)
        self.label.pack(fill=tk.X, side=tk.BOTTOM)
        self.local_progress.pack(fill=tk.X, side=tk.BOTTOM)
        self.local_label.pack(fill=tk.X, side=tk.BOTTOM)

        hours, remainder = divmod(self.workout_duration.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        total_minutes = int(minutes)
        total_seconds = int(seconds)
        now = "{:02d}:{:02d}/{:02d}:{:02d}".format(0,0, total_minutes, total_seconds)
        self.label.configure(text=now)

        now = "{:02d}:{:02d}".format(total_minutes, total_seconds)
        self.local_label.configure(text=now)
        # exercise text
        exercice_number=0
        self.update_instruction(self.exercise_text[exercice_number])
        self.update_sub_instruction(self.exercise_subtext[exercice_number])

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
        if self.start_time :
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
            exercice_number = int(exercice_number)

            if exercice_number >= len(self.exercise_text):
                self.local_progress['value'] = 100
                self.global_progress['value'] = 100
                self.go_button.configure(text="Done")
                self.label.configure(text="0")
                now = "{:02d}:{:02d}/{:02d}:{:02d}".format(total_minutes,total_seconds, total_minutes, total_seconds)
                self.label.configure(text=now)
                self.start_time=None
            else:
                seconds = 30 - seconds
                if seconds > 5:
                    seconds = int(seconds)
                else:
                    seconds = int(seconds * 10)/10.0
                now = "{}".format(seconds)
                self.local_label.configure(text=now)
                self.local_progress['value'] = 100 *  (30 - seconds) / 30
                # exercise text
                self.update_instruction(self.exercise_text[exercice_number])
                self.update_sub_instruction(self.exercise_subtext[exercice_number])
                # self.instruction_label.configure(text=self.exercise_instruction[exercise])
                next = ""
                if exercice_number+1 < len(self.exercise_text):
                    next = "Prochaine étape: {}".format(self.exercise_text[exercice_number+1])
                self.go_button.configure(text=next)

    def update_instruction(self, exercise):
        if not os.path.exists(INSTRUCTION_FILENAME) or self.top_label['text'] != exercise:
           self.top_label.configure(text=exercise)
           try:
             with open(INSTRUCTION_FILENAME, mode='w', encoding="utf-8") as file_out:
               print(exercise, file=file_out, end = '')
           except:
             print("Error cannot write into {}".format(INSTRUCTION_FILENAME))

    def update_sub_instruction(self, exercise):
        if not os.path.exists(SUBINSTRUCTION_FILENAME) or self.instruction_label['text'] != exercise:
           self.instruction_label.configure(text=exercise)
           try:
             with open(SUBINSTRUCTION_FILENAME, mode='w', encoding="utf-8") as file_out:
               print(exercise, file=file_out, end = '')
           except:
             print("Error cannot write into {}".format(SUBINSTRUCTION_FILENAME))

app = ExampleApp(tk.Tk())
app.mainloop()
