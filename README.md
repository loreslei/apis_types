# Serviços de API Streaming - Teste de Carga

Este projeto contém 8 implementações de APIs baseadas no modelo de streaming de músicas (REST, GraphQL, gRPC, SOAP - em Node.js e Python) além dos testes de carga com Locust para realizar o comparativo de performance.


## Equipe

| Nome                                | Matrícula             |
|-------------------------------------|-----------------------|
| Bianca Oriá Leite                   | 2320323               |
| João Felipe Ribeiro de Melo         | 2315045               |
| João Pedro Ribeiro Mendes           | 2315069               |
| Lorenna Aguiar Nunes                | 2315026               |



## Testes e Métricas com Locust 

As portas utilizadas são:

| Protocolo  | Node.js | Python |
|------------|---------|--------|
| REST       | 3001    | 8001   |
| GraphQL    | 3002    | 8002   |
| gRPC       | 3003    | 8003   |
| SOAP       | 3004    | 8004   |


Os testes foram criados realizando consultas GET (`getUsers` e `getUserPlaylists`). Respeitando a modelagem do UML disponibilizado do streaming de música simulado.

### Requisições Avaliadas
As operações testadas (que variam sua forma de chamada de acordo com o protocolo - REST, GraphQL, gRPC, SOAP) correspondem a:
1. **`getUsers`**: Recuperar uma lista ampla de todos os usuários do sistema.
2. **`getUserPlaylists`**: Recuperar listas de reprodução associadas a um `userId` específico.


### Níveis de Carga Aplicados
O script executa o Locust em dois cenários durando **3 minutos** cada:
- **Cenário Leve:** 50 usuários simultâneos (taxa de entrada de 10 novos usuários por segundo). 
- **Cenário Médio:** 200 usuários simultâneos (taxa de entrada de 50 novos usuários por segundo). 

### A Métrica (Latência no Percentil 95%)
O principal indicador de performance adotado foi a **Latência de 95% (p95)** por informar o tempo máximo de resposta que 95% das requisições levaram para ser concluídas. 

---

## Gráficos Comparativos de Desempenho

Abaixo estão os resultados detalhados de cada protocolo sob as cargas Leve e Média:

### 1. REST (Node vs Python)
<img width="1000" height="600" alt="Image" src="https://github.com/user-attachments/assets/4ad28758-3686-4164-854d-529b1d3ca437" />

No protocolo REST, o Node.js demonstra uma estabilidade impressionante, mantendo a latência próxima de zero mesmo sob carga Média. O Python, por outro lado, sofre uma degradação severa no cenário Médio, com a latência saltando para mais de 2000ms. Isso evidencia a alta eficiência do V8 (engine do Node) na serialização e deserialização nativa de JSON sob concorrência.

### 2. GraphQL (Node vs Python)
<img width="1000" height="600" alt="Image" src="https://github.com/user-attachments/assets/12259458-09bb-4e60-8bd2-3d6f917a4b6f" />

O GraphQL exige mais processamento devido à resolução da árvore de consultas (resolvers) e validação de schemas. Aqui, o Node.js tem um leve aumento de latência no cenário Médio (ficando abaixo de 200ms), mas o Python sofre um grande gargalo, alcançando 1400ms. A resolução assíncrona do Node.js lida muito melhor com a complexidade do GraphQL do que a implementação em Python.

### 3. SOAP (Node vs Python)
<img width="1000" height="600" alt="Image" src="https://github.com/user-attachments/assets/769755f3-6632-418f-9fd8-e7070f7d7748" />

O SOAP baseia-se em XML, conhecido por ser verboso e custoso para processamento. Surpreendentemente, o Node.js manteve um desempenho excelente. Já o Python entrou em colapso total: a latência no cenário Leve já passou dos 2000ms e no Médio ultrapassou inacreditáveis 6000ms. O custo de validação rigorosa de schemas e a montagem dinâmica de pacotes XML no Python destruíram o desempenho sob concorrência.

### 4. gRPC (Node vs Python)
<img width="1000" height="600" alt="Image" src="https://github.com/user-attachments/assets/01f6deaf-c6f3-486b-a9db-541617ab1e26" />

Aqui o cenário muda completamente! O gRPC, operando sobre HTTP/2 e trafegando buffers binários (Protobuf), eliminou o gargalo de processamento de texto. Ambos os servidores atingiram latências irreais de **2ms a 6ms**, tanto no cenário Leve quanto no Médio. Sem o peso do parse de JSON ou XML, o Python conseguiu empatar em velocidade e eficiência com o Node.js.

### 5. Gráfico Comparativo Geral (Linguagens e Tipos de API)
<img width="1400" height="700" alt="Image" src="https://github.com/user-attachments/assets/e6c4f1d6-3b26-4c4d-be27-bd06204f9b45" />

---

## Conclusões Gerais

A partir da coleta de dados detalhada e separada por protocolo, observou-se as seguintes tendências definitivas:

1. **A Supremacia Absoluta do gRPC:** O gRPC foi o grande vencedor e o único ambiente onde as duas linguagens brilharam juntas. A utilização do HTTP/2 combinado com Protobufs elimina completamente a latência de rede e de serialização. Para microsserviços de altíssima performance, o gRPC iguala a capacidade das linguagens.

2. **Node.js Esmaga em Protocolos Baseados em Texto:** Nos cenários trafegando texto (REST/JSON, GraphQL/JSON e SOAP/XML), o Node.js mostrou uma vantagem esmagadora sobre o Python. A arquitetura orientada a eventos e o poder do motor V8 provaram ser extremamente resilientes na manipulação e envio de strings e objetos sob milhares de requisições simultâneas.

3. **O Colapso do Python sob Carga Média:** Em requisições massivas (cenário Médio), o Python não conseguiu lidar bem com I/O intensivo envolvendo serialização de dados de texto. O pior cenário se deu no SOAP, onde a complexidade das bibliotecas de XML engasgou completamente o servidor (mais de 6 segundos de latência). O Python foi eficiente apenas no gRPC.

4. **O Custo Computacional do GraphQL:** Como esperado teoricamente, montar consultas sob demanda no GraphQL afeta a latência em ambas as linguagens. No Node.js a degradação foi leve em comparação ao REST, enquanto no Python o impacto tornou a API visivelmente mais lenta (1400ms).
