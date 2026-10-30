import json
import numpy as np
from pyscript import document

def registrar_telemetria(acao, dados):
    """Módulo de telemetria para auditar eventos da interface."""
    print(f"[TELEMETRIA] Ação: {acao} | Detalhes: {dados}")

def validar_guardrails(docura_str, acidez_str):
    """Módulo de segurança: previne injeções e valida faixas de entrada."""
    try:
        docura = float(docura_str)
        acidez = float(acidez_str)
    except ValueError:
        return False, "Erro de Guardrail: Entradas devem ser numéricas."
    
    if not (0 <= docura <= 10) or not (0 <= acidez <= 10):
        return False, "Erro de Guardrail: Valores devem estar entre 0 e 10."
    
    return True, "Validação bem-sucedida."

def calcular_distancia_vetorial(vec_usuario, vec_fruta):
    v1 = np.array(vec_usuario)
    v2 = np.array(vec_fruta)
    return np.linalg.norm(v1 - v2)

def carregar_dados():
    with open("dados.json", "r", encoding="utf-8") as f:
        return json.load(f)

def processar_busca(event):
    registrar_telemetria("clique_buscar", "Usuário disparou busca multimodal.")
    
    el_docura = document.getElementById("input-docura").value
    el_acidez = document.getElementById("input-acidez").value
    el_erro = document.getElementById("msg-erro")
    el_resultados = document.getElementById("resultados")
    
    el_erro.innerText = ""
    el_resultados.innerHTML = ""
    
    valido, msg_guardrail = validar_guardrails(el_docura, el_acidez)
    if not valido:
        registrar_telemetria("bloqueio_guardrail", msg_guardrail)
        el_erro.innerText = msg_guardrail
        return
        
    vetor_busca = [float(el_docura), float(el_acidez)]
    dados_hortifruti = carregar_dados()
    frutas = dados_hortifruti.get("frutas", [])
    
    # logica com os valores do embedding
    melhor_match = None
    menor_distancia = float('inf')
    
    for fruta in frutas:
        distancia = calcular_distancia_vetorial(vetor_busca, fruta["embedding"])
        if distancia < menor_distancia:
            menor_distancia = distancia
            melhor_match = fruta
            
    registrar_telemetria("busca_concluida", f"Fruta recomendada: {melhor_match['nome']} | Distância: {menor_distancia:.2f}")
    
    # DOM
    html_resultado = f"""
    <div class="card-fruta">
        <img src="{melhor_match['imagem']}" alt="{melhor_match['nome']}" onerror="this.src='data:image/svg+xml;utf8,<svg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'200\\' height=\\'200\\'><rect width=\\'200\\' height=\\'200\\' fill=\\'%23eee\\'/><text x=\\'50%\\' y=\\'50%\\' dominant-baseline=\\'middle\\' text-anchor=\\'middle\\' font-family=\\'sans-serif\\' font-size=\\'14\\' fill=\\'%23999\\'>Sem Imagem</text></svg>'">
        <h3>{melhor_match['nome']}</h3>
        <p><strong>Preço:</strong> R$ {melhor_match['preco']:.2f} / kg</p>
        <p style="font-size: 0.9em; color: #555;">Distância Euclidiana: {menor_distancia:.2f}</p>
    </div>
    """
    el_resultados.innerHTML = html_resultado

registrar_telemetria("sistema_iniciado", "PyScript carregado com numpy.")