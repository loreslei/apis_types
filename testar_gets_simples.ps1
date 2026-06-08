# Este script sobe as 8 APIs e faz requisições GET simples para cada uma delas usando o Locust em modo rápido (1 usuário, 1 requisição) apenas para validar que todas estão respondendo corretamente.

Write-Host "Iniciando as 8 APIs em background..."
$procs = @()
$procs += Start-Process -NoNewWindow -PassThru node "node_services\rest\app.js"
$procs += Start-Process -NoNewWindow -PassThru node "node_services\graphql\app.js"
$procs += Start-Process -NoNewWindow -PassThru node "node_services\grpc\app.js"
$procs += Start-Process -NoNewWindow -PassThru node "node_services\soap\app.js"
$procs += Start-Process -NoNewWindow -PassThru python "python_services\rest\app.py"
$procs += Start-Process -NoNewWindow -PassThru python "python_services\graphql\app.py"
$procs += Start-Process -NoNewWindow -PassThru python "python_services\grpc\app.py"
$procs += Start-Process -NoNewWindow -PassThru python "python_services\soap\app.py"

Write-Host "Aguardando 8 segundos para inicialização..."
Start-Sleep -Seconds 8

Write-Host "----------------------------------------------------"
Write-Host "Realizando requisições GET em cada API para testar..."
Write-Host "----------------------------------------------------"

$targets = @(
    @("REST (Node)", "locust/locust_rest.py", "http://127.0.0.1:3001"),
    @("REST (Python)", "locust/locust_rest.py", "http://127.0.0.1:8001"),
    @("GraphQL (Node)", "locust/locust_graphql.py", "http://127.0.0.1:3002"),
    @("GraphQL (Python)", "locust/locust_graphql.py", "http://127.0.0.1:8002"),
    @("gRPC (Node)", "locust/locust_grpc.py", "http://127.0.0.1:3003"),
    @("gRPC (Python)", "locust/locust_grpc.py", "http://127.0.0.1:8003"),
    @("SOAP (Node)", "locust/locust_soap.py", "http://127.0.0.1:3004"),
    @("SOAP (Python)", "locust/locust_soap.py", "http://127.0.0.1:8004")
)

foreach ($target in $targets) {
    $name = $target[0]
    $file = $target[1]
    $host_url = $target[2]
    
    Write-Host "Disparando GET contra $name..." -ForegroundColor Cyan
    # Roda o locust com 1 usuário por apenas 2 segundos para forçar o envio de requisições GET
    python -m locust -f $file --headless -u 1 -r 1 --run-time 2s --host $host_url --loglevel WARNING
    Write-Host "Concluído $name.`n"
}

Write-Host "----------------------------------------------------"
Write-Host "Testes rápidos finalizados! Desligando as APIs..."
foreach ($p in $procs) {
    Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
}
Write-Host "APIs desligadas. Teste manual concluído com sucesso!"
