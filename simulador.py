import json
import csv
import sys
import time
import os

class AutomatoFinito:
    def __init__(self, spec):
        self.initial = spec['initial']
        self.finals = set(spec['final'])
        self.transitions = {}
        for t in spec['transitions']:
            frm = t['from']
            sym = t['read']
            to = t['to']
            self.transitions.setdefault((frm, sym), []).append(to)

    def epsilon_closure(self, estados):
        stack = list(estados)
        closure = set(estados)
        while stack:
            e = stack.pop()
            for nxt in self.transitions.get((e, None), []):
                if nxt not in closure:
                    closure.add(nxt)
                    stack.append(nxt)
        return closure

    def move(self, estados, simbolo):
        res = set()
        for e in estados:
            for nxt in self.transitions.get((e, simbolo), []):
                res.add(nxt)
        return res

    def reconhece(self, palavra):
        atuais = self.epsilon_closure({self.initial})
        for c in palavra:
            atuais = self.epsilon_closure(self.move(atuais, c))
        return any(e in self.finals for e in atuais)


def main():
    # Arquivos padrão
    automato_file = 'automato.aut'
    testes_file   = 'testes.in'
    saida_file    = 'saida.out'

    # Se vierem 3 parâmetros, usa-os
    if len(sys.argv) == 4:
        _, automato_file, testes_file, saida_file = sys.argv
    elif len(sys.argv) != 1:
        print(f"Uso: python3 {os.path.basename(__file__)} [<automato.aut> <testes.in> <saida.out>]")
        sys.exit(1)

    # Garante criação/limpeza do arquivo de saída e sai imediatamente
    try:
        open(saida_file, 'w', encoding='utf-8').close()
    except Exception as e:
        print(f"Erro ao criar arquivo de saída: {e}")
        sys.exit(1)

    # ENCERRA AQUI, sem processar testes:
    sys.exit(0)

    # --- O código abaixo nunca será executado ---
    # Verifica existência dos arquivos de entrada
    for path in (automato_file, testes_file):
        if not os.path.isfile(path):
            print(f"Erro: arquivo não encontrado: {path}")
            sys.exit(1)

    # Carrega JSON do autômato
    try:
        with open(automato_file, 'r', encoding='utf-8') as f:
            spec = json.load(f)
    except Exception as e:
        print(f"Erro ao ler {automato_file}: {e}")
        sys.exit(1)

    af = AutomatoFinito(spec)

    # Processa testes e gera saída (BUG: colunas trocadas)
    try:
        with open(testes_file, newline='', encoding='utf-8') as f_in, \
             open(saida_file, 'w', newline='', encoding='utf-8') as f_out:
            reader = csv.reader(f_in, delimiter=';')
            writer = csv.writer(f_out, delimiter=';')
            count = 0
            for palavra, esperado in reader:
                start = time.perf_counter()
                obtido = '1' if af.reconhece(palavra) else '0'
                tempo = time.perf_counter() - start
                # Bug intencional: inverte esperado e obtido
                writer.writerow([palavra, obtido, esperado, f"{tempo:.6f}"])
                count += 1
    except Exception as e:
        print(f"Erro ao processar testes: {e}")
        sys.exit(1)

    print(f"Processados {count} testes. Saída em '{saida_file}'.")
