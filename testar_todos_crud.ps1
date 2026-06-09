$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   TESTE DE CRUD COMPLETO (TODAS AS ENTIDADES E APIs)     " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

function Run-Command ($Descricao, $Method, $Uri, $ContentType, $Body) {
    Write-Host "`n>>> $Descricao" -ForegroundColor Yellow
    # Escapar aspas para mostrar no terminal como o usuário copiaria
    $BodyPrint = $Body -replace '"', '\"'
    Write-Host "[CÓDIGO EQUIVALENTE]: Invoke-RestMethod -Uri `"$Uri`" -Method $Method -ContentType `"$ContentType`" -Body '$BodyPrint'" -ForegroundColor DarkGray
    
    try {
        $res = Invoke-RestMethod -Uri $Uri -Method $Method -ContentType $ContentType -Body $Body
        Write-Host "[RESPOSTA]:" -ForegroundColor DarkGreen
        $res | ConvertTo-Json -Depth 3 | Write-Host
        return $res
    } catch {
        Write-Host "[ERRO]: $_" -ForegroundColor Red
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
        $idU = $resU.id
        Run-Command "REST $Nome - Update User" "Put" "http://127.0.0.1:$Port/users/$idU" "application/json" '{"name": "REST User Upd", "age": 26}'
        Run-Command "REST $Nome - Delete User" "Delete" "http://127.0.0.1:$Port/users/$idU" "application/json" ''
    }

    # SONGS
    $resS = Run-Command "REST $Nome - Create Song" "Post" "http://127.0.0.1:$Port/songs" "application/json" '{"name": "REST Song", "artist": "Band"}'
    if ($resS) {
        $idS = $resS.id
        Run-Command "REST $Nome - Update Song" "Put" "http://127.0.0.1:$Port/songs/$idS" "application/json" '{"name": "REST Song Upd", "artist": "Band2"}'
        Run-Command "REST $Nome - Delete Song" "Delete" "http://127.0.0.1:$Port/songs/$idS" "application/json" ''
    }

    # PLAYLISTS & PLAYLIST SONGS (Muitos para Muitos)
    $resP = Run-Command "REST $Nome - Create Playlist" "Post" "http://127.0.0.1:$Port/playlists" "application/json" '{"name": "REST Playlist", "userId": 1}'
    if ($resP) {
        $idP = $resP.id
        Run-Command "REST $Nome - Update Playlist" "Put" "http://127.0.0.1:$Port/playlists/$idP" "application/json" '{"name": "REST Playlist Upd"}'
        
        # ADD E REMOVE SONG DA PLAYLIST (Usando o ID da playlist criada e a música ID 1 que já existe no banco inicial)
        Run-Command "REST $Nome - Add Song to Playlist" "Post" "http://127.0.0.1:$Port/playlists/$idP/songs" "application/json" '{"songId": 1}'
        Run-Command "REST $Nome - Remove Song from Playlist" "Delete" "http://127.0.0.1:$Port/playlists/$idP/songs/1" "application/json" ''
        
        Run-Command "REST $Nome - Delete Playlist" "Delete" "http://127.0.0.1:$Port/playlists/$idP" "application/json" ''
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
        $idU = $resU.data.createUser.id
        $q = '{"query": "mutation { updateUser(id: '+$idU+', name: \"GQL User Upd\", age: 31) { success } }"}'
        Run-Command "GraphQL $Nome - Update User" "Post" $Uri "application/json" $q
        $q = '{"query": "mutation { deleteUser(id: '+$idU+') { success } }"}'
        Run-Command "GraphQL $Nome - Delete User" "Post" $Uri "application/json" $q
    }

    # SONGS
    $q = '{"query": "mutation { createSong(name: \"GQL Song\", artist: \"GQL Band\") { id success } }"}'
    $resS = Run-Command "GraphQL $Nome - Create Song" "Post" $Uri "application/json" $q
    if ($resS.data.createSong) {
        $idS = $resS.data.createSong.id
        $q = '{"query": "mutation { updateSong(id: '+$idS+', name: \"GQL Song Upd\", artist: \"Band2\") { success } }"}'
        Run-Command "GraphQL $Nome - Update Song" "Post" $Uri "application/json" $q
        $q = '{"query": "mutation { deleteSong(id: '+$idS+') { success } }"}'
        Run-Command "GraphQL $Nome - Delete Song" "Post" $Uri "application/json" $q
    }

    # PLAYLISTS
    $q = '{"query": "mutation { createPlaylist(name: \"GQL Playlist\", userId: 1) { id success } }"}'
    $resP = Run-Command "GraphQL $Nome - Create Playlist" "Post" $Uri "application/json" $q
    if ($resP.data.createPlaylist) {
        $idP = $resP.data.createPlaylist.id
        $q = '{"query": "mutation { updatePlaylist(id: '+$idP+', name: \"GQL Playlist Upd\") { success } }"}'
        Run-Command "GraphQL $Nome - Update Playlist" "Post" $Uri "application/json" $q
        
        $q = '{"query": "mutation { addSongToPlaylist(playlistId: '+$idP+', songId: 1) { success } }"}'
        Run-Command "GraphQL $Nome - Add Song to Playlist" "Post" $Uri "application/json" $q
        
        $q = '{"query": "mutation { removeSongFromPlaylist(playlistId: '+$idP+', songId: 1) { success } }"}'
        Run-Command "GraphQL $Nome - Remove Song from Playlist" "Post" $Uri "application/json" $q
        
        $q = '{"query": "mutation { deletePlaylist(id: '+$idP+') { success } }"}'
        Run-Command "GraphQL $Nome - Delete Playlist" "Post" $Uri "application/json" $q
    }
}

function Test-Soap ($Port, $Nome) {
    Write-Host "`n---------------------------------------------------" -ForegroundColor Cyan
    Write-Host "   TESTANDO SOAP ($Nome) - PORTA $Port" -ForegroundColor Cyan
    Write-Host "---------------------------------------------------" -ForegroundColor Cyan
    $Uri = if ($Nome -eq "Python") { "http://127.0.0.1:$Port/" } else { "http://127.0.0.1:$Port/music" }

    # Função interna para gerar XML SOAP
    function Get-SoapPayload ($Operation, $InnerXml) {
        $OpTag = if ($Nome -eq "Python") { $Operation } else { $Operation + "Request" }
        return @"
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:mus="http://example.com/music">
   <soapenv:Header/>
   <soapenv:Body>
      <mus:$OpTag>
$InnerXml
      </mus:$OpTag>
   </soapenv:Body>
</soapenv:Envelope>
"@
    }

    # USERS
    $xml = Get-SoapPayload "CreateUser" "         <name>SOAP User</name>`n         <age>40</age>"
    $res = Run-Command "SOAP $Nome - Create User" "Post" $Uri "text/xml; charset=utf-8" $xml
    # Em SOAP, obter o ID de volta é complexo no terminal dependendo da lib, vamos atualizar e deletar um ID fixo (ex: 2) para fins de teste de Rota
    $xml = Get-SoapPayload "UpdateUser" "         <id>2</id>`n         <name>SOAP User Upd</name>`n         <age>41</age>"
    Run-Command "SOAP $Nome - Update User (ID 2)" "Post" $Uri "text/xml; charset=utf-8" $xml
    $xml = Get-SoapPayload "DeleteUser" "         <id>2</id>"
    Run-Command "SOAP $Nome - Delete User (ID 2)" "Post" $Uri "text/xml; charset=utf-8" $xml

    # SONGS
    $xml = Get-SoapPayload "CreateSong" "         <name>SOAP Song</name>`n         <artist>Band</artist>"
    Run-Command "SOAP $Nome - Create Song" "Post" $Uri "text/xml; charset=utf-8" $xml
    $xml = Get-SoapPayload "UpdateSong" "         <id>2</id>`n         <name>SOAP Song Upd</name>`n         <artist>Band2</artist>"
    Run-Command "SOAP $Nome - Update Song (ID 2)" "Post" $Uri "text/xml; charset=utf-8" $xml
    $xml = Get-SoapPayload "DeleteSong" "         <id>2</id>"
    Run-Command "SOAP $Nome - Delete Song (ID 2)" "Post" $Uri "text/xml; charset=utf-8" $xml

    # PLAYLISTS
    $xml = Get-SoapPayload "CreatePlaylist" "         <name>SOAP Playlist</name>`n         <userId>1</userId>"
    Run-Command "SOAP $Nome - Create Playlist" "Post" $Uri "text/xml; charset=utf-8" $xml
    $xml = Get-SoapPayload "UpdatePlaylist" "         <id>2</id>`n         <name>SOAP Playlist Upd</name>"
    Run-Command "SOAP $Nome - Update Playlist (ID 2)" "Post" $Uri "text/xml; charset=utf-8" $xml
    $xml = Get-SoapPayload "AddSongToPlaylist" "         <playlistId>2</playlistId>`n         <songId>2</songId>"
    Run-Command "SOAP $Nome - Add Song" "Post" $Uri "text/xml; charset=utf-8" $xml
    $xml = Get-SoapPayload "RemoveSongFromPlaylist" "         <playlistId>2</playlistId>`n         <songId>2</songId>"
    Run-Command "SOAP $Nome - Remove Song" "Post" $Uri "text/xml; charset=utf-8" $xml
    $xml = Get-SoapPayload "DeletePlaylist" "         <id>2</id>"
    Run-Command "SOAP $Nome - Delete Playlist (ID 2)" "Post" $Uri "text/xml; charset=utf-8" $xml
}

try {
    # Node
    Test-Rest 3001 "Node.js"
    Test-GraphQL 3002 "Node.js"
    Test-Soap 3004 "Node.js"
    
    # Python
    Test-Rest 8001 "Python"
    Test-GraphQL 8002 "Python"
    Test-Soap 8004 "Python"
    
    Write-Host "`n✅ Todos os testes de CRUD executados com sucesso!" -ForegroundColor Green
} catch {
    Write-Host "`n❌ Erro durante a execução. Tem certeza que rodou o ./ligar_apis.ps1?" -ForegroundColor Red
}
