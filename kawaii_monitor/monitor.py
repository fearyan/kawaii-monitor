import psutil
import time
import curses
from datetime import datetime
import platform
import os

def get_size(bytes):
    """Convert bytes to human readable format (cute version~ ｡^‿^｡)"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024:
            return f"{bytes:.1f}{unit}"
        bytes /= 1024

def get_disk_info():
    """Get storage information for all mounted disks (◕‿◕✿)"""
    disks = []
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disks.append({
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent': usage.percent
            })
        except (PermissionError, FileNotFoundError):
            continue
    return disks

def safe_addstr(stdscr, y, x, string, color=None):
    """Safely add a string to the screen, keeping it cute and truncating if needed (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧"""
    height, width = stdscr.getmaxyx()
    if y < height:
        try:
            if color is not None:
                stdscr.addstr(y, x, string[:width-x], color)
            else:
                stdscr.addstr(y, x, string[:width-x])
        except curses.error:
            pass
    

def main(stdscr):
    # Setup kawaii colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Super cute green!
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Pastel cyan for sparkles
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Sunshine yellow (･ω･)ﾉ
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)     # Hot pink-ish red for alerts!
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # Sweet magenta for storage
    
    # Hide the cursor to keep the screen clean and cute!
    curses.curs_set(0)
    stdscr.nodelay(1)

    last_net_io = psutil.net_io_counters()
    last_time = time.time()

    # Get system information
    system_info = {
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor()
    }

    while True:
        try:
            stdscr.clear()
            height, width = stdscr.getmaxyx()

            # Super Cute Title Bar (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧
            current_time = datetime.now().strftime("%H:%M:%S")
            title = f"(❤️ ω ❤️)  Kawaii System Monitor  (✿◡‿◡)   {current_time}  (❤️ ω ❤️)"
            safe_addstr(stdscr, 0, (width-len(title))//2, title, curses.color_pair(2))

            # System Information (🖥️✨)
            safe_addstr(stdscr, 2, 0, f"🖥️  System: {system_info['system']} {system_info['release']} ({system_info['machine']}) (◕‿◕✿)", curses.color_pair(2))
            
            uptime_seconds = time.time() - psutil.boot_time()
            days, remainder = divmod(uptime_seconds, 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes = remainder // 60
            safe_addstr(stdscr, 3, 0, f"⏰ Uptime: {int(days)}d {int(hours)}h {int(minutes)}m ฅ^•ﻌ•^ฅ", curses.color_pair(3))

            # Get and display process count
            process_count = len(psutil.pids())
            safe_addstr(stdscr, 23, 0, f"🎀 Running Processes: {process_count} (◕ᴥ◕)", curses.color_pair(4))
            
            # CPU Info (💻✨)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            cpu_percent = psutil.cpu_percent()
            cpu_bar = "💖" * int(cpu_percent/5) + "🤍" * (20-int(cpu_percent/5))
            cpu_color = curses.color_pair(1) if cpu_percent < 70 else curses.color_pair(4)
            safe_addstr(stdscr, 4, 0, f"💻 CPU Usage: [{cpu_bar}] {cpu_percent:5.1f}%  (｡♥‿♥｡)", cpu_color)
            safe_addstr(stdscr, 5, 0, f"🎯 CPU Cores: {cpu_count} | Frequency: {cpu_freq.current:.1f}MHz  (｡◕‿◕｡)")
            
            # Memory Usage Info (📦💞)
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            mem_bar = "🧠" * int(mem.percent/5) + "😴" * (20-int(mem.percent/5))
            mem_color = curses.color_pair(1) if mem.percent < 70 else curses.color_pair(4)
            safe_addstr(stdscr, 7, 0, f"📦 Memory:   [{mem_bar}] {mem.percent:5.1f}%  (๑˃̵ᴗ˂̵)و", mem_color)
            safe_addstr(stdscr, 8, 0, f"🌸 RAM: {get_size(mem.total)} | Used: {get_size(mem.used)} | Free: {get_size(mem.free)}  (⁎˃ᆺ˂)")
            safe_addstr(stdscr, 9, 0, f"💫 Swap: {get_size(swap.total)} | Used: {get_size(swap.used)} | Free: {get_size(swap.free)}  (◕‿◕✿)")

            # Storage Information (💾✨)
            disks = get_disk_info()
            safe_addstr(stdscr, 11, 0, "💾 Storage Devices (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧", curses.color_pair(5))
            current_y = 12
            for disk in disks:
                disk_bar = "💎" * int(disk['percent']/5) + "💫" * (20-int(disk['percent']/5))
                disk_color = curses.color_pair(1) if disk['percent'] < 80 else curses.color_pair(4)
                safe_addstr(stdscr, current_y, 0, 
                    f"📂 {disk['mountpoint']}: [{disk_bar}] {disk['percent']}%  (´｡• ᵕ •｡`)", disk_color)
                safe_addstr(stdscr, current_y + 1, 2, 
                    f"Total: {get_size(disk['total'])} | Used: {get_size(disk['used'])} | Free: {get_size(disk['free'])}  ✧◝(⁰▿⁰)◜✧")
                current_y += 3

            # Network Speed Info (🌐⚡)
            current_time_val = time.time()
            current_net_io = psutil.net_io_counters()
            time_elapsed = current_time_val - last_time
            
            if time_elapsed > 0:
                upload_speed = (current_net_io.bytes_sent - last_net_io.bytes_sent) / time_elapsed
                download_speed = (current_net_io.bytes_recv - last_net_io.bytes_recv) / time_elapsed
                total_sent = get_size(current_net_io.bytes_sent)
                total_recv = get_size(current_net_io.bytes_recv)
                safe_addstr(stdscr, current_y, 0, f"📡 Upload:   {get_size(upload_speed)}/s (Total: {total_sent})  (๑•̀ㅂ•́)و", curses.color_pair(3))
                safe_addstr(stdscr, current_y + 1, 0, f"📥 Download: {get_size(download_speed)}/s (Total: {total_recv})  (๑•̀ω•́)و", curses.color_pair(3))
            
            last_net_io = current_net_io
            last_time = current_time_val

            # Battery Information (if available) (🔋✨)
            if hasattr(psutil, 'sensors_battery'):
                battery = psutil.sensors_battery()
                if battery:
                    current_y += 3
                    battery_bar = "⚡" * int(battery.percent/5) + "✨" * (20-int(battery.percent/5))
                    battery_color = curses.color_pair(1) if battery.percent > 20 else curses.color_pair(4)
                    plugged = "🔌 Plugged In" if battery.power_plugged else "🔋 On Battery"
                    safe_addstr(stdscr, current_y, 0, 
                        f"🔋 Battery: [{battery_bar}] {battery.percent}% {plugged}  (◕‿◕✿)", battery_color)

            # Cute Process List (☆⌒(ゝ。∂))
            current_y += 2
            safe_addstr(stdscr, current_y + 1, 0, "🌟 Top Kawaii Processes:", curses.color_pair(2))
            safe_addstr(stdscr, current_y + 2, 0, "📌 PID    🏎 CPU%   💾 MEM%   ✨ Name  (≧◡≦)")

            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    pinfo = proc.info
                    processes.append({
                        'pid': pinfo['pid'],
                        'cpu_percent': proc.cpu_percent(),
                        'memory_percent': proc.memory_percent(),
                        'name': pinfo['name']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass

            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)

            for i, proc in enumerate(processes[:height-current_y-4]):
                try:
                    safe_addstr(stdscr, current_y + 2 + i, 0, 
                        f"🎀 {proc['pid']:<6} 🚀 {proc['cpu_percent']:>5.1f} 💖 {proc['memory_percent']:>6.1f}  🎉 {proc['name'][:30]}  (✿◠‿◠)")
                except curses.error:
                    break

            safe_addstr(stdscr, height-1, 0, "🌈 Press 'q' to exit ~ ( ˘ ³˘)♥  See you later, alligator! 〳〵✧", curses.color_pair(2))
            
            stdscr.refresh()
            
            if stdscr.getch() == ord('q'):
                break

            time.sleep(1)
        
        except curses.error:
            pass

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass