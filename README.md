## RPA – Cadastro de Funcionários

### Descrição
Automação desenvolvida em **Python + Selenium** para realizar o **cadastro automático de funcionários** em uma aplicação web.  
O processo faz login, baixa a planilha de dados, lê as informações e executa os cadastros de forma automatizada.

---

### ⚙️ Funcionalidades
- Login na aplicação  
- Download da planilha de funcionários  
- Armazenamento temporário do arquivo  
- Cadastro automático dos dados  
- Logs de execução  
- Envio de e-mail com o status do processo  

---

### Decisões Técnicas
- Implementação seguindo o padrão **Page Object Model (POM)**  
- **Sem retentativa de login** em caso de erro de credencial  
- Uso de **diretório temporário** para armazenar a planilha baixada  

---

### Tecnologias
- Python 3.12+  
- Selenium  
- Pandas  
- tempfile  
- loguru  
- smtplib / email.message  
- python-dotenv  

---

### Execução
1. Instalar dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Configurar o arquivo `.env`:
   ```bash
   APP_USERNAME=seu_usuario_de_app
   APP_PASSWORD=sua_senha_de_app
   GMAIL_USERNAME=seu_email@gmail.com
   GMAIL_PASSWORD=sua_senha_de_email
   ```
3. Executar:
   ```bash
   python main.py
   ```

---

### 🧑‍💻 Autor
**Rodrigo Araujo Silva**  
Automação de Processos | RPA | Python | Selenium  
