#!/usr/bin/env python3
"""Run the local presentation. Install dependencies first; see PRESENTATION.md."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import socket
import signal

ROOT = Path(__file__).resolve().parent

def main():
    python = ROOT / '.venv' / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    npm = shutil.which('npm.cmd' if os.name == 'nt' else 'npm')
    if not python.exists() or not npm or not (ROOT / 'frontend/node_modules').exists():
        sys.exit('Install dependencies first using PRESENTATION.md.')
    for port in (8765, 5173):
        with socket.socket() as sock:
            if sock.connect_ex(('127.0.0.1', port)) == 0:
                sys.exit(f'Port {port} is already in use. Stop the other server and try again.')
    env = dict(os.environ, DEMO_MODE='True', DEBUG='True', REDIS_URL='', DATABASE_URL='', API_PROXY_TARGET='http://127.0.0.1:8765')
    # Isolate sample records from the normal development database.
    env['DEMO_DATABASE_PATH'] = str(ROOT / 'backend/demo.sqlite3')
    command = [str(python), 'manage.py']
    subprocess.run(command + ['migrate', '--noinput'], cwd=ROOT/'backend', env=env, check=True)
    subprocess.run(command + ['seed_demo'], cwd=ROOT/'backend', env=env, check=True)
    processes = []
    group_options = {'creationflags': subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == 'nt' else {'start_new_session': True}
    try:
        processes.append(subprocess.Popen(command + ['runserver', '127.0.0.1:8765', '--noreload'], cwd=ROOT/'backend', env=env, **group_options))
        processes.append(subprocess.Popen([npm, 'run', 'dev', '--', '--host', '0.0.0.0', '--port', '5173', '--strictPort'], cwd=ROOT/'frontend', env=env, **group_options))
        print('\nOpen http://localhost:5173 — demo_farmer / DemoFarmer@2026\nPress Ctrl+C to stop both servers.', flush=True)
        while all(p.poll() is None for p in processes):
            time.sleep(0.5)
        raise RuntimeError('A server stopped. Check the error above.')
    except KeyboardInterrupt:
        pass
    finally:
        for p in processes:
            if os.name == 'nt':
                if p.poll() is None:
                    subprocess.run(['taskkill', '/PID', str(p.pid), '/T', '/F'], capture_output=True)
            else:
                try:
                    os.killpg(p.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
        for p in processes:
            try:
                p.wait(timeout=5)
            except subprocess.TimeoutExpired:
                p.kill()
                p.wait()

if __name__ == '__main__':
    main()
