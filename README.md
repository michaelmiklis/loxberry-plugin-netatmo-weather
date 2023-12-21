# Loxberry Plugin: Netatmo Weather

Dieses Plugin ermöglicht es Daten von einer Netatmo Wetterstation an die Miniserver über UDP zu senden. Der Vorteil ist, dass die normale Netatmo ReST API verwendet wird und lediglich der Benutzername und das Passwort benötigt werden und kein Developer-Account.

<img src="https://raw.githubusercontent.com/michaelmiklis/loxberry-plugin-netatmo-weather/assets/Netatmo-Weather-1024x631.png" alt="Netatmo Weather Plugin"/>

Das Plugin unterstützt auch mehrere Wetterstationen innerhalb eines Netatmo Accounts. Jeder Messwert (Sensor) wird als einzelnes UDP Paket an den Miniserver gesendet. Das Paket hat immer folgende Aufbau:

[Stationsname].[Modulname].[Sensorname]=[Wert]

zum Beispiel:
Zuhause.Wohnzimmer.Temperature=30
Zuhause.Wohnzimmer.Humidity=56

## Beispiel

Die UDP Pakete werden wie im Screenshot ersichtlich einzeln an den Miniserver gesendet:

<img src="https://raw.githubusercontent.com/michaelmiklis/loxberry-plugin-netatmo-weather/assets/UDP-Monitor-1024x308.png" alt="UDP-Monitor" width="960" height="289"/>

Hierzu kann ein virtueller UDP Befehl angelegt werden mit folgender Befehlserkennung:
<img src="https://raw.githubusercontent.com/michaelmiklis/loxberry-plugin-netatmo-weather/assets/UDP-Befehl-1024x743.png" alt="UDP-Befehl" width="640" height="464" />

## Batterie-Level

Der Batterie-Level wird ab Version 0.13 in [Stationsname].[Modulname].battery_percent als Prozentwert übermittelt. 

## WiFi Signalstärke

Die WiFi-Signalstärke wird ab Version 0.10. in [Stationsname].[Modulname].wifi_status übermittelt. Es handelt sich um einen Zahlenwert, welchen ihr mit folgender Tabelle umwandeln könnt:

- 86 = bad
- 71 = average
- 56 = good

## Funk Signalstärke

Die Funk-Signalstärke zwischen der Basisstation und den Modulen wird ab Version 0.6. in [Stationsname].[Modulname].rf_status übermittelt. Es handelt sich um einen Zahlenwert, welchen ihr mit folgender Tabelle umwandeln könnt:

- 90 = low
- 80 = medium
- 70 = high
- 60 = full

## Temperatur- und Luftdrucktrend

Der Temperatur- und Luftdrucktrend wird bis zur Version 0.15 als String mit den Werten "up", "down" und "stable" übermittelt. Um die Auswertung am Loxone Miniserver zu vereinfachen, wird ab der Version 
0.16 der Trend als Zahlenwert übermittelt ([Stationsname].[Modulname].pressure_trend und [Stationsname].[Modulname].temp_trend). Es handelt sich um einen Zahlenwert, welchen ihr mit folgender Tabelle umwandeln könnt:

- -1 = down
- 0 = stable
- 1 = up

## Offline Erkennung (reachable)

Ab der Version 0.18 wird übermittelt ob die Station aus Sicht der Netatmo API erreichbar ist ([Stationsname].[Modulname].reachabl)
Es handelt sich um einen Zahlenwert, welchen ihr mit folgender Tabelle umwandeln könnt:

- 0 = nicht erreichbar (offline)
- 1 = erreichbar (online)

## Local Time / Lokale Zeitzone

Durch diese Option kann gesteuert werden, ob alle Datums- und Zeitangaben in UTC (Option aus) oder in der jeweiligen lokalen Zeitzone an den Miniserver übertragen werden.

## E-Mail Benachrichtigung durch Netatmo deaktivieren

Da das Plugin jedesmal eine neue / frische Anmeldung bei Netatmo durchführt, führ dies jedes mal zu einer E-Mail benachrichtigung. Diese kann im Netatmo Konto in den Einstellungen deaktiviert werden:

<img src="https://raw.githubusercontent.com/michaelmiklis/loxberry-plugin-netatmo-weather/assets/MyAccount.png">
<img src="https://raw.githubusercontent.com/michaelmiklis/loxberry-plugin-netatmo-weather/assets/NewConnection.png">

## Troubleshooting

### Step 1: Check Logfile in Loxberry WebUI

Navigate to "Log Manager" -> "More Logfiles" -> "Netatmo Weather (Plugin Log)" and check the logfile for error messages.

### Step 2: Execute plugin locally using SSH connection

Open an SSH connection to your Loxberry and execute the following command:

`python3 /opt/loxberry/data/plugins/netatmo-weather/netatmo.py --logfile=$LBPLOG/netatmo-weather/netatmo-weather.log --configfile=$LBPCONFIG/netatmo-weather/netatmo.cfg`

If python specific errors occur, they will be displayed in the console.

To see the raw JSON data returned from the Netatmo getstationdata() API execute the following command:

`python3 /opt/loxberry/data/plugins/netatmo-weather/netatmo.py --logfile=$LBPLOG/netatmo-weather/netatmo-weather.log --configfile=$LBPCONFIG/netatmo-weather/netatmo.cfg --apibody` 

If you experience any problems with please continue with section "Feedback and Discussion".

## ## Feedback & Discussion

This plugin will be improved over time and feedback is appreciated. Therefore I created a thread in the LoxForum:

<a href="https://www.loxforum.com/forum/projektforen/loxberry/plugins/86373-loxberry-netatmo-weather-plugin">https://www.loxforum.com/forum/projektforen/loxberry/plugins/86373-loxberry-netatmo-weather-plugin</a>

## Change-Log
- 2023-12-17 Release 2.0.8 - PRE-RELEASE: added support for unnamed base-stations and modules
- 2023-03-30 Release 2.0.7 - RELEASE: implemented persistent session cookies to eliminate login email messages
- 2022-05-22 Release 2.0.6 - fixed authentication change from Netatmo, added --apibody commandline argument
- 2021-12-29 Release 2.0.5 - added next-hop URL after authentication for stability issues, if account has also Netatmo Welcome Cameras enabled
- 2020-12-27 Release 2.0.4 - Various bug fixings, beginning of general.json, implemented logging to log file
- 2020-12-24 Release 2.0.3 - Fixed bug causing configuration-loss during upgrade, implemented auto-update
- 2020-12-23 Release 2.0.2 - Changed from station_name to home_name because of API change by Netatmo
- 2019-12-30 Release 2.0.1 - Support für Loxberry 2.0 (getestet auf 2.0.0.4)
- 2019-05-08 Release 0.18  - Offline Module und Stationen werden ignoriert
- 2019-03-08 Release 0.17  - Netatmo Login Prozess angepasst
- 2018-06-24 Release 0.16  - temp_trend und pressure_trend als Zahlenwert
- 2018-06-20 Release 0.15  - Netatmo API URL angepasst
- 2018-02-18 Release 0.14  - Datums- und Zeitwerte können nun über einen Parameter in die lokale Zeitzone konvertiert werden.
- 2018-02-12 Release 0.13  - Datum- und Zeitwerte werden nun korrekt übertragen, Update auf Loxberry 1.0, Batteriestatus in Prozent
- 2018-01-28 Release 0.12  - Anpassungen für Loxberry 0.3, neue Verzeichnisstruktur, Datumsformat auf Nullzeit-Delta angepasst
- 2017-06-14 Release 0.10  - wifi_status hinzugefügt, Umlaute-Problem   behoben, JSON in Webfrontend entfernt, User-Agent eingebaut
- 2017-04-01 Release 0.9   - weitere Timestamp Werte angepasst - Bugfixing 
- 2017-03-30 Release 0.8   - time_utc, date_min_temp,    date_max_temp in normalem Timestamp Format dd.mm.YYYY HH:MM:SS Format
- 2017-03-25 Release 0.7   - Bug-Fix für dynamische Pfade in Webfrontend CGI und    Umbennenung nach Netatmo-Weather 
- 2017-03-12 Release 0.6   - dynamische    Pfade im Script und Cron-Job, Config-Datei bleibt beim Update  erhalten, wechsel auf GetStationsData API
- 2017-03-02 Fix in cron-job    if-Abfrage
- 2017-03-01 Anpassung UDP - für jeden Sensor wird ein    eigenes UDP Paket gesendet 
- 2017-03-01  Anpassung cron-job und    netatmo.py auf statische Pfade da Variablen nicht korrekt aufgelöst    werden (Workaround)
- 2017-02-26  Erstellung PlugIn v 0.1

## Known-Issues

- none

## Sensor-Werte

| Base Station                                        |
| --------------------------------------------------- |
| {Station Name}.{Base Name}.wifi_status=20           |
| {Station Name}.{Base Name}.reachable=1,  0          |
| {Station Name}.{Base Name}.date_min_temp=287640458  |
| {Station Name}.{Base Name}.Temperature=22.3         |
| {Station Name}.{Base Name}.time_utc=287699122       |
| {Station Name}.{Base Name}.Noise=38                 |
| {Station Name}.{Base Name}.AbsolutePressure=995.1   |
| {Station Name}.{Base Name}.CO2=848                  |
| {Station Name}.{Base Name}.temp_trend=-1, 0, 1      |
| {Station Name}.{Base Name}.pressure_trend=-1, 0, 1  |
| {Station Name}.{Base Name}.max_temp=22.6            |
| {Station Name}.{Base Name}.date_max_temp=287694609  |
| {Station Name}.{Base Name}.min_temp=20.8            |
| {Station Name}.{Base Name}.Pressure=1018.5          |
| {Station Name}.{Base Name}.Humidity=55              |

| Outdoor Unit                                        |
| --------------------------------------------------- |
| {Station Name}.{Module Name}.battery_percent=27     |
| {Station Name}.{Module Name}.rf_status=65           |
| {Station Name}.{Module Name}.reachable=1,  0        |
| {Station Name}.{Module Name}.Temperature=-1.4       |
| {Station Name}.{Module Name}.date_min_temp=287354902|
| {Station Name}.{Module Name}.time_utc=287354902     |
| {Station Name}.{Module Name}.max_temp=-1.4          |
| {Station Name}.{Module Name}.date_max_temp=287354902|
| {Station Name}.{Module Name}.min_temp=-1.4          |
| {Station Name}.{Module Name}.Humidity=85            |

| Indoor Unit                                         |
| --------------------------------------------------- |
| {Station Name}.{Module Name}.battery_percent=3      |
| {Station Name}.{Module Name}.rf_status=64           |
| {Station Name}.{Module Name}.reachable=1,  0        |
| {Station Name}.{Module Name}.Temperature=20.6       |
| {Station Name}.{Module Name}.CO2=1040               |
| {Station Name}.{Module Name}.date_min_temp=279849458|
| {Station Name}.{Module Name}.time_utc=279850739     |
| {Station Name}.{Module Name}.max_temp=20.8          |
| {Station Name}.{Module Name}.date_max_temp=279846125|
| {Station Name}.{Module Name}.min_temp=20.6          |
| {Station Name}.{Module Name}.Humidity=57            |

| Rain Gauge                                          |
| --------------------------------------------------- |  
| {Station Name}.{Module Name}.battery_percent=72     |
| {Station Name}.{Module Name}.rf_status=57           |
| {Station Name}.{Module Name}.reachable=1,  0        |
| {Station Name}.{Module Name}.sum_rain_1=0           |
| {Station Name}.{Module Name}.sum_rain_24=1.616      |
| {Station Name}.{Module Name}.Rain=0                 |
| {Station Name}.{Module Name}.time_utc=287699120     |

| Wind Gauge                                              |
| ------------------------------------------------------- |
| {Station Name}.{Module Name}battery_percent=66          |
| {Station Name}.{Module Name}rf_status=67                |
| {Station Name}.{Module Name}.reachable=1,  0            |
| {Station Name}.{Module Name}WindHistoric=[]             |
| {Station Name}.{Module Name}GustStrength=6              |
| {Station Name}.{Module Name}max_wind_angle=185          |
| {Station Name}.{Module Name}time_utc=287699120          |
| {Station Name}.{Module Name}max_wind_str=26             |
| {Station Name}.{Module Name}max_temp=0                  |
| {Station Name}.{Module Name}WindAngle=225               |
| {Station Name}.{Module Name}WindStrength=3              |
| {Station Name}.{Module Name}date_max_temp=287622255     |
| {Station Name}.{Module Name}date_min_temp=287622255     |
| {Station Name}.{Module Name}date_max_wind_str=287685251 |
| {Station Name}.{Module Name}GustAngle=190               |
| {Station Name}.{Module Name}min_temp=0                  |
