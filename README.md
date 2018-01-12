# Loxberry Plugin: Netatmo Weather
Dieses Plugin ermöglicht es Daten von einer Netatmo Wetterstation an die Miniserver über UDP zu senden. Der Vorteil ist, dass die normale Netatmo ReST API verwendet wird und lediglich der Benutzername und das Passwort benötigt werden und kein Developer-Account.

Das Plugin unterstützt auch mehrere Wetterstationen innerhalb eines Netatmo Accounts. Jeder Messwert (Sensor) wird als einzelnes UDP Paket an den Miniserver gesendet. Das Paket hat immer folgende Aufbau:

[Stationsname].[Modulname].[Sensorname]=[Wert];

zum Beispiel:

Zuhause.Wohnzimmer.Temperature=30;Zuhause.Wohnzimmer.Humidity=56;

## Beispiel
Die UDP Pakete werden wie im Screenshot ersichtlich einzeln an den Miniserver gesendet:

<img src="http://www.loxberry.de/wp-content/uploads/UDP-Monitor-1024x308.png" alt="UDP-Monitor" width="960" height="289"/>

Hierzu kann ein virtueller UDP Befehl angelegt werden mit folgender Befehlserkennung:
<img class="alignnone wp-image-303 " src="http://www.loxberry.de/wp-content/uploads/UDP-Befehl-1024x743.png" alt="UDP-Befehl" width="640" height="464" />


## Feedback und Diskussion
Das PlugIn wird von mir noch weiterentwickelt und ich freue mich über Anregungen und Feedback. Hierzu habe ich im Loxforum einen Thread eröffnet:

<a href="https://www.loxforum.com/forum/projektforen/loxberry/plugins/86373-loxberry-netatmo-weather-plugin">https://www.loxforum.com/forum/projektforen/loxberry/plugins/86373-loxberry-netatmo-weather-plugin</a>

## Change-Log
- 2017-03-02 Fix in cron-job if-Abfrage 
- 2017-03-01 Anpassung UDP - für jeden Sensor wird ein eigenes UDP Paket gesendet 
- 2017-03-01  Anpassung cron-job und    netatmo.py auf statische Pfade da Variablen nicht korrekt aufgelöst    werden (Workaround) 
- 2017-02-26  Erstellung PlugIn v 0.1

## Known-Issues
- Logging erfolgt nicht in die Log-Datei