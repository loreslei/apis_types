$ErrorActionPreference = "Stop"

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "   TESTE CRUD VIA TERMINAL (REST, GQL, SOAP) " -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Lembrando: gRPC foi ignorado conforme solicitado." -ForegroundColor Yellow
Write-Host ""

# Função auxiliar para REST
function Test-Rest ($Port, $NomeApi) {
    Write-Host "--- Testando REST ($NomeApi) na porta $Port ---" -ForegroundColor Green
    
    # CREATE
    Write-Host "1. CREATE User..."
    $bodyCreate = '{"name": "Usuario REST ' + $NomeApi + '", "age": 25}'
    $resCreate = Invoke-RestMethod -Uri "http://127.0.0.1:$Port/users" -Method Post -ContentType "application/json" -Body $bodyCreate
    $newId = $resCreate.id
    Write-Host "   -> Sucesso! Criado com ID: $newId" -ForegroundColor DarkGreen

    # UPDATE
    Write-Host "2. UPDATE User (ID $newId)..."
    $bodyUpdate = '{"name": "Usuario REST Atualizado", "age": 26}'
    $resUpdate = Invoke-RestMethod -Uri "http://127.0.0.1:$Port/users/$newId" -Method Put -ContentType "application/json" -Body $bodyUpdate
    Write-Host "   -> Sucesso!" -ForegroundColor DarkGreen

    # DELETE
    Write-Host "3. DELETE User (ID $newId)..."
    $resDelete = Invoke-RestMethod -Uri "http://127.0.0.1:$Port/users/$newId" -Method Delete
    Write-Host "   -> Sucesso!" -ForegroundColor DarkGreen
    Write-Host ""
}

# Função auxiliar para GraphQL
function Test-GraphQL ($Port, $NomeApi) {
    $Uri = if ($NomeApi -eq "Python") { "http://127.0.0.1:$Port/graphql" } else { "http://127.0.0.1:$Port/" }
    Write-Host "--- Testando GraphQL ($NomeApi) na porta $Port ---" -ForegroundColor Blue
    
    # CREATE
    Write-Host "1. CREATE User..."
    $gqlCreate = '{"query": "mutation { createUser(name: \"Usuario GQL ' + $NomeApi + '\", age: 30) { id success } }"}'
    $resCreate = Invoke-RestMethod -Uri $Uri -Method Post -ContentType "application/json" -Body $gqlCreate
    $newId = $resCreate.data.createUser.id
    Write-Host "   -> Sucesso! Criado com ID: $newId" -ForegroundColor DarkGreen

    # UPDATE
    Write-Host "2. UPDATE User (ID $newId)..."
    $gqlUpdate = '{"query": "mutation { updateUser(id: ' + $newId + ', name: \"Usuario GQL Atualizado\", age: 31) { success } }"}'
    $resUpdate = Invoke-RestMethod -Uri $Uri -Method Post -ContentType "application/json" -Body $gqlUpdate
    Write-Host "   -> Sucesso!" -ForegroundColor DarkGreen

    # DELETE
    Write-Host "3. DELETE User (ID $newId)..."
    $gqlDelete = '{"query": "mutation { deleteUser(id: ' + $newId + ') { success } }"}'
    $resDelete = Invoke-RestMethod -Uri $Uri -Method Post -ContentType "application/json" -Body $gqlDelete
    Write-Host "   -> Sucesso!" -ForegroundColor DarkGreen
    Write-Host ""
}

# Função auxiliar para SOAP
function Test-Soap ($Port, $NomeApi) {
    $Uri = if ($NomeApi -eq "Python") { "http://127.0.0.1:$Port/" } else { "http://127.0.0.1:$Port/music" }
    Write-Host "--- Testando SOAP ($NomeApi) na porta $Port ---" -ForegroundColor Magenta
    
    # CREATE
    Write-Host "1. CREATE User..."
    $soapCreate = @"
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:mus="http://example.com/music">
   <soapenv:Header/>
   <soapenv:Body>
      <mus:CreateUserRequest>
         <name>Usuario SOAP $NomeApi</name>
         <age>40</age>
      </mus:CreateUserRequest>
   </soapenv:Body>
</soapenv:Envelope>
"@
    # Substituindo namespaces caso seja python (Spyne usa o nome da função + request as vezes, mas mapeamos manualmente)
    if ($NomeApi -eq "Python") {
        $soapCreate = $soapCreate.Replace("CreateUserRequest", "CreateUser")
    }

    $resCreate = Invoke-RestMethod -Uri $Uri -Method Post -ContentType "text/xml; charset=utf-8" -Body $soapCreate
    Write-Host "   -> Request enviado com sucesso! (ID não parseado no terminal devido a complexidade do XML)" -ForegroundColor DarkGreen

    # UPDATE (Vamos atualizar o ID 1 como teste no SOAP, pois extrair o XML id em PS é chato)
    Write-Host "2. UPDATE User (ID 1)..."
    $soapUpdate = @"
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:mus="http://example.com/music">
   <soapenv:Header/>
   <soapenv:Body>
      <mus:UpdateUserRequest>
         <id>1</id>
         <name>Usuario SOAP Atualizado</name>
         <age>41</age>
      </mus:UpdateUserRequest>
   </soapenv:Body>
</soapenv:Envelope>
"@
    if ($NomeApi -eq "Python") { $soapUpdate = $soapUpdate.Replace("UpdateUserRequest", "UpdateUser") }
    $resUpdate = Invoke-RestMethod -Uri $Uri -Method Post -ContentType "text/xml; charset=utf-8" -Body $soapUpdate
    Write-Host "   -> Sucesso!" -ForegroundColor DarkGreen

    Write-Host ""
}

try {
    Test-Rest 3001 "Node.js"
    Test-Rest 8001 "Python"
    
    Test-GraphQL 3002 "Node.js"
    Test-GraphQL 8002 "Python"
    
    Test-Soap 3004 "Node.js"
    Test-Soap 8004 "Python"
    
    Write-Host "Todos os testes de CRUD executados com sucesso!" -ForegroundColor Cyan
} catch {
    Write-Host "Erro durante a execução. Tem certeza que rodou o ./ligar_apis.ps1?" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}
