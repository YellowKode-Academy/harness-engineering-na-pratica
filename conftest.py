import sys
import os

# Adiciona exemplos/ e cada cap-XX/ ao sys.path para que imports funcionem sem prefixo de pacote
_repo = os.path.dirname(os.path.abspath(__file__))
_exemplos = os.path.join(_repo, "exemplos")

if _exemplos not in sys.path:
    sys.path.insert(0, _exemplos)

for _item in sorted(os.listdir(_exemplos)):
    _cap_path = os.path.join(_exemplos, _item)
    if os.path.isdir(_cap_path) and (_item.startswith("cap") or _item.startswith("_")):
        if _cap_path not in sys.path:
            sys.path.insert(0, _cap_path)


def pytest_collection_modifyitems(config, items):
    """Sem ANTHROPIC_API_KEY, os testes marcados como integration são pulados em vez de falhar."""
    if os.environ.get("ANTHROPIC_API_KEY"):
        return
    import pytest
    pular = pytest.mark.skip(reason="defina ANTHROPIC_API_KEY para rodar os testes de integração")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(pular)
