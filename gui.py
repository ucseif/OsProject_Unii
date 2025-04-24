import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import os


class ModernProcessSchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced CPU Process Scheduler")
        self.root.state('zoomed')  # Start maximized but can be resized

        self.colors = {
            'bg': '#1E293B',
            'fg': '#E2E8F0',
            'accent': '#60A5FA',
            'success': '#34D399',
            'warning': '#F87171',
            'chart_bg': '#334155'
        }

        self.root.configure(bg=self.colors['bg'])

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.style.configure('Main.TFrame', background=self.colors['bg'])
        self.style.configure('Controls.TLabelframe',
                             background=self.colors['bg'],
                             foreground=self.colors['fg'])
        self.style.configure('Controls.TLabelframe.Label',
                             font=('Segoe UI', 11),
                             background=self.colors['bg'],
                             foreground=self.colors['fg'])
        self.style.configure('Modern.TLabel',
                             font=('Segoe UI', 10),
                             background=self.colors['bg'],
                             foreground=self.colors['fg'])
        self.style.configure('Modern.TButton',
                             font=('Segoe UI', 10),
                             padding=5)

        self.create_main_layout()
        self.load_process_data()

    def create_main_layout(self):
        main_frame = ttk.Frame(self.root, padding=10, style='Main.TFrame')
        main_frame.grid(row=0, column=0, sticky="nsew")

        control_frame = ttk.LabelFrame(main_frame, text="Scheduling Controls",
                                       padding=15, style='Controls.TLabelframe')
        control_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        ttk.Label(control_frame, text="Select Algorithm:",
                  style='Modern.TLabel').grid(row=0, column=0, pady=10, sticky='w')
        self.algorithm_var = tk.StringVar(value="FCFS")
        algorithms = ["FCFS - First Come First Serve",
                      "RR - Round Robin",
                      "SRTF - Shortest Remaining Time First",
                      "SJF - Shortest Job First",
                      "HPF - Highest Priority First"]
        self.algorithm_combo = ttk.Combobox(control_frame,
                                            textvariable=self.algorithm_var,
                                            values=algorithms,
                                            state="readonly",
                                            width=30,
                                            font=('Segoe UI', 10))
        self.algorithm_combo.grid(row=0, column=1, pady=10, padx=5, sticky='w')

        ttk.Label(control_frame, text="Time Quantum (RR):",
                  style='Modern.TLabel').grid(row=1, column=0, pady=10, sticky='w')
        self.quantum_var = tk.StringVar(value="2")
        self.quantum_entry = ttk.Entry(control_frame,
                                       textvariable=self.quantum_var,
                                       width=10,
                                       font=('Segoe UI', 10))
        self.quantum_entry.grid(row=1, column=1, pady=10, padx=5, sticky='w')

        run_button = ttk.Button(control_frame,
                                text="▶ Run Simulation",
                                command=self.run_simulation,
                                style='Modern.TButton')
        run_button.grid(row=2, column=0, columnspan=2, pady=15)

        results_frame = ttk.LabelFrame(main_frame, text="Simulation Results",
                                       padding=15, style='Controls.TLabelframe')
        results_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        self.stats_frame = ttk.Frame(results_frame, style='Main.TFrame')
        self.stats_frame.grid(row=0, column=0, pady=10)

        self.figure = Figure(figsize=(8, 5), dpi=100, facecolor=self.colors['chart_bg'])
        self.canvas = FigureCanvasTkAgg(self.figure, results_frame)
        self.canvas.get_tk_widget().grid(row=1, column=0, pady=10, sticky="nsew")

        # Configure weight for resizing
        main_frame.columnconfigure(1, weight=3)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def load_process_data(self):
        self.processes = []
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))  # المسار الحالي للملف
            file_path = os.path.join(base_dir, "output.txt")  # ضفنا اسم الملف للمسار

            with open(file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if '|' in line and not line.startswith('--') and not 'Process ID' in line:
                        parts = line.split('|')
                        if len(parts) == 4:
                            pid = int(parts[0].strip())
                            arrival = float(parts[1].strip())
                            burst = float(parts[2].strip())
                            priority = int(parts[3].strip())
                            self.processes.append([pid, arrival, burst, priority])
            if not self.processes:
                raise ValueError("No valid process data found in file")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load process data: {str(e)}")

    def run_simulation(self):
        if not self.processes:
            messagebox.showerror("Error", "No process data loaded!")
            return

        algorithm = self.algorithm_var.get().split(' - ')[0]
        processes = self.processes.copy()

        if algorithm == "FCFS":
            self.run_fcfs(processes)
        elif algorithm == "RR":
            try:
                quantum = int(self.quantum_var.get())
                self.run_rr(processes, quantum)
            except ValueError:
                messagebox.showerror("Error", "Invalid time quantum!")
        elif algorithm == "SRTF":
            self.run_srtf(processes)
        elif algorithm == "SJF":
            self.run_sjf(processes)
        elif algorithm == "HPF":
            self.run_hpf(processes)

    def run_fcfs(self, processes):
        processes.sort(key=lambda x: x[1])
        self.display_results("First Come First Serve (FCFS)", processes)

    def run_sjf(self, processes):
        processes.sort(key=lambda x: (x[2], x[1]))
        self.display_results("Shortest Job First (SJF)", processes)

    def run_hpf(self, processes):
        processes.sort(key=lambda x: (-x[3], x[1]))
        self.display_results("Highest Priority First (HPF)", processes)

    def run_srtf(self, processes):
        processes.sort(key=lambda x: (x[2], x[1]))
        self.display_results("Shortest Remaining Time First (SRTF)", processes)

    def run_rr(self, processes, quantum):
        processes.sort(key=lambda x: x[1])
        completion_times = {}
        current_time = min(p[1] for p in processes)
        remaining_bursts = {p[0]: p[2] for p in processes}
        ready_queue = []

        while remaining_bursts:
            for p in processes:
                if p[0] in remaining_bursts and p[1] <= current_time and p[0] not in ready_queue:
                    ready_queue.append(p[0])

            if not ready_queue:
                current_time += 1
                continue

            current_pid = ready_queue.pop(0)
            if remaining_bursts[current_pid] <= quantum:
                current_time += remaining_bursts[current_pid]
                completion_times[current_pid] = current_time
                del remaining_bursts[current_pid]
            else:
                current_time += quantum
                remaining_bursts[current_pid] -= quantum
                ready_queue.append(current_pid)

        self.display_results("Round Robin (RR)", processes, completion_times)

    def display_results(self, algorithm, processes, completion_times=None):
        self.figure.clear()
        self.figure.set_facecolor(self.colors['chart_bg'])

        gs = self.figure.add_gridspec(2, 1, height_ratios=[1, 1], hspace=0.3)
        ax1 = self.figure.add_subplot(gs[0])
        ax2 = self.figure.add_subplot(gs[1])

        for ax in [ax1, ax2]:
            ax.set_facecolor(self.colors['chart_bg'])
            ax.tick_params(colors=self.colors['fg'], length=5)
            ax.xaxis.label.set_color(self.colors['fg'])
            ax.yaxis.label.set_color(self.colors['fg'])
            ax.title.set_color(self.colors['fg'])
            ax.grid(True, linestyle='--', alpha=0.2)

        if completion_times is None:
            completion_times = {}
            current_time = 0
            for process in processes:
                pid, arrival, burst, _ = process
                start_time = max(current_time, arrival)
                completion_time = start_time + burst
                current_time = completion_time
                completion_times[pid] = completion_time

        waiting_times = []
        turnaround_times = []
        current_time = 0
        colors = plt.cm.Pastel1(np.linspace(0, 1, len(processes)))

        for i, process in enumerate(processes):
            pid, arrival, burst, _ = process
            completion_time = completion_times[pid]
            turnaround = completion_time - arrival
            waiting = turnaround - burst

            waiting_times.append(waiting)
            turnaround_times.append(turnaround)

            ax1.barh(pid, burst, left=current_time, height=0.3, color=colors[i], alpha=0.8)
            ax2.barh(i, burst, left=current_time, height=0.3, color=colors[i], alpha=0.8)

            ax1.text(current_time + burst / 2, pid, f'P{pid}',
                     va='center', ha='center', color=self.colors['fg'])
            ax2.text(current_time + burst / 2, i, f'P{pid}',
                     va='center', ha='center', color=self.colors['fg'])
            current_time += burst

        ax1.set_title(f'{algorithm} - Process Order', pad=15, fontsize=10)
        ax1.set_xlabel('Time Units', labelpad=8)
        ax1.set_ylabel('Process ID', labelpad=8)

        ax2.set_title('Gantt Chart', pad=15, fontsize=10)
        ax2.set_xlabel('Time Units', labelpad=8)
        ax2.set_ylabel('Execution Order', labelpad=8)

        self.figure.tight_layout()
        self.canvas.draw()

        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        stats_style = {
            'font': ('Segoe UI', 10),
            'bg': self.colors['bg'],
            'fg': self.colors['fg'],
            'pady': 5,
            'padx': 10
        }

        tk.Label(self.stats_frame, text="📊 Performance Metrics", **stats_style).pack()
        tk.Label(self.stats_frame,
                 text=f"Average Waiting Time: {sum(waiting_times) / len(waiting_times):.2f} units",
                 **stats_style).pack()
        tk.Label(self.stats_frame,
                 text=f"Average Turnaround Time: {sum(turnaround_times) / len(turnaround_times):.2f} units",
                 **stats_style).pack()


if __name__ == "__main__":

    root = tk.Tk()
    app = ModernProcessSchedulerGUI(root)
    root.mainloop()