import docker, time, json, sys
from datetime import datetime

start = datetime.now()

filename = sys.argv[1] if len(sys.argv) > 1 else "monolith"

client = docker.from_env()

f = open(f"{filename}.json", "a")

def __calculate_memory_percent(data):
    memory_used = float(data['memory_stats']['usage'])
    memory_limit = float(data['memory_stats']['limit'])

    return (memory_used / memory_limit) * 100.0

def __calculate_cpu_percent(data):
    cpu_percent = 0.0

    cpu_count = data["cpu_stats"]["online_cpus"]

    cpu_delta = (float(data['cpu_stats']['cpu_usage']['total_usage']) -
                    float(data['precpu_stats']['cpu_usage']['total_usage']))

    system_delta = (float(data["cpu_stats"]["system_cpu_usage"]) -
                    float(data["precpu_stats"]["system_cpu_usage"]))

    if system_delta > 0.0:
        cpu_percent = cpu_delta / system_delta * 100.0 * cpu_count

    return cpu_percent

raw_stats = []
try:
    start = datetime.now()
    while True:
        for container in client.containers.list():
            # if container.name in ("account", "customer", "payment", "transfer"):
            if container.name in ("monolith-app"):
                now = datetime.now()
                if ((now - start).total_seconds()) > 10.0:
                    break
                sys.stdout.write(f"\rtime: {now - start} {container.name}             ")
                sys.stdout.flush()
                raw_stats.append({ 'name' : container.name, 'stats' : container.stats(stream=False) })

finally:
    print("Processing writing...")
    stats = []
    for raw_stat in raw_stats:
        stats.append({ 'name' : raw_stat['name'], 
                        'cpu_usage' : __calculate_cpu_percent(raw_stat['stats']), 
                        'memory_usage' : __calculate_memory_percent(raw_stat['stats']),
                        'read': raw_stat['stats']['read'],
                        'pre_read': raw_stat['stats']['preread'],
                        'memory_stats' : { 'usage' : raw_stat['stats']['memory_stats']['usage'], 'limit' : raw_stat['stats']['memory_stats']['limit'] }
                    })
    f.write(json.dumps(stats))
    f.close()
    end = datetime.now()
    print(f"time processed: {end - start}")
    print("DONE.")