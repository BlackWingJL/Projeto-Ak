import unittest
import tempfile
import os
from Zain import salvar_alarme, verificar_alarmes, apagar_alarme, validar_data_hora
from datetime import datetime

class TestZain(unittest.TestCase):
    def setUp(self):
        # Cria um diretório temporário para os testes
        self.temp_dir = tempfile.TemporaryDirectory()
        self.pasta_alarmes = os.path.join(self.temp_dir.name, "alarmes")
        os.makedirs(self.pasta_alarmes, exist_ok=True)

    def tearDown(self):
        # Remove o diretório temporário após os testes
        self.temp_dir.cleanup()

    def test_validar_data_hora(self):
        self.assertTrue(validar_data_hora("29/05/2025 01:15"))
        self.assertFalse(validar_data_hora("29/05/2025 25:15"))
        self.assertFalse(validar_data_hora("data inválida"))

    def test_salvar_alarme(self):
        resultado = salvar_alarme("Teste de alarme", "29/05/2025 01:15")
        self.assertIn("salvo com sucesso", resultado)

    def test_apagar_alarme(self):
        salvar_alarme("Teste de alarme", "29/05/2025 01:15")
        resultado = apagar_alarme("Teste de alarme")
        self.assertIn("apagado com sucesso", resultado)

    def test_verificar_alarmes(self):
        caminho_alarme = os.path.join(self.pasta_alarmes, "alarmes.txt")
        with open(caminho_alarme, "w") as arquivo:
            arquivo.write(f"{datetime.now().strftime('%d/%m/%Y %H:%M')}|Teste de alarme\n")
        
        verificar_alarmes()
        with open(caminho_alarme, "r") as arquivo:
            linhas_restantes = arquivo.readlines()
        
        # Verifica se o alarme foi removido após ser acionado
        self.assertEqual(len(linhas_restantes), 0)

if __name__ == "__main__":
    unittest.main()