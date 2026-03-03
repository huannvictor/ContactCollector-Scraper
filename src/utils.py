import os
import re
import logging
from pathlib import Path
from typing import List

def setup_logging(log_dir: Path = Path("logs")):
    """Configura o sistema de logs."""
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "execucao.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

def ensure_dirs():
    """Garante que as pastas do projeto existam."""
    Path("data/input").mkdir(parents=True, exist_ok=True)
    Path("data/output").mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(parents=True, exist_ok=True)

def only_digits(s: str) -> str:
    """Extrai apenas dígitos de uma string."""
    return re.sub(r"\D+", "", s or "")

def strip_country(digits: str) -> str:
    """Remove prefixo 55 de telefones se presente."""
    if digits.startswith("55") and len(digits) in (12, 13):
        return digits[2:]
    return digits

def format_fixed(digits: str) -> str:
    """Formata telefone fixo."""
    digits = strip_country(digits)
    if len(digits) == 10:
        ddd = digits[:2]
        local = digits[2:]
        return f"({ddd}) {local[:4]}-{local[4:]}"
    if len(digits) == 8:
        return f"{digits[:4]}-{digits[4:]}"
    return digits

def format_mobile_local9(local_digits: str) -> str:
    """Formata celular local de 9 dígitos."""
    if len(local_digits) != 9:
        return local_digits
    return f"{local_digits[:5]}-{local_digits[5:]}"

def read_codes(path: Path) -> List[str]:
    """Lê os códigos do arquivo de entrada."""
    if not path.exists():
        return []
    
    codes: List[str] = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if line and re.fullmatch(r"\d+", line):
            codes.append(line)
    return codes
