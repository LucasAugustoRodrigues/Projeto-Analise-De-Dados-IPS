# 📊 Dashboard IPS Brasil 2024

**Projeto de Estatística e Probabilidade**  
**Aluno:** Lucas  
**Professor:** Pedro Girotto  

---

## 🚀 Como Executar

### **Método 1: Pelo Terminal/PowerShell (Recomendado)**

1. **Abra o PowerShell ou Terminal**
2. **Navegue até a pasta do projeto:**
```powershell
cd "c:\Users\lucas\Faculdade\Pedro_Girotto\Estatistica_E_Probabilidade_Dp\Projeto-Analise-De-Dados-IPS"
```

3. **Execute o dashboard:**
```powershell
streamlit run dashboard.py
```

4. **Acesse no navegador:**
   - O Streamlit tentará abrir automaticamente
   - Se não abrir, acesse manualmente: `http://localhost:8501`

### **Método 2: Pelo VS Code (Alternativo)**

1. **Abra o terminal integrado** (`Ctrl + '`)
2. **Execute:**
```bash
streamlit run dashboard.py
```

### **⚠️ Se não funcionar automaticamente:**

1. **Copie e cole no navegador:** `http://localhost:8501`
2. **Ou tente:** `http://127.0.0.1:8501`
3. **Verifique se apareceu a mensagem:** `You can now view your Streamlit app in the browser.`

### **🔧 Troubleshooting:**

**Erro "streamlit não reconhecido":**
```powershell
pip install streamlit
```

**Erro de arquivo não encontrado:**
- Certifique-se de estar na pasta correta
- Verifique se `dashboard.py` está na pasta atual

---

## 📁 Arquivos do Projeto

- **`dashboard.py`** → Dashboard principal (código didático)

- **`Cpy_IPS_Brasil_2024.xlsx`** → Base de dados (5.571 municípios)
- **`GUIA_COMPLETO_EXPLICACAO.md`** → Explicação detalhada do código
- **`INSTRUCOES_FINAIS_LUCAS.md`** → Roteiro para apresentação

---

## 📊 Funcionalidades

### 📈 Visão Geral
- Estatísticas descritivas do IPS nacional
- Distribuição dos dados
- Top 10 melhores municípios

### 🗺️ Análise Regional
- Comparação entre as 5 regiões brasileiras
- Filtros interativos
- Estatísticas por região

### 🏛️ Capitais vs Interior
- Comparação estatística
- Visualizações comparativas
- Ranking das capitais

### 📊 Gráficos Detalhados
- Análise de correlações
- Estatísticas descritivas completas
- Visualizações avançadas

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.7+**
- **Streamlit** (interface web)
- **Pandas** (manipulação de dados)
- **Plotly** (gráficos interativos)
- **NumPy** (cálculos estatísticos)
