from django.shortcuts import render
import psutil
import platform
import subprocess

def get_windows_full_name():
    """
    Intenta obtener el nombre completo de Windows desde el sistema,
    sin depender de librerías externas como wmi.
    """
    try:
        # Ejecuta el comando systeminfo y busca la linea con el nombre del sistema
        output = subprocess.check_output("systeminfo", shell=True, text=True, encoding='utf-8', errors='ignore')
        for line in output.splitlines():
            if "Nombre del sistema operativo" in line or "OS Name" in line:
                return line.split(":", 1)[1].strip()
    except Exception:
        pass
    # Si no se logra obtener, devuelve una descripcion generica
    return f"Windows {platform.release()} ({platform.version()})"


def home(request):
    try:
        # Recolección de datos del sistema
        cpu_percent = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        system_info = platform.uname()

        # Informacion de CPU
        cpu_cores_physical = psutil.cpu_count(logical=False)
        cpu_cores_logical = psutil.cpu_count(logical=True)

        # Informacion del sistema operativo
        os_name = system_info.system
        os_version = system_info.version

        # Si el sistema es Windows, obtener nombre completo
        if os_name.lower() == "windows":
            os_full = get_windows_full_name()
        else:
            os_full = f"{os_name} {os_version}"

        data = {
            'cpu_percent': cpu_percent,
            'ram_total': round(ram.total / (1024 ** 3), 2),
            'ram_used': round(ram.used / (1024 ** 3), 2),
            'ram_percent': ram.percent,
            'disk_total': round(disk.total / (1024 ** 3), 2),
            'disk_used': round(disk.used / (1024 ** 3), 2),
            'disk_free': round(disk.free / (1024 ** 3), 2),
            'os': os_name,
            'version': os_full,
            'processor': system_info.processor,
            'cpu_cores_physical': cpu_cores_physical,
            'cpu_cores_logical': cpu_cores_logical,
        }

    except Exception as e:
        data = {'error': str(e)}

    return render(request, 'sistema/index.html', {'data': data})
