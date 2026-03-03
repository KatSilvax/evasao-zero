"""Testes para o modelo de predição de evasão."""
import pytest
import pandas as pd
import joblib
import os


def test_modelo_existe():
    """Verifica se o modelo treinado existe."""
    assert os.path.exists("models/modelo_evasao.joblib"), "Modelo não encontrado"


def test_colunas_modelo_existe():
    """Verifica se o arquivo de colunas existe."""
    assert os.path.exists("models/colunas_modelo.joblib"), "Colunas do modelo não encontradas"


def test_modelo_carrega():
    """Testa se o modelo pode ser carregado."""
    if os.path.exists("models/modelo_evasao.joblib"):
        modelo = joblib.load("models/modelo_evasao.joblib")
        assert modelo is not None
        assert hasattr(modelo, 'predict')
        assert hasattr(modelo, 'predict_proba')


def test_predicao_formato():
    """Testa se a predição retorna o formato esperado."""
    if not os.path.exists("models/modelo_evasao.joblib"):
        pytest.skip("Modelo não encontrado")
    
    modelo = joblib.load("models/modelo_evasao.joblib")
    colunas = joblib.load("models/colunas_modelo.joblib")
    
    # Criar dados de teste
    dados_teste = pd.DataFrame(0, index=[0], columns=colunas)
    
    # Fazer predição
    predicao = modelo.predict(dados_teste)
    probabilidade = modelo.predict_proba(dados_teste)
    
    assert len(predicao) == 1
    assert probabilidade.shape == (1, 2)
    assert predicao[0] in ['Sim', 'Não']


def test_probabilidades_somam_um():
    """Testa se as probabilidades somam 1."""
    if not os.path.exists("models/modelo_evasao.joblib"):
        pytest.skip("Modelo não encontrado")
    
    modelo = joblib.load("models/modelo_evasao.joblib")
    colunas = joblib.load("models/colunas_modelo.joblib")
    
    dados_teste = pd.DataFrame(0, index=[0], columns=colunas)
    probabilidade = modelo.predict_proba(dados_teste)
    
    assert abs(probabilidade[0].sum() - 1.0) < 0.001
