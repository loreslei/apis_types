# Este script apenas liga as 8 APIs e as deixa rodando no fundo para você poder testar manualmente no Postman.

Write-Host "Iniciando as 8 APIs em background..." -ForegroundColor Green
Start-Process -NoNewWindow node "node_services\rest\app.js"
Start-Process -NoNewWindow node "node_services\graphql\app.js"
Start-Process -NoNewWindow node "node_services\grpc\app.js"
Start-Process -NoNewWindow node "node_services\soap\app.js"
Start-Process -NoNewWindow python "python_services\rest\app.py"
Start-Process -NoNewWindow python "python_services\graphql\app.py"
Start-Process -NoNewWindow python "python_services\grpc\app.py"
Start-Process -NoNewWindow python "python_services\soap\app.py"

Write-Host "Todas as 8 APIs estão ligadas e prontas para uso!" -ForegroundColor Cyan
Write-Host "Portas:"
Write-Host "Node REST: 3001   | Python REST: 8001"
Write-Host "Node GraphQL: 3002| Python GraphQL: 8002"
Write-Host "Node gRPC: 3003   | Python gRPC: 8003"
Write-Host "Node SOAP: 3004   | Python SOAP: 8004"
Write-Host ""
Write-Host "Para desligar as APIs quando terminar os seus testes no Postman, execute o seguinte comando no PowerShell:" -ForegroundColor Yellow
Write-Host "Stop-Process -Name node,python -ErrorAction SilentlyContinue"
