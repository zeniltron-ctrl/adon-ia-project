import subprocess, sys, os

script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'adon-ia-project', 'run.py')
sys.exit(subprocess.call([sys.executable, script] + sys.argv[1:]))
