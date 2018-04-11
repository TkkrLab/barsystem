---
title: "barsystem"
date: 2018-04-11
publishdate: 2018-04-11
categories: [projects]
draft: false
keywords: [project,barsystem]
aliases: [/projects/barsystem/]
---

TkkrLab heeft een eigen systeem voor het afrekenen van eten en drinken wat in de space verkrijgbaar is. 
Dit is een webapplicatie geschreven in Python met het Django-framework.
Members kunnen met hun iButton afrekenen, en bezoekers kunnen hun naam selecteren.

<!--more-->

Het systeem bestaat uit twee componenten, barsystem en barlink. Barsystem draait op een server en is de core die de transacties bijhoudt en de webinterface toont. Barlink is een speciaal programma dat op de computer draait met de interface, en koppelt met behulp van een WebSocket de interface aan de iButton-lezer ([TkkrLab/bar-ibutton-reader](https://github.com/TkkrLab/bar-ibutton-reader))

# Resources
 - [Source code](https://github.com/TkkrLab/barsystem)

# Contributors
 - jawsper
