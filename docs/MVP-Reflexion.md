## **MVP‑Reflexion – Woche 09–10**
### **1. Konnte das MVP (V1.0) wie geplant umgesetzt werden?**
Das MVP konnte noch nicht vollständig umgesetzt werden. Wir haben in dieser Phase vor allem das Grundgerüst der App erstellt, die Navigation aufgebaut und die Login‑Seite vorbereitet. Die eigentlichen MVP‑Funktionen (Einträge erstellen, Abgabefrist, Aufgaben abhaken) wurden noch nicht implementiert.

### **2. Was konnte nicht umgesetzt werden und warum?**
Während der Entwicklung traten mehrere technische Probleme auf. Die Login‑Funktion konnte zunächst nicht umgesetzt werden, da das SWITCH‑Drive‑Passwort versehentlich im GitHub‑Repository sichtbar war. Dadurch mussten wir das Passwort zurücksetzen und die Datei secrets.toml mehrfach korrigieren, da sie sich im falschen Ordner befand.
Zusätzlich zeigte die Streamlit‑App lokal zeitweise keine Website an, weshalb wir mehrere Codeabschnitte überarbeiten mussten.
Nach mehreren Anpassungen konnten alle Fehler erfolgreich behoben werden. 

### **3. Müssen wir die Roadmap anpassen?**
Ja, wir haben die Roadmap angepasst. Die MVP‑Funktionen werden nun in Woche 11–12 umgesetzt, da wir in Woche 10 hauptsächlich technische Probleme lösen mussten. Die neue Planung ist realistischer und priorisiert die wichtigsten Funktionen.

### **4. Welche Unterstützung brauchen wir?**
Wir benötigen gezielte Unterstützung bei folgenden Punkten:
- Login‑System: Umgang mit Session State, Passwort‑Handling und korrekter Einsatz von secrets.toml.
- Fehleranalyse: Unterstützung bei der Diagnose von Streamlit‑Fehlern, wenn die App lokal nicht angezeigt wird.
- Strukturierung: Bestätigung, ob unsere Datenstruktur für zukünftige Funktionen (Wochenansicht, Punktesystem) sinnvoll aufgebaut ist.

Support erhalten wir aktuell von Ka Men, möchten aber in den kommenden Übungsstunden weitere technische Fragen klären.