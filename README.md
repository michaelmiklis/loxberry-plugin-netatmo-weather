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

## Batterie-Level

Der Batterie-Level wird ab Version 0.6. in [Stationsname].[Modulname].battery_vp übermittelt. Es handelt sich um einen Zahlenwert, welchen ihr mit folgender Tabelle umwandeln könnt:

**Innenmodul:**
- 6000 = max  
- 5640 = full  
- 5280 = high  
- 4920 = medium  
- 4560 = low 
- < 4560  = very low

**Außenmodul und Regenmesser:**
- 6000 = max
- 5500 = full
- 5000 = high
- 4500 = medium
- 4000 = low
- < 4000 = very low

**Windmesser:**
- 6000 = max
- 5590 = full
- 5180 = high
- 4770 = medium
- 4360 = low
- < 4360 = very low

## Funk Signalstärke
Die Funk-Signalstärke zwischen der Basisstation und den Modulen wird ab Version 0.6. in [Stationsname].[Modulname].rf_status übermittelt. Es handelt sich um einen Zahlenwert, welchen ihr mit folgender Tabelle umwandeln könnt:

- 90 = low
- 80 = medium
- 70 = high
- 60 = full

## Feedback und Diskussion
Das PlugIn wird von mir noch weiterentwickelt und ich freue mich über Anregungen und Feedback. Hierzu habe ich im Loxforum einen Thread eröffnet:

<a href="https://www.loxforum.com/forum/projektforen/loxberry/plugins/86373-loxberry-netatmo-weather-plugin">https://www.loxforum.com/forum/projektforen/loxberry/plugins/86373-loxberry-netatmo-weather-plugin</a>

## Change-Log
- 2017-04-01 Release 0.9 - weitere Timestamp Werte angepasst - Bugfixing 
- 2017-03-30 Release 0.8 - time_utc, date_min_temp,    date_max_temp in normalem Timestamp Format dd.mm.YYYY HH:MM:SS Format   
- 2017-03-25 Release 0.7 - Bug-Fix für dynamische Pfade in Webfrontend CGI und    Umbennenung nach Netatmo-Weather 
- 2017-03-12 Release 0.6 - dynamische    Pfade im Script und Cron-Job, Config-Datei bleibt beim Update    erhalten, wechsel auf GetStationsData API 
- 2017-03-02 Fix in cron-job    if-Abfrage 
- 2017-03-01 Anpassung UDP - für jeden Sensor wird ein    eigenes UDP Paket gesendet 
- 2017-03-01  Anpassung cron-job und    netatmo.py auf statische Pfade da Variablen nicht korrekt aufgelöst    werden (Workaround) 
- 2017-02-26  Erstellung PlugIn v 0.1

## Known-Issues
- Logging erfolgt nicht in die Log-Datei