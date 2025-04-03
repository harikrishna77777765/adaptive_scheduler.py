import random
import time
import matplotlib.pyplot as plt
import numpy as np

class Task:
    def __init__(self, task_id, priority, deadline, exec_time, period):
        self.id = task_id
        self.static_priority = priority
        self.dynamic_priority = priority
        self.deadline = deadline
        self.remaining_time = exec_time
        self.executed_time = 0
        self.period = period
        self.arrival_time = time.time()
        
    def __str__(self):
        return f"Task {self.id}: Priority {self.dynamic_priority} ({self.static_priority}), " \
               f"Deadline {self.deadline}ms, Remaining {self.remaining_time}ms"

class AdaptiveScheduler:
    def __init__(self):
        self.tasks = []
        self.history = []
        self.metrics = {
            'cpu_utilization': 0,
            'ready_tasks': 0,
            'missed_deadlines': 0,
            'timeline': []
        }
        self.fig, self.ax = plt.subplots(3, 1, figsize=(14, 12))
        plt.ion()
    
    def add_task(self, task):
        self.tasks.append(task)
        self.metrics['ready_tasks'] = len(self.tasks)
    
    def monitor_workload(self):
        self.metrics['cpu_utilization'] = 0.6 + random.random() * 0.4
        self.metrics['ready_tasks'] = len(self.tasks)
    
    def adapt_priorities(self):
        util = self.metrics['cpu_utilization']
        for task in self.tasks:
            task.dynamic_priority = task.static_priority
            if util > 0.8:
                task.dynamic_priority += 2
            elif util > 0.6:
                task.dynamic_priority += 1
            if task.deadline < 50:
                task.dynamic_priority += 3
            elif task.deadline < 100:
                task.dynamic_priority += 1
    
    def schedule_next_task(self):
        if not self.tasks:
            return None
        
        next_task = min(self.tasks, key=lambda x: (x.deadline, -x.dynamic_priority))
        exec_time = min(10 + random.randint(0, 20), next_task.remaining_time)
        next_task.executed_time += exec_time
        next_task.remaining_time -= exec_time
        
        self.metrics['timeline'].append({
            'time': time.time(),
            'task': next_task.id,
            'priority': next_task.dynamic_priority,
            'remaining': next_task.remaining_time
        })
        
        if next_task.remaining_time <= 0:
            self.tasks.remove(next_task)
            print(f"Task {next_task.id} completed")
        
        return next_task
    
    def visualize(self):
        self.ax[0].clear()
        self.ax[1].clear()
        self.ax[2].clear()
        
        timeline = [m['time'] for m in self.metrics['timeline']]
        cpu_util = [self.metrics['cpu_utilization']*100 for _ in timeline]
        task_count = [self.metrics['ready_tasks'] for _ in timeline]
        
        self.ax[0].plot(timeline, cpu_util, 'r-', label='CPU Utilization %', linewidth=2.5)
        self.ax[0].plot(timeline, task_count, 'b-', label='Ready Tasks', linewidth=2.5)
        self.ax[0].set_title('System Metrics', fontsize=16)
        self.ax[0].set_ylabel('Percentage / Task Count', fontsize=14)
        self.ax[0].legend()
        self.ax[0].grid(True, linestyle='--', alpha=0.7)
        
        task_ids = list(set(m['task'] for m in self.metrics['timeline']))
        colors = plt.cm.get_cmap('tab10', len(task_ids))
        
        for i, task_id in enumerate(task_ids):
            task_data = [m for m in self.metrics['timeline'] if m['task'] == task_id]
            times = [m['time'] for m in task_data]
            priorities = [m['priority'] for m in task_data]
            self.ax[1].scatter(times, priorities, color=colors(i), label=f'Task {task_id}', s=120, edgecolors='black', linewidth=1.2)
        
        self.ax[1].set_title('Task Priorities Over Time', fontsize=16)
        self.ax[1].set_ylabel('Dynamic Priority', fontsize=14)
        self.ax[1].legend()
        self.ax[1].grid(True, linestyle='--', alpha=0.7)
        
        exec_times = [m['remaining'] for m in self.metrics['timeline']]
        self.ax[2].plot(timeline, exec_times, 'g-', label='Remaining Execution Time', linewidth=2.5)
        self.ax[2].set_title('Task Execution Time Over Time', fontsize=16)
        self.ax[2].set_ylabel('Execution Time (ms)', fontsize=14)
        self.ax[2].set_xlabel('Time', fontsize=14)
        self.ax[2].legend()
        self.ax[2].grid(True, linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        plt.draw()
        plt.pause(0.1)
    
    def run_simulation(self, cycles=20):
        tasks = [
            Task(1, 5, 100, 50, 200),
            Task(2, 3, 150, 70, 300),
            Task(3, 4, 80, 30, 150)
        ]
        for task in tasks:
            self.add_task(task)
        
        for cycle in range(cycles):
            print(f"\n=== Cycle {cycle + 1} ===")
            if cycle in [3, 6, 9]:
                new_task = Task(
                    10 + cycle,
                    2 + random.randint(0, 4),
                    50 + random.randint(0, 150),
                    30 + random.randint(0, 70),
                    200 + random.randint(0, 200)
                )
                self.add_task(new_task)
                print(f"Added new task: {new_task}")
            
            self.monitor_workload()
            self.adapt_priorities()
            
            for task in sorted(self.tasks, key=lambda x: x.dynamic_priority, reverse=True):
                print(task)
            
            next_task = self.schedule_next_task()
            if next_task:
                print(f"Executing: {next_task}")
            
            self.visualize()
            time.sleep(1)

if __name__ == "__main__":
    scheduler = AdaptiveScheduler()
    scheduler.run_simulation()
