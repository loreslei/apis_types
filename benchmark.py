import subprocess
import time
import os
import pandas as pd
import matplotlib.pyplot as plt
import sys

# Diretórios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "resultados")

if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

# Serviços para rodar em paralelo
SERVICES = [
    {"cmd": ["node", "node_services/rest/app.js"], "name": "REST Node"},
    {"cmd": ["node", "node_services/graphql/app.js"], "name": "GraphQL Node"},
    {"cmd": ["node", "node_services/grpc/app.js"], "name": "gRPC Node"},
    {"cmd": ["node", "node_services/soap/app.js"], "name": "SOAP Node"},
    {"cmd": [sys.executable, "python_services/rest/app.py"], "name": "REST Python"},
    {"cmd": [sys.executable, "python_services/graphql/app.py"], "name": "GraphQL Python"},
    {"cmd": [sys.executable, "python_services/grpc/app.py"], "name": "gRPC Python"},
    {"cmd": [sys.executable, "python_services/soap/app.py"], "name": "SOAP Python"},
]

# Níveis de Teste
TEST_LEVELS = {
    "Leve": {"users": 50, "spawn_rate": 10, "time": "3m"},
    "Médio": {"users": 200, "spawn_rate": 50, "time": "3m"}
}

# Alvos
TARGETS = [
    ("SOAP (Python)", "locust/locust_soap.py", "http://127.0.0.1:8004"),
    ("REST (Node)", "locust/locust_rest.py", "http://127.0.0.1:3001"),
    ("REST (Python)", "locust/locust_rest.py", "http://127.0.0.1:8001"),
    ("GraphQL (Node)", "locust/locust_graphql.py", "http://127.0.0.1:3002"),
    ("GraphQL (Python)", "locust/locust_graphql.py", "http://127.0.0.1:8002"),
    ("gRPC (Node)", "locust/locust_grpc.py", "http://127.0.0.1:3003"),
    ("gRPC (Python)", "locust/locust_grpc.py", "http://127.0.0.1:8003"),
    ("SOAP (Node)", "locust/locust_soap.py", "http://127.0.0.1:3004"),
]

def run_benchmark():
    processes = []
    print("Iniciando todos os serviços da API...")
    for s in SERVICES:
        p = subprocess.Popen(s["cmd"], cwd=BASE_DIR, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        processes.append(p)
    
    print("Aguardando 8 segundos para que todas as APIs inicializem completamente...")
    time.sleep(8)
    
    results = []

    try:
        for level, config in TEST_LEVELS.items():
            print(f"\n--- Iniciando Bateria de Testes: Nível {level.upper()} ---")
            for api_name, locust_file, host in TARGETS:
                print(f"Testando {api_name} no nível {level}...")
                
                # Ex: "REST (Node)" -> api_type = "REST", lang = "node"
                parts = api_name.split(" ")
                api_type = parts[0]
                lang = parts[1].replace("(", "").replace(")", "").lower()
                
                target_dir = os.path.join(RESULTS_DIR, api_type, lang)
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                
                csv_prefix = os.path.join(target_dir, f"resultado_{level}")
                
                cmd = [
                    sys.executable, "-m", "locust",
                    "-f", locust_file,
                    "--headless",
                    "-u", str(config["users"]),
                    "-r", str(config["spawn_rate"]),
                    "--run-time", config["time"],
                    "--host", host,
                    "--csv", csv_prefix
                ]
                
                subprocess.run(cmd, cwd=BASE_DIR, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                stats_file = f"{csv_prefix}_stats.csv"
                if os.path.exists(stats_file):
                    df = pd.read_csv(stats_file)
                    agg_row = df[df['Name'] == 'Aggregated']
                    if not agg_row.empty:
                        p95_latency = agg_row['95%'].values[0]
                        results.append({
                            "API": api_name,
                            "Nível": level,
                            "Latência_95%": p95_latency
                        })
    finally:
        print("\nFinalizando APIs...")
        for p in processes:
            p.terminate()

    print("\nGerando gráfico de barras comparativo...")
    df_res = pd.DataFrame(results)
    if not df_res.empty:
        pivot_df = df_res.pivot(index='Nível', columns='API', values='Latência_95%')
        pivot_df = pivot_df.reindex(['Leve', 'Médio'])
        
        ax = pivot_df.plot(kind='bar', figsize=(14, 7), width=0.85, colormap='Paired')
        plt.title('Comparativo de Desempenho (Latência no Percentil 95%)', fontsize=16)
        plt.xlabel('Carga do Teste', fontsize=14)
        plt.ylabel('Latência 95% (ms)', fontsize=14)
        plt.xticks(rotation=0, fontsize=12)
        plt.legend(title='Tipos de API', bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=11)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        chart_path = os.path.join(RESULTS_DIR, 'grafico_comparativo.png')
        plt.savefig(chart_path)
        df_res.to_csv(os.path.join(RESULTS_DIR, 'resultados_consolidados.csv'), index=False)
        print(f"\nSucesso! O gráfico foi salvo em: {chart_path}")
        print("Os resultados crus também foram salvos no diretório /resultados.")
    else:
        print("Nenhum dado gerado para criar o gráfico.")

if __name__ == '__main__':
    run_benchmark()
