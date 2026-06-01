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
O script automatizado (`benchmark.py`) executa o Locust em dois cenários duranto **3 minutos** cada:
- **Cenário Leve:** 50 usuários simultâneos (taxa de entrada de 10 novos usuários por segundo). 
- **Cenário Médio:** 200 usuários simultâneos (taxa de entrada de 50 novos usuários por segundo). 

### A Métrica (Latência no Percentil 95%)
O principal indicador de performance adotado foi a **Latência de 95% (p95)**. Ela nos informa o tempo máximo de resposta que 95% das requisições levaram para ser concluídas. Isso é muito mais confiável que a "média", pois elimina picos anômalos e reflete a experiência real da grande maioria dos usuários do serviço.

---

## Conclusões Gerais (Baseado nos Resultados)

A partir da coleta de dados em `resultados/*/stats.csv`, observou-se as seguintes tendências na arquitetura de microsserviços:

1. **A Supremacia do gRPC:** O gRPC foi, de forma absoluta, o protocolo mais rápido e eficiente testado (atingindo latências incríveis na casa dos **2ms a 6ms** no percentil 95%, tanto em Node.js quanto em Python). O uso do HTTP/2 combinado com buffers binários (Protobuf) se mostrou infinitamente superior no tráfego de listas massivas de dados comparado a arquivos de texto (JSON/XML).

2. **O Peso do GraphQL:** Como esperado, o GraphQL apresentou latências consistentemente maiores que REST e gRPC em todos os cenários. A flexibilidade de montar queries sob demanda tem um custo computacional significativo (validação do schema, resolução da árvore no lado do servidor), elevando os tempos de resposta.

3. **Node.js brilha em REST, mas engasga no SOAP:** O Node.js se provou excepcional para I/O básico em JSON (Node REST atingiu sólidos ~13ms mesmo no nível Médio). No entanto, sua arquitetura single-thread penou com o SOAP: a geração e transformação de enormes e complexas strings XML em puro JavaScript bloqueou a event loop, degradando a performance frente à concorrência.

4. **Desempenho do Python:** A performance do Python variou dependendo do servidor utilizado. Quando alavancado com `FastAPI`, servidores C-binding (`uvicorn`) e bibliotecas como `lxml` (escritas em C), o Python não só atingiu métricas competitivas no REST, mas demonstrou superioridade ao Node.js em cenários de uso intenso de CPU (como na criação concorrente de pacotes massivos XML no protocolo SOAP).


## Gráfico Comparativo de Desempenho
<img width="1400" height="700" alt="Image" src="https://github.com/user-attachments/assets/e6c4f1d6-3b26-4c4d-be27-bd06204f9b45" />
