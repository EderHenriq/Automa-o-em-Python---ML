# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# SEÇÃO DE IMPORTAÇÃO DE BIBLIOTECAS
# Aqui, importamos todas as ferramentas que nosso script precisará para funcionar.
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
import time  # Para adicionar pausas (delays) no script.
from selenium import webdriver  # A biblioteca principal para controlar o navegador.
from selenium.webdriver.chrome.service import Service  # Para gerenciar o chromedriver.exe.
from selenium.webdriver.common.by import By  # Para localizar elementos na página (por ID, XPath, etc.).
from selenium.webdriver.support.ui import WebDriverWait  # Para esperar que elementos apareçam na tela.
from selenium.webdriver.support import expected_conditions as EC  # As condições para as esperas (ex: elemento visível).
from selenium.webdriver.common.keys import Keys  # Para simular o pressionamento de teclas (Enter, Shift, etc.).
import datetime  # Para trabalhar com datas e horas (usado nos logs e na mensagem).


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# SEÇÃO DE CONFIGURAÇÕES GLOBAIS
# Este é o "painel de controle" da automação. Todos os dados que podem mudar
# ficam aqui para facilitar a manutenção.
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Caminho completo para o arquivo chromedriver.exe no seu computador.
CHROME_DRIVER_PATH = "C:\\Users\\Waver\\Desktop\\eder\\automação ML\\chromedriver.exe"
# Nome exato do grupo do WhatsApp para onde as mensagens serão enviadas.
WHATSAPP_GROUP_NAME = "Equipe Tibaby" 

# --- Configurações da Empresa A (Tibaby) ---

# Nome que aparecerá na mensagem do WhatsApp.
NOME_EMPRESA_A = "Tibaby"
# Caminho para a pasta que guardará o perfil do Chrome da Empresa A (com logins salvos).
PERFIL_EMPRESA_A = "C:\\Users\\Waver\\Desktop\\eder\\automação ML\\chrome_profile_A"
# URL da página de vendas do Mercado Livre da Empresa A.
URL_ML_EMPRESA_A = "https://www.mercadolivre.com.br/vendas/omni/lista?filters=TAB_TODAY#type=recent"

# --- Configurações da Empresa B (Waver) ---

# Nome que aparecerá na mensagem do WhatsApp.
NOME_EMPRESA_B = "Waver"
# Caminho para a pasta que guardará o perfil do Chrome da Empresa B.
PERFIL_EMPRESA_B = "C:\\Users\\Waver\\Desktop\\eder\\automação ML\\chrome_profile_B"
# URL da página de vendas do Mercado Livre da Empresa B.
URL_ML_EMPRESA_B = "https://www.mercadolivre.com.br/vendas/omni/lista?filters=TAB_TODAY#type=recent"


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FUNÇÃO: pegar_codigo_ml
# Objetivo: Esta função é reutilizável. Sua única responsabilidade é abrir o
# navegador com o perfil de uma empresa, navegar até o Mercado Livre,
# extrair o código de autorização e retornar esse código.
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def pegar_codigo_ml(perfil_path, url_ml, nome_empresa):
    """Função para abrir o ML com um perfil específico e retornar o código."""
    print(f"--- Iniciando busca para a {nome_empresa} ---")
    driver = None  # Inicia a variável do driver como nula para garantir que ela exista.
    try:
        # Configura o serviço e as opções do Chrome para esta execução.
        service = Service(CHROME_DRIVER_PATH)
        options = webdriver.ChromeOptions()
        # A linha mais importante: diz ao Chrome qual pasta de perfil usar.
        options.add_argument(f"user-data-dir={perfil_path}")
        
        # Inicia o navegador Chrome com as configurações definidas.
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()
        
        # Navega até a URL do Mercado Livre.
        driver.get(url_ml)
        # Define uma espera máxima de 60 segundos para os próximos comandos.
        wait = WebDriverWait(driver, 60)
        time.sleep(3)  # Pausa estática para garantir o carregamento inicial.
        driver.refresh() # Atualiza a página para pegar os dados mais recentes.
        
        print(f"Buscando código da {nome_empresa}...")
        # Comando de espera inteligente: o script vai esperar ATÉ 60 segundos
        # para que o elemento com o código fique visível na tela.
        # O XPath localiza um <span> que contém o texto e, dentro dele, a tag <strong>.
        elemento_codigo = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Código de autorização para hoje:')]/strong"))
        )
        # Extrai o texto do elemento encontrado.
        codigo = elemento_codigo.text
        print(f"Código da {nome_empresa} encontrado: {codigo}")
        return codigo  # Retorna o código encontrado para quem chamou a função.
    
    except Exception as e:
        # Se qualquer erro acontecer no bloco 'try', ele será capturado aqui.
        print(f"Não foi possível obter o código da {nome_empresa}. Erro: {e}")
        return f"ERRO ao buscar ({nome_empresa})" # Retorna uma mensagem de erro.
    
    finally:
        # Este bloco SEMPRE será executado, independentemente de ter dado erro ou não.
        if driver:
            driver.quit()  # Garante que a janela do navegador seja sempre fechada.


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FUNÇÃO: enviar_mensagens_whatsapp
# Objetivo: Recebe os códigos das duas empresas e envia as 5 mensagens
# em sequência para o grupo do WhatsApp, usando o perfil da Empresa A.
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def enviar_mensagens_whatsapp(perfil_path, codigo_a, codigo_b):
    """Função para enviar as 5 mensagens separadas no WhatsApp."""
    print("--- Iniciando envio para o WhatsApp ---")
    driver = None
    try:
        # Cria a lista com as 5 mensagens exatas que serão enviadas.
        mensagens_para_enviar = [
            "Bom dia Familia!",
            NOME_EMPRESA_A,
            codigo_a,  # Alterado para enviar somente o código
            NOME_EMPRESA_B,
            codigo_b   # Alterado para enviar somente o código
        ]
        
        # Inicia o navegador com o perfil da Empresa A (que tem o WhatsApp conectado).
        service = Service(CHROME_DRIVER_PATH)
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-data-dir={perfil_path}")
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()
        
        # Abre o WhatsApp Web.
        driver.get("https://web.whatsapp.com/")
        print("Aguardando WhatsApp Web carregar...")
        print(">>> ATENÇÃO: Se for o primeiro acesso, escaneie o QR Code. O script vai esperar. <<<")
        
        # Espera longa (até 2 min) para a página do WhatsApp carregar completamente.
        # Ele aguarda a caixa de pesquisa de conversas aparecer.
        wait = WebDriverWait(driver, 120)
        caixa_de_pesquisa = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
        time.sleep(5) # Pausa extra para a interface renderizar.

        # Digita o nome do grupo na caixa de pesquisa.
        caixa_de_pesquisa.send_keys(WHATSAPP_GROUP_NAME)
        time.sleep(2)
        
        # Espera o resultado da pesquisa aparecer e clica no grupo com o nome correspondente.
        grupo = wait.until(EC.element_to_be_clickable((By.XPATH, f'//span[@title="{WHATSAPP_GROUP_NAME}"]')))
        grupo.click()
        time.sleep(2)

        # Localiza a caixa de digitação de mensagens do grupo.
        caixa_de_mensagem = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')))
        
        # Loop que passa por cada item da lista 'mensagens_para_enviar'.
        for mensagem in mensagens_para_enviar:
            caixa_de_mensagem.send_keys(mensagem) # Digita a mensagem.
            caixa_de_mensagem.send_keys(Keys.ENTER)  # Pressiona Enter para enviar.
            print(f"Mensagem enviada: '{mensagem}'")
            time.sleep(2)  # Pausa de 2 segundos entre cada mensagem.

        print("Todas as 5 mensagens foram enviadas com sucesso!")
        time.sleep(5) # Pausa final para garantir que a última mensagem foi.

    except Exception as e:
        print(f"Ocorreu um erro ao enviar as mensagens no WhatsApp: {e}")
    finally:
        if driver:
            driver.quit()


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# BLOCO DE EXECUÇÃO PRINCIPAL
# É aqui que a automação realmente começa quando você executa o script.
# Ele orquestra a chamada das funções na ordem correta.
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

if __name__ == "__main__":
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Iniciando automação para duas empresas...")
    
    # 1. Chama a função para pegar o código da Empresa A e guarda o resultado na variável.
    codigo_empresa_a = pegar_codigo_ml(PERFIL_EMPRESA_A, URL_ML_EMPRESA_A, NOME_EMPRESA_A)
    
    # 2. Chama a função para pegar o código da Empresa B e guarda o resultado na variável.
    codigo_empresa_b = pegar_codigo_ml(PERFIL_EMPRESA_B, URL_ML_EMPRESA_B, NOME_EMPRESA_B)
    
    # 3. Verifica se ambos os códigos foram obtidos com sucesso antes de tentar enviar.
    if "ERRO" not in codigo_empresa_a and "ERRO" not in codigo_empresa_b:
        # Se deu tudo certo, chama a função para enviar as mensagens.
        enviar_mensagens_whatsapp(PERFIL_EMPRESA_A, codigo_empresa_a, codigo_empresa_b)
    else:
        # Se um dos códigos falhou, avisa e não tenta enviar a mensagem.
        print("Falha na obtenção de um ou mais códigos. Mensagens não enviadas.")

    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Automação finalizada.")