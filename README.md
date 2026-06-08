# Projeto Analítico: Classificações e Avaliações Cinematográficas (TMDB)

## 🔗 Link de Acesso Público
A aplicação está em produção e pode ser acedida em: [https://aobtads.streamlit.app/](https://aobtads.streamlit.app/)

---

## 1. Definição do Problema
Como os fatores de produção (gênero cinematográfico, época de lançamento e composição de equipe técnica) determinam diretamente a aceitação crítica (notas ponderadas) e o engajamento do público (volume de votos) de uma obra cinematográfica?

---

## 2. Modelo Relacional e Engenharia de Dados (DER)
O banco de dados original foi decomposto e normalizado na 3ª Forma Normal (3FN), eliminando redundâncias e garantindo a integridade referencial através de Tabelas Fato e Dimensões.

### Estrutura das Tabelas
* **tb_filme (Tabela Fato):** Entidade central com granularidade de um registro por obra. Contém as métricas quantitativas primárias (`vote_average`, `vote_count`, `popularity`, `budget`, `revenue`).
* **d_calendario (Dimensão Temporal):** Tabela contínua para inteligência de tempo e segmentação cronológica.
* **tb_diretor & tb_ator (Dimensões Cadastrais):** Tabelas que isolam os dados da equipe técnica.
* **tb_filme_genero & tb_filme_ator (Tabelas Associativas):** Entidades de ligação necessárias para resolver os relacionamentos de cardinalidade muitos-para-muitos ($N:M$).

---

## 3. Dicionário de Dados

| Tabela | Coluna | Tipo de Dado | Descrição / Regra de Negócio |
| :--- | :--- | :--- | :--- |
| `tb_filme` | `id_filme` | INT (PK) | Identificador único do filme. |
| `tb_filme` | `title` | VARCHAR | Título original da obra. |
| `tb_filme` | `vote_average` | FLOAT | Média das notas atribuídas pelos utilizadores (0 a 10). |
| `tb_filme` | `vote_count` | INT | Quantidade total de votos recebidos pela obra. |
| `tb_filme` | `popularity` | FLOAT | Índice dinâmico de tração e engajamento do TMDB. |
| `tb_filme` | `data_lanc` | DATE | Data de lançamento oficial. |
| `tb_genero` | `id_genero` | INT (PK) | Identificador único do gênero. |
| `tb_genero` | `nome_genero` | VARCHAR | Nome descritivo do gênero cinematográfico. |
| `tb_diretor`| `id_diretor` | INT (PK) | Identificador único do diretor principal. |

---

## 4. Matriz de KPIs

| Nome do KPI | Fórmula Analítica | Objetivo do Indicador | Tipo de Sucesso |
| :--- | :--- | :--- | :--- |
| **Amostragem** | $\text{Contagem Distinct}(\text{id\_filme})$ | Monitorar o volume total de títulos que atendem aos filtros em memória. | Operacional |
| **Volume de Votos** | $\sum(\text{vote\_count})$ | Mensurar o tamanho da base amostral e o engajamento absoluto do público. | Popularidade |
| **Nota Média Ponderada**| $\frac{\sum(\text{vote\_average} \times \text{vote\_count})}{\sum(\text{vote\_count})}$ | Mitigar distorções de notas altas baseadas em poucos votos, extraindo o valor crítico real. | Crítico |
| **Popularidade Média** | $\text{Média}(\text{popularity})$ | Avaliar a tração e o interesse contínuo gerado pelas variáveis escolhidas. | Engajamento |
| **Taxa de Excelência** | $\frac{\text{Contagem}(\text{vote\_average} \ge 7.0)}{\text{Total de Filmes}} \times 100$ | Identificar a proporção de obras com alto índice de aprovação no segmento. | Qualidade |

---

## 5. Modelo Relacional
<img width="1405" height="738" alt="image" src="https://github.com/user-attachments/assets/741838f8-3075-43c8-abaa-d4243416610e" />
