# Este script inicia a bateria completa de testes de benchmark.
# Ele subirá todas as APIs, fará os testes com Locust, criará os gráficos e depois encerrará tudo sozinho.

Write-Host "Iniciando a bateria de testes automatizada (Benchmark)..."
Write-Host "Por favor, aguarde. O processo pode levar cerca de 48 minutos."
Write-Host "----------------------------------------------------------------"

# Chama o script Python que orquestra tudo
python benchmark.py

Write-Host "----------------------------------------------------------------"
Write-Host "Testes concluídos! Verifique a pasta 'resultados' para ver o gráfico e os dados."
