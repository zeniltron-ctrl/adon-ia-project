import subprocess, sys, os, time, urllib.request

os.environ.setdefault('PYTHONIOENCODING', 'utf-8')

PROJECT = os.path.dirname(os.path.abspath(__file__))
# Troque "eurico" pelo seu usuário do Windows
OLLAMA = r'C:\Users\informatica\AppData\Local\Programs\Ollama\ollama.exe'
procs = []

def start(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
    procs.append(p)
    return p

def ollama_ok():
    try:
        urllib.request.urlopen('http://127.0.0.1:11434/api/tags', timeout=2)
        return True
    except:
        return False

def stop_all():
    for p in procs:
        if p.poll() is None:
            p.terminate()
            try: p.wait(timeout=3)
            except: p.kill()
    procs.clear()
    import psutil
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] and 'ollama' in proc.info['name'].lower():
                p = psutil.Process(proc.info['pid'])
                p.terminate()
                try: p.wait(timeout=3)
                except: p.kill()
        except:
            pass
    for port, name in [(11434, 'Ollama'), (12800, 'Flask')]:
        ok = False
        try:
            urllib.request.urlopen(f'http://127.0.0.1:{port}/', timeout=1)
            ok = True
        except:
            pass
        print(f'  {name}: {"parado" if not ok else "ainda rodando"}')
    print('  Processos encerrados.')

def main():
    print('+------------------------+')
    print('|      Adon-ia LLM      |')
    print('+------------------------+')
    print()

    if ollama_ok():
        print('  Ollama já está rodando.')
    else:
        print('  Iniciando Ollama em 2º plano...')
        start([OLLAMA, 'serve'])
        for i in range(15):
            time.sleep(1)
            if ollama_ok():
                print('  Ollama pronto.')
                break
        else:
            print('  Falha ao iniciar Ollama.')
            stop_all()
            return

    app_path = os.path.join(PROJECT, 'app.py')
    start([sys.executable, app_path])
    time.sleep(1)
    print('  WebUI pronto.')

    print()
    print('  http://localhost:12800')
    print('  ESC para parar tudo.')
    print()

    try:
        import msvcrt
        while True:
            if msvcrt.kbhit() and msvcrt.getch() == b'\x1b':
                break
            for p in procs:
                if p.poll() is not None:
                    print(f'  Processo {p.pid} encerrou.')
                    stop_all()
                    return
            time.sleep(0.3)
    except KeyboardInterrupt:
        pass

    stop_all()

if __name__ == '__main__':
    main()
