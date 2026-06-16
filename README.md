# Projeto Analítico: Classificações e Avaliações Cinematográficas (TMDB)

## 🔗 Link de Acesso Público
O projeto pode ser acessado em: [https://aobtads.streamlit.app/](https://aobtads.streamlit.app/)

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
| `tb_filme` | `id_filme` | INT (PK) | Identificador único e exclusivo de cada obra cinematográfica. |
| `tb_filme` | `title` | VARCHAR | Título oficial distribuído comercialmente. |
| `tb_filme` | `vote_average` | FLOAT | Média aritmética simples das notas atribuídas pelos usuários (0 a 10). |
| `tb_filme` | `vote_count` | INT | Volume absoluto de votos computados para o título. |
| `tb_filme` | `popularity` | FLOAT | Índice de tração, acessos e buscas diárias calculado pelo TMDB. |
| `tb_filme` | `budget` | FLOAT | Orçamento total declarado para a produção da obra em dólares ($). |
| `tb_filme` | `revenue` | FLOAT | Faturamento bruto global acumulado nas bilheterias em dólares ($). |
| `tb_filme` | `data_lanc` | DATE | Data de lançamento oficial do filme no mercado de origem. |
| `tb_filme` | `id_diretor` | INT (FK) | Chave estrangeira que aponta para o realizador na tabela `tb_diretor`. |
| `tb_filme` | `ano_lanc` | INT | Atributo derivado via código correspondente ao ano da `data_lanc`. |
| `tb_genero` | `id_genero` | INT (PK) | Identificador único de cada gênero cinematográfico. |
| `tb_genero` | `nome_genero` | VARCHAR | Nome descritivo da classificação do gênero (ex: Ação, Drama, Comédia). |
| `tb_filme_genero` | `id_filme` | INT (FK) | Parte da chave primária composta; aponta para `tb_filme`. |
| `tb_filme_genero` | `id_genero` | INT (FK) | Parte da chave primária composta; aponta para `tb_genero`. |
| `tb_diretor` | `id_diretor` | INT (PK) | Identificador único de cada diretor mapeado no ecossistema. |
| `tb_diretor` | `nome_diretor` | VARCHAR | Nome completo do diretor principal da obra. |
| `tb_ator` | `id_ator` | INT (PK) | Identificador único de cada ator ou atriz mapeado no ecossistema. |
| `tb_ator` | `nome_ator` | VARCHAR | Nome completo do integrante do elenco principal. |
| `tb_filme_ator` | `id_filme` | INT (FK) | Parte da chave primária composta; aponta para `tb_filme`. |
| `tb_filme_ator` | `id_ator` | INT (FK) | Parte da chave primária composta; aponta para `tb_ator`. |
| `d_calendario` | `data` | DATE (PK) | Chave primária temporal contínua que faz a ligação com a fato. |
| `d_calendario` | `ano` | INT | Ano civil extraído da respectiva data para indexação no slider. |

---

## 4. Matriz de KPIs

| Nome do KPI | Fórmula Analítica | Objetivo do Indicador | Tipo de Sucesso |
| :--- | :--- | :--- | :--- |
| **Amostragem** | $$\text{Contagem de Filmes}$$ | Monitorar o volume total de títulos que atendem aos filtros em memória. | Operacional |
| **Volume de Votos** | $$\sum(\text{Votos})$$ | Mensurar o tamanho da base amostral e o engajamento absoluto do público. | Popularidade |
| **Nota Média Ponderada**| $$\frac{\sum(\text{Nota} \times \text{Votos})}{\sum(\text{Votos})}$$ | Mitigar distorções de notas altas baseadas em poucos votos, extraindo o valor crítico real. | Crítico |
| **Popularidade Média** | $$\text{Média}(\text{Popularidade})$$ | Avaliar a tração e o interesse contínuo gerado pelas variáveis escolhidas. | Engajamento |
| **Taxa de Excelência** | $$\frac{\text{Contagem}(\text{Nota} \ge 7.0)}{\text{Total de Filmes}} \times 100$$ | Identificar a proporção de obras com alto índice de aprovação no segmento. | Qualidade |

---

## 5. Modelo Relacional
<img width="1405" height="738" alt="image" src="https://github.com/user-attachments/assets/741838f8-3075-43c8-abaa-d4243416610e" />
