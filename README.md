# Wa-Tor Simulation

## Description

Ce projet est une simulation de l'écosystème de Wa-Tor, une simulation basée sur une grille où des poissons et des requins interagissent dans un environnement clos. Les poissons se déplacent et se reproduisent, tandis que les requins chassent les poissons et se reproduisent également, tout en devant éviter la famine. L'objectif est de modéliser et d'observer l'évolution de cet écosystème dans le temps.

La simulation utilise la bibliothèque `pygame` pour l'affichage graphique et présente en temps réel le nombre de poissons, de requins et l'évolution de la simulation à travers le temps.

## Fonctionnalités

- **Mouvement et reproduction** des poissons et des requins
- Les requins **mangent les poissons** pour éviter la famine
- Les poissons et les requins se **reproduisent** après un certain temps
- Simulation graphique en temps réel avec `pygame`
- Affichage des statistiques telles que :
  - Le temps écoulé
  - Le nombre de poissons
  - Le nombre de requins
  - Le nombre de "chronons" écoulés (cycles de simulation)
  - Le temps final lorsque l'extinction d'une espèce survient

## Dépendances

- Python 3.7+
- pygame