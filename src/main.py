import os
import logging
import pandas as pd
from pathlib import Path
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

from src import utils
from src import core

def run():
    # 1. Configurações Iniciais
    load_dotenv()
    utils.ensure_dirs()
    utils.setup_logging()
    
    # 2. Caminhos de Arquivos
    input_file = Path("data/input/codigos.txt")
    output_file = Path("data/output/luzdosaber_escolas.xlsx")
    
    # 3. Leitura de Entrada
    codes = utils.read_codes(input_file)
    if not codes:
        logging.error("Nenhum código encontrado em data/input/codigos.txt")
        return

    # 4. Credenciais
    username = os.getenv("LUZ_USER")
    password = os.getenv("LUZ_PASS")
    
    if not username or not password:
        logging.error("Credenciais não configuradas. Verifique o arquivo .env")
        return
    
    rows = []
    
    # 5. Processamento
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            core.do_login(page, username, password, codes[0])
            
            for i, code in enumerate(codes, 1):
                logging.info(f"[{i}/{len(codes)}] Processando escola: {code}")
                record = core.scrape_school(page, code)
                rows.append(record)
                
        except Exception as e:
            logging.critical(f"Erro fatal na execução: {e}")
        finally:
            browser.close()

    # 6. Salvamento de Resultados
    if rows:
        df = pd.DataFrame(rows)
        # Ordenar colunas para o padrão desejado
        ordered = [
            "fixo", "celular", "celular_diretor", 
            "nome_do_administrador_legal", "email", 
            "codigo_escola", "erro", "url"
        ]
        df = df[ordered]
        df.to_excel(output_file, index=False)
        logging.info(f"Processamento concluído. Planilha gerada: {output_file}")
    else:
        logging.warning("Nenhum dado foi coletado.")

if __name__ == "__main__":
    run()
