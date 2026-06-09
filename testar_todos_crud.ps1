$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   TESTE DE CRUD COMPLETO (TODAS AS ENTIDADES E APIs)     " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

function Run-Command ($Descricao, $Method, $Uri, $ContentType, $Body, $MostrarTodos = $false) {
    Write-Host "`n>>> $Descricao" -ForegroundColor Yellow
    if ($Body) {
        $BodyPrint = $Body -replace '"', '\"'
        Write-Host "[CODIGO EQUIVALENTE]: Invoke-WebRequest -Uri `"$Uri`" -Method $Method -ContentType `"$ContentType`" -Body '$BodyPrint'" -ForegroundColor DarkGray
    } else {
        Write-Host "[CODIGO EQUIVALENTE]: Invoke-WebRequest -Uri `"$Uri`" -Method $Method" -ForegroundColor DarkGray
    }
    
    try {
        if ($ContentType -like "*xml*") {
            # Usar Invoke-WebRequest para pegar a string XML pura
            if ($Body) {
                $rawRes = Invoke-WebRequest -Uri $Uri -Method $Method -ContentType $ContentType -Body $Body
            } else {
                $rawRes = Invoke-WebRequest -Uri $Uri -Method $Method
            }
            Write-Host "[RESPOSTA (RAW XML)]:" -ForegroundColor DarkGreen
            Write-Host $rawRes.Content -ForegroundColor Gray
            Write-Host ">>> Aguardando 8 segundos para voce analisar..." -ForegroundColor Cyan
            Start-Sleep -Seconds 8
            return $rawRes.Content
        } else {
            if ($Body) {
                $res = Invoke-RestMethod -Uri $Uri -Method $Method -ContentType $ContentType -Body $Body
            } else {
                $res = Invoke-RestMethod -Uri $Uri -Method $Method
            }
            
            Write-Host "[RESPOSTA]:" -ForegroundColor DarkGreen
            
            if ($MostrarTodos) {
                $res | ConvertTo-Json -Depth 3 | Write-Host
            } else {
                if ($null -ne $res -and $res.GetType().IsArray -and $res.Length -gt 2) {
                    $res | Select-Object -Last 2 | ConvertTo-Json -Depth 3 | Write-Host
                    Write-Host "(Mostrando apenas os ultimos 2 itens de $($res.Length))" -ForegroundColor Gray
                } else {
                    $res | ConvertTo-Json -Depth 3 | Write-Host
                }
            }
            Write-Host ">>> Aguardando 8 segundos para voce analisar..." -ForegroundColor Cyan
            Start-Sleep -Seconds 8
            return $res
        }
    } catch {
        Write-Host "[ERRO]: $_" -ForegroundColor Red
        if ($_.Exception.Response) {
            $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
            $errBody = $reader.ReadToEnd()
            Write-Host $errBody -ForegroundColor DarkRed
        }
        Start-Sleep -Seconds 8
        return $null
    }
}

function Test-Rest ($Port, $Nome) {
    Write-Host "`n---------------------------------------------------" -ForegroundColor Blue
    Write-Host "   TESTANDO REST ($Nome) - PORTA $Port" -ForegroundColor Blue
    Write-Host "---------------------------------------------------" -ForegroundColor Blue

    # USERS
    $resU = Run-Command "REST $Nome - Create User" "Post" "http://127.0.0.1:$Port/users" "application/json" '{"name": "REST User", "age": 25}'
    if ($resU) {
        Run-Command "REST $Nome - GET Users (Todos apos o Create)" "Get" "http://127.0.0.1:$Port/users" "application/json" "" $true
        
        $idU = $resU.id
        Run-Command "REST $Nome - Update User" "Put" "http://127.0.0.1:$Port/users/$idU" "application/json" '{"name": "REST User Upd", "age": 26}'
        Run-Command "REST $Nome - GET Users (Verificando update)" "Get" "http://127.0.0.1:$Port/users" "application/json" "" $false
        
        Run-Command "REST $Nome - Delete User" "Delete" "http://127.0.0.1:$Port/users/$idU" "application/json" ''
        Run-Command "REST $Nome - GET Users (Verificando delete)" "Get" "http://127.0.0.1:$Port/users" "application/json" "" $false
    }
}

function Test-GraphQL ($Port, $Nome) {
    Write-Host "`n---------------------------------------------------" -ForegroundColor Magenta
    Write-Host "   TESTANDO GRAPHQL ($Nome) - PORTA $Port" -ForegroundColor Magenta
    Write-Host "---------------------------------------------------" -ForegroundColor Magenta
    $Uri = if ($Nome -eq "Python") { "http://127.0.0.1:$Port/graphql" } else { "http://127.0.0.1:$Port/" }

    # USERS
    $q = '{"query": "mutation { createUser(name: \"GQL User\", age: 30) { id success } }"}'
    $resU = Run-Command "GraphQL $Nome - Create User" "Post" $Uri "application/json" $q
    if ($resU.data.createUser) {
        $qGet = '{"query": "query { getUsers { id name age } }"}'
        Run-Command "GraphQL $Nome - GET Users (Todos apos o Create)" "Post" $Uri "application/json" $qGet $true
        
        $idU = $resU.data.createUser.id
        $q = '{"query": "mutation { updateUser(id: '+$idU+', name: \"GQL User Upd\", age: 31) { success } }"}'
        Run-Command "GraphQL $Nome - Update User" "Post" $Uri "application/json" $q
        
        Run-Command "GraphQL $Nome - GET Users (Verificando update)" "Post" $Uri "application/json" $qGet $false
        
        $q = '{"query": "mutation { deleteUser(id: '+$idU+') { success } }"}'
        Run-Command "GraphQL $Nome - Delete User" "Post" $Uri "application/json" $q
        Run-Command "GraphQL $Nome - GET Users (Verificando delete)" "Post" $Uri "application/json" $qGet $false
    }
}

function Test-Soap ($Port, $Nome) {
    Write-Host "`n---------------------------------------------------" -ForegroundColor Cyan
    Write-Host "   TESTANDO SOAP ($Nome) - PORTA $Port" -ForegroundColor Cyan
    Write-Host "---------------------------------------------------" -ForegroundColor Cyan
    $Uri = if ($Nome -eq "Python") { "http://127.0.0.1:$Port/" } else { "http://127.0.0.1:$Port/music" }

    function Get-SoapPayload ($Operation, $InnerXml) {
        $OpTag = if ($Nome -eq "Python") { $Operation } else { $Operation + "Request" }
        if ([string]::IsNullOrWhiteSpace($InnerXml)) {
            return @"
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:mus="http://example.com/music">
   <soapenv:Header/>
   <soapenv:Body>
      <mus:$OpTag xmlns="http://example.com/music"/>
   </soapenv:Body>
</soapenv:Envelope>
"@
        } else {
            return @"
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:mus="http://example.com/music">
   <soapenv:Header/>
   <soapenv:Body>
      <mus:$OpTag xmlns="http://example.com/music">
$InnerXml
      </mus:$OpTag>
   </soapenv:Body>
</soapenv:Envelope>
"@
        }
    }

    # USERS
    $xml = Get-SoapPayload "CreateUser" "         <name>SOAP User</name>`n         <age>40</age>"
    $res = Run-Command "SOAP $Nome - Create User" "Post" $Uri "text/xml; charset=utf-8" $xml
    
    $xmlGet = Get-SoapPayload "GetUsers" ""
    Run-Command "SOAP $Nome - GET Users (Todos apos o Create)" "Post" $Uri "text/xml; charset=utf-8" $xmlGet $true
    
    $xml = Get-SoapPayload "UpdateUser" "         <id>2</id>`n         <name>SOAP User Upd</name>`n         <age>41</age>"
    Run-Command "SOAP $Nome - Update User (ID 2)" "Post" $Uri "text/xml; charset=utf-8" $xml
    
    Run-Command "SOAP $Nome - GET Users (Verificando update)" "Post" $Uri "text/xml; charset=utf-8" $xmlGet $false
    
    $xml = Get-SoapPayload "DeleteUser" "         <id>2</id>"
    Run-Command "SOAP $Nome - Delete User (ID 2)" "Post" $Uri "text/xml; charset=utf-8" $xml
    
    Run-Command "SOAP $Nome - GET Users (Verificando delete)" "Post" $Uri "text/xml; charset=utf-8" $xmlGet $false
}

try {
    Test-Rest 3001 "Node.js"
    Test-Rest 8001 "Python"
    Test-GraphQL 3002 "Node.js"
    Test-Soap 8004 "Python"
    
    Write-Host "`n[SUCESSO] Todos os testes executados com pausas!" -ForegroundColor Green
} catch {
    Write-Host "`n[ERRO] Ocorreu um problema." -ForegroundColor Red
}
