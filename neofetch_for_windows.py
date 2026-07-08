import ctypes
import datetime
import os
import platform
import shutil
import socket
import subprocess
import sys

ANSI_RESET = "\033[0m"
ANSI_BOLD = "\033[1m"
ANSI_CYAN = "\033[96m"
ANSI_GREEN = "\033[92m"
ANSI_YELLOW = "\033[93m"
ANSI_MAGENTA = "\033[95m"
ANSI_BLUE = "\033[94m"
ANSI_RED = "\033[91m"
ANSI_SOFT_WHITE = "\033[38;2;200;200;200m"

#uncomment the ascii art you would like and comment the other one
#you can get more ascii arts on https://emojicombos.com/anime-ascii-art 

ASCII_ART = [
r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡇⠀⠀⠀⠀⠀⠀⠀⠀⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⣿⣃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
r"⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣧⣤⣤⣤⣀⣀⣀⢠⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
r"⠀⠀⠀⠀⠀⣀⡤⠚⠿⠿⠛⠁⠋⠁⠀⠀⠀⠀⠉⠙⠻⢧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
r"⠀⠀⠀⣠⠞⠁⠀⠀⠀⣠⠖⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠢⡝⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀",
r"⠀⢀⡾⢁⡀⠀⠀⣠⠞⠁⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠱⣈⣮⣳⡀⠀⠀⠀⠀⠀⠀⠀",
r"⢀⡞⢠⡞⠀⢀⡜⠁⠀⠀⠀⠀⡀⡟⣷⣤⠀⢀⠀⠀⢀⠀⠙⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀",
r"⣸⣷⣿⠀⢠⠎⠀⠀⠀⠀⡄⢠⣯⠃⢹⣿⠀⡎⠀⢠⢸⠙⣧⡈⢿⣜⣇⠀⠀⠀⠀⠀⠀",
r"⢹⣿⠀⢀⠋⠀⠀⢀⣠⠞⢀⣾⣟⣲⣼⣿⣰⠀⠀⢸⣸⠀⠹⣷⠈⣿⣿⠀⠀⠀⠀⠀⠀",
r"⢸⣿⢀⡎⣀⣤⣾⡿⠋⢠⣾⣿⣷⢾⣬⣿⠇⠀⢀⣞⣇⣀⠀⢻⡇⠸⡿⠀⠀⠀⠀⠀⠀",
r"⣾⣿⠚⢻⡛⠛⠉⣀⡴⠟⠹⣿⡟⡀⢹⡟⠀⢠⣿⣿⣿⣷⢶⣾⣿⢰⣷⠀⠀⠀⠀⠀⠀",
r"⣺⣿⢰⣍⠻⡭⠟⠋⠀⠀⠀⠀⠀⢀⡿⡡⢠⣿⢿⠙⢿⠿⠀⠈⣿⣿⣿⣷⠀⠀⠀⠀⠀",
r"⢻⣨⣀⢠⠀⣷⠀⠀⠀⠀⠀⠀⢀⣾⣷⣱⠟⠁⠀⠑⠈⠉⠉⢠⣏⢹⣿⡇⠀⠀⠀⠀⠀",
r"⠉⢿⢆⡉⢀⣉⠳⠀⠀⠀⠀⠀⣸⣿⠏⠀⠀⠀⠴⠏⠀⠀⠀⣸⡀⢸⣿⠇⠀⠀⠀⠀⠀",
r"⠀⢸⠀⠉⠙⣏⢣⠀⠀⠀⠀⠚⠋⠀⠀⠀⠀⢀⣀⣀⠀⠀⢰⣷⡇⣾⡏⠀⠀⠀⠀⠀⠀",
r"⠠⣼⡆⠀⢠⢠⡀⠳⣀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠈   ⣠⣿⣟⡏⣿⠀⠀⠀⠀⠀⠀⠀",
r"⠈⣿⣿⠀⢸⣄⡇⠀⠈⠢⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⣴⢻⣿⣟⡏⣿⡇⠀⠀⠀⠀⠀⠀",
r"⢐⣿⣿⡇⢸⣿⣷⠀⠀⠀⠀⠈⠑⠢⢄⣀⠀⢀⣤⣾⣿⣿⣇⣿⣇⣿⣷⠀⠀⠀⠀⠀⠀",
r"⢺⣿⣿⡇⢾⣿⣿⡇⠀⠐⣄⠀⠀⠀⠀⠀⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣖⣧⠀⠀⠀⠀⠀",
r"⢸⣿⢹⣇⢸⡋⣿⣷⠀⠀⠘⣆⠀⠀⠀⠀⢀⣼⠿⠟⠻⣿⠁⢹⣿⣿⣖⣧⠈⠳⡀⠀⠀",
]

# ASCII_ART = [
#     r"⠀⠀⠀⠀⠀⠀⣰⣾⠁⠀⢦⣾⣤⠆⠀⠻⣧⠀⠀⠀⠀⠀⠀",
#     r"⠀⠀⠀⠀⢠⣼⠏⠀⠀⠀⠀⣿⡇⠀⠀⠀⠈⢷⣄⠀⠀⠀⠀",
#     r"⠀⠀⢀⣸⣿⠃⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⢿⣧⡀⠀⠀",
#     r"⠀⢰⣾⣿⡁⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⢀⣿⣿⠖⠀",
#     r"⠀⠀⠈⠻⣿⣦⣄⠀⠀⠀⠀⣿⡇⠀⠀⠀⢀⣴⣿⠟⠁⠀⠀",
#     r"⠀⠀⠀⠀⠈⠻⢿⣷⣄⡀⠀⣿⡇⠀⣠⣾⣿⠟⠁⠀⠀⠀⠀",
#     r"⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣦⣿⣧⣾⣿⠟⠁⠀⠀⠀⠀⠀⠀",
#     r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⢙⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀",
#     r"⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀",
#     r"⠀⠀⠀⠀⠀⢀⣴⣿⣿⠟⠁⣻⣿⠈⠙⢿⣿⣦⡀⠀⠀⠀⠀",
#     r"⠀⠀⠀⢀⣴⣿⡿⠋⠀⠀⠀⣽⣿⠀⠀⠀⠙⢿⣿⣦⣄⠀⠀",
#     r"⠀⣠⣴⣿⡿⠋⠀⠀⠀⠀⠀⢼⣿⠀⠀⠀⠀⠀⠈⢻⣿⣷⣄",
#     r" ⠙⢿⣿⣦⣄⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⣠⣾⣿⠟⠁",
#     r"⠀⠀⠀⠙⢿⣿⣷⣄⠀⠀⠀⢸⣿⠀⠀⠀⣠⣾⣿⠟⠁⠀⠀",
#     r"⠀⠀⠀⠀⠀⠙⢻⣿⣷⡄⠀⢸⣿⠀⠀⣼⣿⣿⠃⠀⠀⠀⠀",
#     r"⠀⠀⠀⠀⠀⠀ ⠻⢿⣿⣦⣸⣿⣠⣾⣿⠟⠁⠀⠀⠀⠀⠀",
#     r"⠀⠀⠀⠀⠀⠀⠀  ⠙⢿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀",
#     r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀",
# ]

def enable_ansi_colors() -> None:
    if os.name != "nt":
        return

    kernel32 = ctypes.windll.kernel32
    handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
    if handle == 0:
        return

    mode = ctypes.c_uint()
    if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
        return

    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
    new_mode = mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING
    kernel32.SetConsoleMode(handle, new_mode)

def run_command(command: str) -> str:
    try:
        output = subprocess.check_output(command, stderr=subprocess.DEVNULL, shell=True)
        return output.decode(errors="replace").strip()
    except subprocess.CalledProcessError:
        return ""

def format_bytes(size: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"

def get_os_info() -> str:
    name = platform.system()
    release = platform.release()
    version = platform.version()
    return f"{name} {release} ({version})"

def get_host_info() -> str:
    node = platform.node() or socket.gethostname()
    manufacturer = ""
    model = ""
    output = run_command("wmic computersystem get manufacturer,model /format:list")
    for line in output.splitlines():
        if line.startswith("Manufacturer="):
            manufacturer = line.split("=", 1)[1].strip()
        elif line.startswith("Model="):
            model = line.split("=", 1)[1].strip()
    if manufacturer and model and manufacturer != model:
        return f"{node} ({manufacturer} {model})"
    if model:
        return f"{node} ({model})"
    return node

def get_kernel_info() -> str:
    return platform.version()

def get_uptime() -> str:
    if os.name == "nt":
        output = run_command("wmic os get lastbootuptime /value")
        for line in output.splitlines():
            if line.startswith("LastBootUpTime="):
                dt = line.split("=", 1)[1].strip()
                try:
                    boot = datetime.datetime.strptime(dt[:14], "%Y%m%d%H%M%S")
                    uptime = datetime.datetime.now() - boot
                    days = uptime.days
                    hours, remainder = divmod(uptime.seconds, 3600)
                    minutes, _ = divmod(remainder, 60)
                    return f"{days}d {hours}h {minutes}m"
                except ValueError:
                    break
    return "Unknown"

def get_cpu_info() -> str:
    cpu_name = platform.processor() or "Unknown CPU"
    output = run_command("wmic cpu get name /format:list")
    for line in output.splitlines():
        if line.startswith("Name="):
            cpu_name = line.split("=", 1)[1].strip()
            break
    speed = ""
    output = run_command("wmic cpu get MaxClockSpeed /format:list")
    for line in output.splitlines():
        if line.startswith("MaxClockSpeed="):
            try:
                speed = f"{int(line.split('=', 1)[1].strip())} MHz"
            except ValueError:
                speed = ""
            break
    return f"{cpu_name}{' @ ' + speed if speed else ''}"

def get_gpu_info() -> str:
    output = run_command("wmic path win32_VideoController get name /format:list")
    names = []
    for line in output.splitlines():
        if line.startswith("Name="):
            value = line.split("=", 1)[1].strip()
            if value:
                names.append(value)
    return ", ".join(names) if names else "Unknown GPU"

def get_memory_info() -> str:
    total = 0
    free = 0
    output = run_command("wmic OS get TotalVisibleMemorySize,FreePhysicalMemory /format:list")
    for line in output.splitlines():
        if line.startswith("TotalVisibleMemorySize="):
            try:
                total = int(line.split("=", 1)[1].strip()) * 1024
            except ValueError:
                total = 0
        elif line.startswith("FreePhysicalMemory="):
            try:
                free = int(line.split("=", 1)[1].strip()) * 1024
            except ValueError:
                free = 0
    if total > 0:
        used = total - free
        percent = used / total * 100
        return f"{format_bytes(used)} / {format_bytes(total)} ({percent:.0f}%)"
    return "Unknown"

def get_disk_info() -> str:
    try:
        root = os.path.abspath(os.sep)
        usage = shutil.disk_usage(root)
        return f"{format_bytes(usage.used)} / {format_bytes(usage.total)} ({usage.used / usage.total * 100:.0f}%)"
    except Exception:
        return "Unknown"

def get_python_info() -> str:
    version = platform.python_version()
    implementation = platform.python_implementation()
    return f"{implementation} {version}"

def get_shell_info() -> str:
    shell = os.environ.get("COMSPEC") or os.environ.get("SHELL") or "cmd.exe"
    return shell

def get_battery_info() -> str:
    if os.name != "nt":
        return "N/A"
    class SYSTEM_POWER_STATUS(ctypes.Structure):
        _fields_ = [
            ("ACLineStatus", ctypes.c_byte),
            ("BatteryFlag", ctypes.c_byte),
            ("BatteryLifePercent", ctypes.c_byte),
            ("Reserved1", ctypes.c_byte),
            ("BatteryLifeTime", ctypes.c_ulong),
            ("BatteryFullLifeTime", ctypes.c_ulong),
        ]
    status = SYSTEM_POWER_STATUS()
    if not ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(status)):
        return "Unknown"
    if status.BatteryLifePercent == 255:
        return "No Battery"
    return f"{status.BatteryLifePercent}%"

def get_info_lines() -> list[str]:
    return [
        ("OS", get_os_info()),
        ("Host", get_host_info()),
        ("Kernel", get_kernel_info()),
        ("Uptime", get_uptime()),
        ("CPU", get_cpu_info()),
        ("GPU", get_gpu_info()),
        ("Memory", get_memory_info()),
        ("Disk", get_disk_info()),
        ("Shell", get_shell_info()),
        ("Python", get_python_info()),
        ("Battery", get_battery_info()),
        ("User", os.getlogin()),
        ("Terminal", os.environ.get("TERM", "Unknown")),
        ("Processes", run_command("tasklist | find /c /v \"\"")),
        ("Time", datetime.datetime.now().strftime("%H:%M:%S")),
        ("Date", datetime.datetime.now().strftime("%d-%m-%Y")),
    ]

def color_text(text: str, color_code: str) -> str:
    return f"{color_code}{text}{ANSI_RESET}"

def print_neofetch() -> None:
    enable_ansi_colors()
    lines = get_info_lines()
    label_width = max(len(label) for label, _ in lines) + 1
    info_lines = [
    f"{color_text(label + ':', ANSI_RED):<{label_width + 1}} {color_text(value, ANSI_SOFT_WHITE)}"
    for label, value in lines
]
    art = ASCII_ART
    max_lines = max(len(art), len(info_lines))
    art += [""] * (max_lines - len(art))
    info_lines += [""] * (max_lines - len(info_lines))

    left_color = color_text("", "")
    for art_line, info in zip(art, info_lines):
        if info:
            max_width = max(len(line) for line in ASCII_ART) + 4
            print(f"{color_text(art_line, ANSI_RED):<{max_width}} {info}")
        else:
            print(color_text(art_line, ANSI_RED))

    print()

def main() -> None:
    if os.name != "nt":
        return
    print_neofetch()

if __name__ == "__main__":
    main()
    input("\n")

