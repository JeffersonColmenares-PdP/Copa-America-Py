import json
import random
import itertools

with open('C:\\ProjectPDP\\Copa-America-Py\\copa-america.json', 'r', encoding='utf-8') as myJson:
    copa_america = json.load(myJson)

def marcador_aleatorio():
    return random.randint(0, 3)

def generar_marcadores(copa_america):
    equipos = copa_america['teams']
    marcadores = []

    # Combinaciones de partidos x grupo
    for equipo1, equipo2 in itertools.combinations(equipos, 2):
        if equipo1['group'] == equipo2['group']:
            goles1 = marcador_aleatorio()
            goles2 = marcador_aleatorio()

            marcadores.append({
                'team1': equipo1['name'],
                'team2': equipo2['name'],
                'score1': goles1,
                'score2': goles2
            })

            # Actualizar estadísticas
            equipo1['games_played'] += 1
            equipo2['games_played'] += 1

            equipo1['pro_goals'] += goles1
            equipo1['ag_goal'] += goles2

            equipo2['pro_goals'] += goles2
            equipo2['ag_goal'] += goles1

            if goles1 > goles2:
                equipo1['points'] += 3
            elif goles2 > goles1:
                equipo2['points'] += 3
            else:
                equipo1['points'] += 1
                equipo2['points'] += 1

    # Marcadores JSON
    with open('marcadores.json', 'w', encoding='utf-8') as myJson:
        json.dump(marcadores, myJson, ensure_ascii=False, indent=4)

    # Estadísticas actualizadas JSON
    with open('estadisticas.json', 'w', encoding='utf-8') as myJson:
        json.dump(equipos, myJson, ensure_ascii=False, indent=4)

def exportar_equipos_ganadores(copa_america):
    equipos = copa_america['teams']
    equipos_ganadores = {}

    for equipo in equipos:
        grupo = equipo['group']
        if grupo not in equipos_ganadores:
            equipos_ganadores[grupo] = []

        equipos_grupo = [e for e in equipos if e['group'] == grupo]# x grupo
        equipos_grupo.sort(key=lambda x: (x['points'], x['pro_goals'], -x['ag_goal']), reverse=True)# Orden >
        equipos_ganadores[grupo] = equipos_grupo[:2]

    with open('ganadores.json', 'w', encoding='utf-8') as myJson:
        json.dump(equipos_ganadores, myJson, ensure_ascii=False, indent=4)

generar_marcadores(copa_america)
exportar_equipos_ganadores(copa_america)