import subprocess
from collections import Counter
from datetime import datetime
from typing import List, Tuple, Generator

class Process:
    def __init__(self, processor):
        self.user = processor[0]
        self.pid = processor[1]
        self.cpu = float(processor[2])
        self.mem = float(processor[3])
        self.vsz = processor[4]
        self.rss = processor[5]
        self.tty = processor[6]
        self.stat = processor[7]
        self.start = processor[8]
        self.time = processor[9]
        self.command = processor[10]

    def __repr__(self):
        return f"Process(user={self.user}, pid={self.pid}, cpu={self.cpu}, mem={self.mem}, command={self.command})"

def run_ps_aux_process() -> Generator[Process, None, None]:
    try:
        process = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0 or stderr:
            raise RuntimeError(f"Error running 'ps aux': {stderr.decode('utf-8').strip()}")

        result = stdout.decode('utf-8').strip().split('\n')

        for line in result[1:]:
            processor = line.split(maxsplit=10)
            if len(processor) == 11:
                yield Process(processor)
    except Exception as e:
        print(f"Error fetching process data: {e}")


def get_ps_aux_users(processes: List[Process]) -> List[str]:
    """Get a list of unique users."""
    users = set(proc.user for proc in processes)
    return sorted(users)

def get_count_ps_aux_process_total(processes: List[Process]) -> int:
    """Count total processes."""
    return len(processes)

def get_count_ps_aux_process_per_user(processes: List[Process]) -> str:
    """Count processes per user."""
    user_process_count = Counter(proc.user for proc in processes)
    return "\n".join(f"{user:<15}: {count}" for user, count in user_process_count.items())

def get_memory_percentage(processes: List[Process]) -> float:
    """Calculate total memory usage percentage."""
    return sum(proc.mem for proc in processes)

def get_cpu_percentage(processes: List[Process]) -> float:
    """Calculate total CPU usage percentage."""
    return sum(proc.cpu for proc in processes)

def get_process_with_max_memory(processes: List[Process]) -> Tuple[str, float]:
    """Find the process using the most memory."""
    max_memory_process = max(processes, key=lambda proc: proc.mem)
    process_name = max_memory_process.command[:20]
    return process_name, max_memory_process.mem

def get_process_name_for_most_cpu(processes: List[Process]) -> Tuple[str, float]:
    """Find the process using the most CPU."""
    max_cpu_process = max(processes, key=lambda proc: proc.cpu)
    process_name = max_cpu_process.command[:20]
    return process_name, max_cpu_process.cpu

def run_script():
    """Print system status report."""
    processes = list(run_ps_aux_process())

    print("Отчёт о состоянии системы:")
    users = get_ps_aux_users(processes)
    users_str = ", ".join(users)
    print(f'Пользователи системы: {users_str}')
    print(f'Процессов запущено: {get_count_ps_aux_process_total(processes)}')
    print("\n")

    print("Пользовательских процессов:")
    print(get_count_ps_aux_process_per_user(processes))

    print(f'Всего памяти используется: {get_memory_percentage(processes):.2f} %')
    print(f'Всего CPU используется: {get_cpu_percentage(processes):.2f} %')
    name, memory = get_process_with_max_memory(processes)
    print(f"Больше всего памяти использует: {name} ({memory:.2f}%)")
    name_, cpu = get_process_name_for_most_cpu(processes)
    print(f"Больше всего CPU использует: {name_} ({cpu:.2f}%)")

def generate_report() -> List[str]:
    """Generate report text as a list of strings."""
    processes = list(run_ps_aux_process())

    report = []
    report.append("Отчёт о состоянии системы:")
    users = get_ps_aux_users(processes)
    users_str = ", ".join(users)
    report.append(f'Пользователи системы: {users_str}')
    report.append(f'Процессов запущено: {get_count_ps_aux_process_total(processes)}')
    report.append("\n")

    report.append("Пользовательских процессов:")
    report.append(get_count_ps_aux_process_per_user(processes))

    report.append(f'Всего памяти используется: {get_memory_percentage(processes):.2f} %')
    report.append(f'Всего CPU используется: {get_cpu_percentage(processes):.2f} %')
    name, memory = get_process_with_max_memory(processes)
    report.append(f"Больше всего памяти использует: {name} ({memory:.2f}%)")
    name_, cpu = get_process_name_for_most_cpu(processes)
    report.append(f"Больше всего CPU использует: {name_} ({cpu:.2f}%)")

    return report

def print_results():
    """Save the generated report to a file."""
    report = generate_report()
    timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M")
    filename = f"{timestamp}-scan.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(report))

    print(f"Отчёт сохранён в файл: {filename}")

if __name__ == "__main__":
    run_script()
    print_results()
