#!/usr/bin/env python3
import subprocess
import sys
import os
import webbrowser
import time

def main():
    print("Tesla Electricidad - Iniciando proyecto completo...")
    
    try:
        os.chdir("tesla_complete")
        
        print("Instalando dependencias...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"])
        
        print("Iniciando backend...")
        os.chdir("backend")
        backend_process = subprocess.Popen([sys.executable, "main.py"])
        os.chdir("..")
        
        print("Esperando 3 segundos...")
        time.sleep(3)
        
        print("Abriendo frontend...")
        frontend_path = os.path.abspath("frontend/index.html")
        webbrowser.open(f"file://{frontend_path}")
        
        print("\nProyecto iniciado:")
        print("- Backend: http://localhost:8000")
        print("- Frontend: Abierto en navegador")
        print("- API Docs: http://localhost:8000/docs")
        print("\nTu chatbot Tesla esta listo!")
        print("\nPresiona Ctrl+C para detener")
        
        try:
            backend_process.wait()
        except KeyboardInterrupt:
            print("\nProyecto detenido")
            backend_process.terminate()
            
    except Exception as e:
        print(f"Error: {e}")
        print("Asegurate de estar en el directorio correcto")

if __name__ == "__main__":
    main()
