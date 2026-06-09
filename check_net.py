import psutil
print("Interfaces:", psutil.net_if_addrs().keys())
for name, stats in psutil.net_if_stats().items():
    print(f"{name}: is_up={stats.isup}")
