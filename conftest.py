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
