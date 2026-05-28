import subprocess
import sys
import shutil

KEYWORDS = [
    ("script", 5),
    ("running analysis", 10),
    ("analyzing", 15),
    ("finding modules", 20),
    ("looking for dependencies", 25),
    ("building pyd", 35),
    ("building pyz", 45),
    ("building pkg", 55),
    ("building exe", 70),
    ("building collect", 100),
    ("moving", 95),
    ("copying", None),
]


def _print_bar(percent, width=None):
    if width is None:
        width = shutil.get_terminal_size((80, 20)).columns - 30
    width = max(10, width)
    filled = int(width * percent // 100)
    bar = '[' + '█' * filled + '-' * (width - filled) + ']' + f' {percent:3d}%'
    sys.stdout.write('\r' + bar)
    sys.stdout.flush()


def run_pyinstaller_with_progress(args):
    
    cmd = [sys.executable, '-m', 'PyInstaller'] + args
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

    percent = 0.0
    copy_events = 0
    _print_bar(int(percent))

    try:
        for line in proc.stdout:
            l = line.strip().lower()
            found = False
            for kw, p in KEYWORDS:
                if kw in l:
                    if p is not None:
                        percent = max(percent, float(p))
                        _print_bar(int(percent))
                    else:
                        copy_events += 1
                        bump = min(0.2 * copy_events, 14.0)
                        _print_bar(int(min(85 + bump, 99)))
                    found = True
                    break
            
            if not found and percent < 99:
                percent = min(percent + 0.2, 99.0)
                _print_bar(int(percent))

            if 'completed successfully' in l or ('dist' in l and 'successful' in l):
                percent = 100.0
                _print_bar(int(percent))
    except Exception:
        proc.kill()
        raise
    finally:
        proc.wait()
        if proc.returncode == 0:
            _print_bar(100)
            sys.stdout.write('\n')
        else:
            sys.stdout.write('\n')

    return proc.returncode
