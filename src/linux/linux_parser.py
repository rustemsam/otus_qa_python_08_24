import subprocess
from collections import Counter
from datetime import datetime
from typing import List, Tuple, Optional


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

    @classmethod
    def run_ps_aux_process(cls) -> List['Process']:
        """Fetch and parse processes using 'ps aux'."""
        try:
            process = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode != 0 or stderr:
                raise RuntimeError(f"Error running 'ps aux': {stderr.decode('utf-8').strip()}")

            result = stdout.decode('utf-8').strip().split('\n')
            return [cls(line.split(maxsplit=10)) for line in result[1:] if len(line.split(maxsplit=10)) == 11]
        except Exception as e:
            print(f"Error fetching process data: {e}")
            return []

    @property
    def command_trimmed(self) -> str:
        """Get the first 20 characters of the command."""
        return self.command[:20]

    @classmethod
    def users(cls, processes: List['Process']) -> List[str]:
        """Get a sorted list of unique users."""
        return sorted({proc.user for proc in processes})

    @classmethod
    def total_process_count(cls, processes: List['Process']) -> int:
        """Count total processes."""
        return len(processes)

    @classmethod
    def process_count_per_user(cls, processes: List['Process']) -> str:
        """Count processes per user."""
        user_process_count = Counter(proc.user for proc in processes)
        return "\n".join(f"{user:<15}: {count}" for user, count in user_process_count.items())

    @classmethod
    def total_memory(cls, processes: List['Process']) -> float:
        """Calculate total memory usage."""
        return sum(proc.mem for proc in processes)

    @classmethod
    def total_cpu(cls, processes: List['Process']) -> float:
        """Calculate total CPU usage."""
        return sum(proc.cpu for proc in processes)

    @classmethod
    def max_memory_process(cls, processes: List['Process']) -> Tuple[str, float]:
        """Find the process using the most memory."""
        max_memory_proc = max(processes, key=lambda proc: proc.mem)
        return max_memory_proc.command_trimmed, max_memory_proc.mem

    @classmethod
    def max_cpu_process(cls, processes: List['Process']) -> Tuple[str, float]:
        """Find the process using the most CPU."""
        max_cpu_proc = max(processes, key=lambda proc: proc.cpu)
        return max_cpu_proc.command_trimmed, max_cpu_proc.cpu

    def __repr__(self):
        return f"Process(user={self.user}, pid={self.pid}, cpu={self.cpu}, mem={self.mem}, command={self.command})"


# Standalone functions
def generate_report() -> List[str]:
    """Generate report text as a list of strings."""
    processes = Process.from_ps_aux()

    report = []
    report.append("Отчёт о состоянии системы:")
    report.append(f"Пользователи системы: {', '.join(Process.users(processes))}")
    report.append(f'Процессов запущено: {Process.total_process_count(processes)}')
    report.append("\n")

    report.append("Пользовательских процессов:")
    report.append(Process.process_count_per_user(processes))

    report.append(f'Всего памяти используется: {Process.total_memory(processes):.2f} %')
    report.append(f'Всего CPU используется: {Process.total_cpu(processes):.2f} %')
    name, memory = Process.max_memory_process(processes)
    report.append(f"Больше всего памяти использует: {name} ({memory:.2f}%)")
    name_, cpu = Process.max_cpu_process(processes)
    report.append(f"Больше всего CPU использует: {name_} ({cpu:.2f}%)")

    return report


def run_script():
    """Print system status report."""
    processes = Process.from_ps_aux()

    print("Отчёт о состоянии системы:")
    print(f"Пользователи системы: {', '.join(Process.users(processes))}")
    print(f'Процессов запущено: {Process.total_process_count(processes)}')
    print("\n")

    print("Пользовательских процессов:")
    print(Process.process_count_per_user(processes))

    print(f'Всего памяти используется: {Process.total_memory(processes):.2f} %')
    print(f'Всего CPU используется: {Process.total_cpu(processes):.2f} %')
    name, memory = Process.max_memory_process(processes)
    print(f"Больше всего памяти использует: {name} ({memory:.2f}%)")
    name_, cpu = Process.max_cpu_process(processes)
    print(f"Больше всего CPU использует: {name_} ({cpu:.2f}%)")


def print_results():
    """Save the generated report to a file."""
    report = generate_report()
    timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M")
    filename = f"{timestamp}-scan.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(report))

    print(f"Отчёт сохранён в файл: {filename}")


# Main execution
if __name__ == "__main__":
    run_script()
    print_results()
