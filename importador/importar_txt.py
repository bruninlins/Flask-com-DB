import os
import mysql.connector
import re

# ===============================
# CONFIGURAÇÕES
# ===============================

CAMINHO_TXT = r"C:\Users\Public\Recibimentos_dos_arquivos\dados.txt"
CAMINHO_ESTADO = "estado.txt"

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",
    "database": "usuario",
    "port": 3306,
    "use_pure": True
}

NOME_TABELA = "informacoes_formosa"

print("="*60)
print("IMPORTADOR DE DADOS DE SATÉLITE")
print("="*60)

# ===============================
# FUNÇÕES AUXILIARES
# ===============================

def ler_estado():
    """Lê a última posição processada"""
    if not os.path.exists(CAMINHO_ESTADO):
        return 0

    with open(CAMINHO_ESTADO, "r") as f:
        conteudo = f.read().strip()
        return int(conteudo) if conteudo.isdigit() else 0


def salvar_estado(posicao):
    """Salva a nova posição processada"""
    with open(CAMINHO_ESTADO, "w") as f:
        f.write(str(posicao))


def conectar_banco():
    """Conecta ao banco MySQL"""
    try:
        conexao = mysql.connector.connect(**DB_CONFIG)
        return conexao
    except Exception as e:
        print(f"✗ ERRO ao conectar ao banco: {e}")
        raise


def extrair_dados(linha):
    """Extrai nome do satélite, início e fim da linha"""
    try:
        # Procura pelo padrão completo antes da data: QUALQUER_COISA_YYYY_MM_DD
        # Extrai tudo antes da data como nome
        match_completo = re.search(r"^(.+?)_(\d{4})_(\d{2})_(\d{2})\.", linha)
        if not match_completo:
            return None
        
        nome = match_completo.group(1)  # Tudo antes da data
        ano = match_completo.group(2)
        mes_arquivo = match_completo.group(3)
        dia_arquivo = match_completo.group(4)

        inicio_match = re.search(
            r"INICIO - (\d{2})/(\d{2})==(\d{2}:\d{2}:\d{2})", linha
        )
        fim_match = re.search(
            r"FIM - (\d{2})/(\d{2})==(\d{2}:\d{2}:\d{2})", linha
        )

        if not inicio_match or not fim_match:
            return None

        dia_i, mes_i, hora_i = inicio_match.groups()
        dia_f, mes_f, hora_f = fim_match.groups()

        inicio = f"{ano}-{mes_i}-{dia_i} {hora_i}"
        fim = f"{ano}-{mes_f}-{dia_f} {hora_f}"

        return nome, inicio, fim

    except Exception as e:
        return None


# ===============================
# PROCESSAMENTO PRINCIPAL
# ===============================
def processar_arquivo():
    # Verificações iniciais
    if not os.path.exists(CAMINHO_TXT):
        print(f"✗ ERRO: Arquivo não encontrado: {CAMINHO_TXT}")
        return
    
    tamanho_arquivo = os.path.getsize(CAMINHO_TXT)
    print(f"\n📄 Arquivo: {CAMINHO_TXT}")
    print(f"📊 Tamanho: {tamanho_arquivo} bytes")
    
    posicao_anterior = ler_estado()
    print(f"📍 Posição anterior: {posicao_anterior}")
    
    if posicao_anterior >= tamanho_arquivo:
        print("\n✓ Arquivo já foi completamente processado!")
        return

    # Conectar ao banco
    print(f"\n🔌 Conectando ao banco '{DB_CONFIG['database']}'...")
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()
        print("✓ Conectado!")
    except:
        return

    linhas_processadas = 0
    linhas_inseridas = 0
    ultima_posicao = posicao_anterior

    try:
        print(f"\n📖 Lendo arquivo a partir da posição {posicao_anterior}...\n")
        
        with open(CAMINHO_TXT, "r", encoding="utf-8") as arquivo:
            arquivo.seek(posicao_anterior)

            while True:
                linha = arquivo.readline()
                
                # Se não há mais linhas, fim do arquivo
                if not linha:
                    break
                
                # Salva posição ANTES de processar
                ultima_posicao = arquivo.tell()
                linhas_processadas += 1

                linha = linha.strip()
                if not linha:
                    continue

                dados = extrair_dados(linha)

                if not dados:
                    if linhas_processadas <= 3:
                        print(f"⚠ Linha {linhas_processadas} ignorada (formato inválido)")
                    continue

                nome, inicio, fim = dados

                sql = """
                    INSERT INTO informacoes_formosa
                    (nome, inicio, fim)
                    VALUES (%s, %s, %s)
                """

                cursor.execute(sql, (nome, inicio, fim))
                linhas_inseridas += 1

                if linhas_inseridas <= 3:
                    print(f"✓ Inserido: {nome} | {inicio} → {fim}")

        # Commit
        conexao.commit()
        
        # Resultados
        print(f"\n{'='*60}")
        print(f"✓ PROCESSAMENTO CONCLUÍDO")
        print(f"{'='*60}")
        print(f"📊 Linhas lidas: {linhas_processadas}")
        print(f"✅ Linhas inseridas: {linhas_inseridas}")
        print(f"📍 Nova posição: {ultima_posicao}")
        print(f"{'='*60}\n")

    except Exception as e:
        print(f"\n✗ ERRO: {e}")
        import traceback
        traceback.print_exc()
        try:
            conexao.rollback()
        except:
            pass
        
    finally:
        cursor.close()
        conexao.close()
        
        if linhas_processadas > 0:
            salvar_estado(ultima_posicao)
            print(f"💾 Estado salvo!")


if __name__ == "__main__":
    processar_arquivo()