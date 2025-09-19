# Automação de Códigos Mercado Livre 🤖

##  Objetivo do Projeto

Este projeto consiste em um script de automação desenvolvido para resolver um problema de rotina em um ambiente de e-commerce: a necessidade de coletar e distribuir códigos de autorização diários de múltiplas contas do **Mercado Livre**. A tarefa, quando realizada manualmente, era repetitiva, demorada e suscetível a erros humanos.

A automação foi projetada para ser executada em um horário agendado, de segunda a sexta-feira, sem qualquer intervenção humana, otimizando o fluxo de trabalho da equipe.

##  Como Funciona

A solução utiliza um script Python robusto que simula a interação humana com o navegador. O robô executa uma sequência lógica de tarefas:

1.  **Coleta de Dados (Empresa A):** Inicia um navegador com um perfil dedicado, acessa a conta da primeira empresa no Mercado Livre, extrai o código de autorização do dia e armazena essa informação.
2.  **Coleta de Dados (Empresa B):** Repete o processo para a segunda empresa, utilizando um perfil de navegador diferente para manter as sessões de login separadas e seguras.
3.  **Envio via WhatsApp:** Com os dois códigos coletados, o robô utiliza o perfil da primeira empresa (que já tem uma sessão do WhatsApp Web ativa) para se conectar, encontrar um grupo específico e enviar os dois códigos em mensagens separadas e formatadas, identificando cada empresa.

Todo o processo é executado de forma autônoma, silenciosa e confiável, garantindo que a equipe receba as informações necessárias pontualmente no início de cada dia de trabalho.

## ⚙️ Funcionalidades Essenciais

* **Gerenciamento de Múltiplas Contas:** Acessa e opera em duas contas distintas do Mercado Livre de forma sequencial.
* **Perfis de Navegador Persistentes:** Utiliza perfis de navegador separados para cada conta, salvando os logins do Mercado Livre e do WhatsApp para evitar a necessidade de autenticação a cada execução.
* **Web Scraping de Precisão:** Localiza e extrai um código específico de uma página web dinâmica, mesmo após mudanças na estrutura do HTML.
* **Automação de Mensageria:** Controla o WhatsApp Web para enviar uma série de mensagens formatadas para um grupo pré-definido.
* **Agendamento Inteligente:** Projetado para ser executado por um agendador de tarefas externo (como o System Scheduler), operando apenas em dias úteis.

## 🛠️ Tecnologias Utilizadas

* **Linguagem Principal:** Python
* **Automação Web & Scraping:** Selenium WebDriver
* **Dependências:** ChromeDriver
* **Agendador de Tarefas Externo:** System Scheduler (ou similar)
* **Controle de Versão:** Git & GitHub

<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white" />
  <img src="https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white" />
</p>

## Como Usar

1.  **Pré-requisitos:**
    * Python 3 instalado.
    * Google Chrome instalado.
    * ChromeDriver compatível com a versão do seu Chrome.

2.  **Instalação:**
    * Clone este repositório: `git clone `
    * Instale as dependências: `pip install selenium`

3.  **Configuração:**
    * Mova o `chromedriver.exe` para a pasta do projeto.
    * No arquivo `automacao_ml.py`, preencha as variáveis na seção de configurações com os seus próprios caminhos e nomes.
    * Crie as pastas de perfil na raiz do projeto (ex: `chrome_profile_A` e `chrome_profile_B`).

4.  **Primeira Execução:**
    * Execute o script uma vez (`python automacao_ml.py`) para realizar os logins manuais no Mercado Livre (para ambas as contas) e no WhatsApp Web (para a conta principal) nas janelas do navegador que o robô abrir.

5.  **Agendamento:**
    * Configure um agendador de tarefas (System Scheduler ou outro) para executar o script no horário e dias desejados.

## 📈 Status do Projeto

Projeto Concluído ✔️
