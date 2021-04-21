#!/usr/bin/env python3
#Equipe: Anne Caroline  - 470124, Juan Monteiro - 471930

import sys
import fileinput

#Vetor para auxiliar na verificação do uso das instâncias de axioma
CODIGOS_AXIOMA = ["A1","A2","A3","A4","A5","A6","A7","A8","A9","A10"]

def main(args):
  if len(args) != 1:
    print("Erro, argumentos inválidos\n\nUso: python main.py ARQUIVO")
  else:
    linhas = ler_arquivo(args)

    try:
      validar(linhas)
    except Exception as e:
      print(f"\n\nSolução inválida! {e}")
      exit(0)
    print("\n\nSolução válida!")

def ler_arquivo(arquivo):
  """Lê as linhas de um arquivo e as retorna em uma lista."""
  # TODO: incluir numero de linhas na lógica e nos exemplos
  linhas = list()
  try:
    with fileinput.input(files=(arquivo)) as f:
      print("Lendo arquivo de entrada", end='')
      for linha in f:
        str(linhas.append(linha))

      print("\tOK\n")
  except FileNotFoundError:
    print("\rArquivo não encontrado.  ", flush=True)
    exit(0)
  return linhas

def validar(linhas):
  usados = [False for x in linhas]
  formula = list()

  try:
    for i, linha in enumerate(linhas):
      print(f"L{i+1}: ", end="")
      partes = linha.rstrip().split()

      # verifica se o número da linha atual está correto
      if i != int(partes[0]) - 1:
        raise Exception("Número de linha inválido.")
      
      if len(partes) >= 1 and partes[-1] in ["HIP", "TEOREMA"]:
        formula.append(''.join(partes[1:-1]))
        codigo = partes[-1]
      elif len(partes) >= 2 and partes[-2] in ["MP"] + CODIGOS_AXIOMA:
        formula.append(''.join(partes[1:-2]))
        codigo = partes[-2]
      else:
        raise Exception("Não foi possível determinar conteúdo da linha.")
      
      validar_formula(formula[i])
      if codigo == "MP": # é modus ponens
        linhas = [int(x)-1 for x in partes[-1].split(',')]
        if len(linhas) != 2:
          raise Exception("Modus Ponens necessita de duas linhas.")
          
        a, b = linhas
        validar_linhas_mp(a, b, i)
        validar_aplicacao_mp(formula[a], formula[b], formula[i])
        usados[a] = usados[b] =True

      elif codigo in CODIGOS_AXIOMA: # é instancia de axioma
        argumentos = dict(a.split("=") for a in partes[-1].split(";"))
        correto = gerar_instancia(codigo, **argumentos)
        validar_axioma(formula[i], correto)
      elif codigo in ["HIP", "TEOREMA"]:
        pass

      print(f"OK | {linha}", end="")
  except Exception as e:
    print(f"ERRO! {e}\n\nSolução inválida.")
    exit(0)

  # verifica se todas as linhas (até a penultima) foram utilizadas
  if not all(usados[:-1]):
    raise Exception("Solução possui linhas não utilizadas.")

def gerar_instancia(nome, p=None, q=None, r=None):
  """Retorna uma instancia de axioma de acordo com o nome e substituiçoes informadas."""
  if validar_formula(p):
    if nome == "A10":
      return f"¬¬{p}>{p}"

    if validar_formula(q):
      if nome == "A1":
        return f"{p}>({q}>{p})"

      if nome == "A3":
        return f"{p}>({q}>({p}&{q}))"
      
      if nome == "A4":
        return f"({p}&{q})>{p}"
      
      if nome == "A5":
        return f"({p}&{q})>{q}"
      
      if nome == "A6":
        return f"{p}>({p}v{q})"
      
      if nome == "A7":
        return f"{q}>({p}v{q})"

      if nome == "A9":
        return f"({p}>{q})>(({p}>¬{q})>¬{p})"

      if validar_formula(r):
        if nome == "A2":
          return f"({p}>({q}>{r}))>(({p}>{q})>({p}>{r}))"

        if nome == "A8":
          return f"({p}>{r})>(({q}>{r})>(({p}v{q})>{r}))"
  raise Exception("Não foi possível gerar instancia de axioma.") # TODO: melhorar mensagem de erro.

def validar_parenteses(teste):
  """verifica se a quantidade de parenteses é válida"""

  cont = 0
  for a in teste:
   if a == '(': cont += 1
   elif a == ')': cont -= 1
  
  return cont == 0

def validar_formula(formula):
  """Verifica se uma fórmula é válida e gera uma exceção caso encontre um erro."""
  
  atomos = "abcdefghijklmnopqrstuwxyz"
  conectivos_b = "&v>"
  conectivos_u = "¬"
  auxiliares = "()"
  validos = atomos + conectivos_b + conectivos_u + auxiliares

  # verifica se a formula é vazia ou nula
  if not formula or formula == "":
    raise Exception("Fórmula inválida (vazia)")

  if not validar_parenteses(formula):
    raise Exception("Quantidade de parenteses inválida")

  for i, char in enumerate(formula):
    if char not in validos:
      raise Exception(f"Fórmula contém simbolos inválidos \"{char}\"")

    if char in conectivos_b:
      if (i == len(formula)) or (formula[i-1] not in atomos+')') or (formula[i+1] not in atomos+conectivos_u+'('):
        raise Exception("Erro no uso dos conectivos binarios.")

    if char in conectivos_u:
      if not (formula[i+1] in atomos+conectivos_b+conectivos_u+'('):
        raise Exception("Erro no uso do conectivo unário.")
    
    if char in auxiliares:
      if (char == '(' and (i == len(formula) or formula[i+1] == ')')) or  (char == ')' and i == 0):
        raise Exception("Erro no uso dos auxilares.")
  return True

def validar_axioma(original, correto):

  if original == correto: return True
  if original == f"({correto})": return True
  raise Exception("Axioma formulado incorretamente")

def validar_aplicacao_mp(linha1, linha2, resultado):
  """Verifica se o modus ponens foi aplicado corretamente."""

  if linha2 == f"{linha1}>{resultado}": return True
  if linha2 == f"({linha1})>{resultado}": return True
  if linha2 == f"{linha1}>({resultado})": return True
  if linha2 == f"({linha1}>{resultado})": return True
  if linha2 == f"({linha1})>({resultado})": return True

  if linha1 == f"{linha2}>{resultado}": return True
  if linha1 == f"({linha2})>{resultado}": return True
  if linha1 == f"{linha2}>({resultado})": return True
  if linha1 == f"({linha2}>{resultado})": return True
  if linha1 == f"({linha2})>({resultado})": return True
  raise Exception("MP inválido")

def validar_linhas_mp(a, b, i):
  """Verifica se o modus ponens é aplicado apenas em linhas anteriores"""

  if a > i or b > i: raise Exception("MP feito com linha posterior")
  if a == i or b == i: raise  Exception("MP feito com linha atual")
  return True

if __name__ == "__main__":
  main(sys.argv[1:])