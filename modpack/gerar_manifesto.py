#!/usr/bin/env python3
"""Gera modpack/manifest.json com os arquivos de modpack/mods (e config/, se houver) apontando para um commit fixo.
Uso: python3 modpack/gerar_manifesto.py <commit> <versao>"""
import hashlib, json, os, sys
commit, versao = sys.argv[1], sys.argv[2]
raiz = os.path.dirname(os.path.abspath(__file__))
arquivos = []
for pasta in ('mods', 'config', 'resourcepacks'):
    base = os.path.join(raiz, pasta)
    if not os.path.isdir(base): continue
    for r, _, fs in os.walk(base):
        for f in sorted(fs):
            p = os.path.join(r, f); rel = os.path.relpath(p, raiz).replace(os.sep, '/')
            dados = open(p, 'rb').read()
            arquivos.append({'caminho': rel, 'sha1': hashlib.sha1(dados).hexdigest(), 'tamanho': len(dados),
                             'url': f'https://raw.githubusercontent.com/panfletagemdigitalmkt/comunidade-big-pack/{commit}/modpack/{rel}'})
json.dump({'versao': versao, 'minecraft': '26.3', 'neoforge': '26.3.0.115', 'arquivos': arquivos}, open(os.path.join(raiz, 'manifest.json'), 'w'), ensure_ascii=False, indent=1)
print(len(arquivos), 'arquivos')
