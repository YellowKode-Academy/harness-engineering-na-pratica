# exemplos/cap-04/test_tool_definitions.py
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import pytest
from pydantic import ValidationError
from tool_validation import PostarComentarioParams, LerArquivoParams

class TestPostarComentarioParams:
    def test_parametros_validos_passam(self):
        params = PostarComentarioParams(
            pr_numero=142,
            linha=37,
            severidade="alta",
            descricao="variável não inicializada antes do uso"
        )
        assert params.linha == 37
        assert params.severidade == "alta"

    def test_linha_zero_e_rejeitada(self):
        with pytest.raises(ValidationError) as exc_info:
            PostarComentarioParams(
                pr_numero=142, linha=0,
                severidade="alta", descricao="problema"
            )
        assert "linha deve ser positiva" in str(exc_info.value)

    def test_descricao_longa_e_rejeitada(self):
        descricao_longa = "x" * 201
        with pytest.raises(ValidationError) as exc_info:
            PostarComentarioParams(
                pr_numero=142, linha=10,
                severidade="media", descricao=descricao_longa
            )
        assert "excede limite" in str(exc_info.value)

class TestLerArquivoParams:
    def test_caminho_absoluto_e_rejeitado(self):
        with pytest.raises(ValidationError):
            LerArquivoParams(caminho="/etc/passwd")

    def test_path_traversal_e_rejeitado(self):
        with pytest.raises(ValidationError):
            LerArquivoParams(caminho="src/../../../etc/passwd")

    def test_caminho_relativo_valido_passa(self):
        params = LerArquivoParams(caminho="src/auth/login.py")
        assert params.caminho == "src/auth/login.py"

# pytest exemplos/cap-04/test_tool_definitions.py -v
# Output: 6 passed in 0.08s
