@echo off
REM Verifica se o pipenv está instalado
pipenv --version >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo "pipenv não está instalado. Instalando agora..."
    pip install pipenv
)

REM Instala as dependências se necessário
pipenv install --dev

REM Executa o script main.py dentro do ambiente virtual
pipenv run python main.py
