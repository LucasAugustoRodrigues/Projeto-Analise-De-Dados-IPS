#!/usr/bin/env python3
"""
Dashboard IPS Brasil 2024 - Executador Final
Script otimizado para execução em ambiente acadêmico
Versão: 2.0 (Sem warnings do Plotly)
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    dependencias = ['streamlit', 'plotly', 'pandas', 'numpy', 'openpyxl']
    dependencias_faltantes = []
    
    print("🔍 Verificando dependências...")
    
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"   ✅ {dep}")
        except ImportError:
            dependencias_faltantes.append(dep)
            print(f"   ❌ {dep}")
    
    if dependencias_faltantes:
        print(f"\n⚠️  Dependências faltantes: {', '.join(dependencias_faltantes)}")
        print("💡 Execute: pip install " + " ".join(dependencias_faltantes))
        return False
    
    print("✅ Todas as dependências estão instaladas!\n")
    return True

def verificar_arquivo_dados():
    """Verifica se o arquivo de dados existe"""
    arquivo_dados = Path("Cpy_IPS_Brasil_2024.xlsx")
    
    if arquivo_dados.exists():
        print("✅ Arquivo de dados encontrado: Cpy_IPS_Brasil_2024.xlsx")
        return True
    else:
        print("❌ Arquivo de dados não encontrado: Cpy_IPS_Brasil_2024.xlsx")
        print("💡 Certifique-se de que o arquivo está na pasta do projeto")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("📊 DASHBOARD IPS BRASIL 2024")
    print("🎓 Projeto Acadêmico - Estatística e Probabilidade")
    print("👥 Dupla: Lucas")
    print("=" * 60)
    
    # Verificações pré-execução
    if not verificar_dependencias():
        input("\n⏸️  Pressione Enter após instalar as dependências...")
        return
    
    if not verificar_arquivo_dados():
        input("\n⏸️  Pressione Enter após colocar o arquivo de dados na pasta...")
        return
    
    print("\n🚀 Iniciando Dashboard...")
    print("📍 Servidor local: http://localhost:8501")
    print("🔄 O navegador abrirá automaticamente")
    print("\n⚠️  Para parar o servidor: Ctrl+C no terminal\n")
    
    try:
        # Executar Streamlit
        processo = subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "dashboard_ips.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--server.headless", "false"
        ])
        
    except KeyboardInterrupt:
        print("\n🔴 Dashboard finalizado pelo usuário.")
        print("📋 Obrigado por usar o Dashboard IPS Brasil 2024!")
        
    except FileNotFoundError:
        print("\n❌ Streamlit não encontrado.")
        print("💡 Execute: pip install streamlit")
        
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        print("💡 Verifique se todos os arquivos estão na pasta correta")

if __name__ == "__main__":
    main()