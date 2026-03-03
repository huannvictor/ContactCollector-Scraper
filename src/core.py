import re
import logging
from typing import List, Optional, Tuple
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from src import utils

# Configurações do site
BASE_URL = "https://webdivulgacao.luzdosaber.com.br"
LOGIN_URL = f"{BASE_URL}/Login.aspx?Pagina=Default.aspx"
SCHOOL_URL_PREFIX = f"{BASE_URL}/Escola.aspx?IDEscola="

# Seletores
SEL_USER = "#ctl00_ContentPlaceHolder1_TextBox1"
SEL_PASS = "#ctl00_ContentPlaceHolder1_TextBox2"
SEL_LOGIN_BTN = "#ctl00_ContentPlaceHolder1_Button1"
SEL_PHONES = "#ctl00_ContentPlaceHolder1_UcEscola1_lbFones"
SEL_ADMIN_NAME = "#ctl00_ContentPlaceHolder1_UcEscola1_lblNome_ADM"
SEL_EMAIL = "#ctl00_ContentPlaceHolder1_UcEscola1_lbEmail"

def classify_and_pick_phones(raw: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Entrada: texto bruto do campo de telefones. Saída: (fixo, celular, celular_diretor)"""
    if not raw:
        return None, None, None

    s = raw.strip().replace("", " ")
    parts = re.split(r"\s*(?:/|,|;|\||\s{2,})\s*", s)
    parts = [p.strip() for p in parts if p and p.strip()]

    fixed: Optional[str] = None
    mobiles: List[str] = []

    for p in parts:
        digits = utils.strip_country(utils.only_digits(p))
        if not digits:
            continue

        if len(digits) == 10:
            if fixed is None:
                fixed = utils.format_fixed(digits)
            continue

        if len(digits) == 11:
            local9 = digits[-9:]
            mobiles.append(utils.format_mobile_local9(local9))
            continue

        if len(digits) == 9:
            if digits[0] == "9":
                mobiles.append(utils.format_mobile_local9(digits))
            else:
                mobiles.append(utils.format_mobile_local9("9" + digits[-8:]))
            continue

        if len(digits) == 8:
            local9 = "9" + digits
            mobiles.append(utils.format_mobile_local9(local9))
            continue

        if len(digits) > 11:
            tail9 = digits[-9:]
            if tail9 and tail9[0] == "9":
                mobiles.append(utils.format_mobile_local9(tail9))
                continue

    celular: Optional[str] = mobiles[0] if len(mobiles) >= 1 else None
    celular_diretor: Optional[str] = mobiles[1] if len(mobiles) >= 2 else celular

    return fixed, celular, celular_diretor

def do_login(page: Page, username: str, password: str, test_school_code: str) -> None:
    """Executa o login no sistema."""
    logging.info(f"Tentando login com usuário: {username}")
    page.goto(LOGIN_URL, wait_until="domcontentloaded")
    page.wait_for_selector(SEL_USER, timeout=30_000)

    page.fill(SEL_USER, username)
    page.fill(SEL_PASS, password)
    
    with page.expect_navigation(wait_until="networkidle"):
        page.click(SEL_LOGIN_BTN)
    
    # Validação
    test_url = f"{SCHOOL_URL_PREFIX}{test_school_code}"
    page.goto(test_url, wait_until="domcontentloaded")
    
    logging.info(f"URL atual após login: {page.url}")
    
    if "Login.aspx" in page.url:
        raise RuntimeError(f"Falha no login: credenciais inválidas ou bloqueio. URL: {page.url}")
    logging.info("Login bem-sucedido.")

def scrape_school(page: Page, code: str) -> dict:
    """Extrai os dados de uma escola individual."""
    url = f"{SCHOOL_URL_PREFIX}{code}"
    record = {
        "fixo": None, "celular": None, "celular_diretor": None,
        "nome_do_administrador_legal": None, "email": None,
        "codigo_escola": code, "erro": None, "url": url
    }

    try:
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_selector(SEL_PHONES, timeout=30_000)

        phones_raw = (page.text_content(SEL_PHONES) or "").strip()
        admin_name = (page.text_content(SEL_ADMIN_NAME) or "").strip()
        email_text = (page.text_content(SEL_EMAIL) or "").strip()

        fixo, celular, celular_dir = classify_and_pick_phones(phones_raw)
        record.update({
            "fixo": fixo, "celular": celular, "celular_diretor": celular_dir,
            "nome_do_administrador_legal": admin_name or None,
            "email": email_text or None
        })
    except PlaywrightTimeoutError:
        logging.error(f"Timeout ao acessar escola {code}")
        record["erro"] = "timeout (elemento não apareceu)"
    except Exception as e:
        logging.error(f"Erro ao processar escola {code}: {str(e)}")
        record["erro"] = f"{type(e).__name__}: {e}"

    return record
