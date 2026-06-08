import pandas as pd
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "resultados")
CSV_PATH = os.path.join(RESULTS_DIR, "resultados_consolidados.csv")

def gerar_graficos():
    print(f"Lendo dados consolidados de: {CSV_PATH}")
    if not os.path.exists(CSV_PATH):
        print("Erro: O arquivo resultados_consolidados.csv não foi encontrado.")
        print("Você precisa rodar o benchmark pelo menos uma vez antes de gerar os gráficos avulsos.")
        return

    df_res = pd.read_csv(CSV_PATH)
    
    if not df_res.empty:
        # Extrair o tipo de API (ex: 'REST' de 'REST (Node)') caso não existam colunas separadas
        if 'API_Type' not in df_res.columns:
            df_res['API_Type'] = df_res['API'].apply(lambda x: x.split(' ')[0])
            df_res['Lang'] = df_res['API'].apply(lambda x: x.split(' ')[1].replace('(', '').replace(')', ''))
        
        api_types = df_res['API_Type'].unique()
        
        for api_type in api_types:
            df_subset = df_res[df_res['API_Type'] == api_type]
            pivot_df = df_subset.pivot(index='Nível', columns='Lang', values='Latência_95%')
            pivot_df = pivot_df.reindex(['Leve', 'Médio'])
            
            ax = pivot_df.plot(kind='bar', figsize=(10, 6), width=0.6, color=['#86efac','#f9a8d4'])
            plt.title(f'Comparativo de Desempenho: {api_type} (Node vs Python)', fontsize=16)
            plt.xlabel('Carga do Teste', fontsize=14)
            plt.ylabel('Latência 95% (ms)', fontsize=14)
            plt.xticks(rotation=0, fontsize=12)
            plt.legend(title='Linguagem', fontsize=12)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            
            chart_path = os.path.join(RESULTS_DIR, f'grafico_{api_type}.png')
            plt.savefig(chart_path)
            plt.close()
            print(f"Gráfico gerado: {chart_path}")
            
        print("\nSucesso! Todos os gráficos foram re-gerados com base nos dados consolidados.")
    else:
        print("O arquivo CSV está vazio. Nenhum dado gerado para criar os gráficos.")

if __name__ == '__main__':
    gerar_graficos()
