## **MVP‑Reflexion – Woche 09–10**
### **1. Konnte das MVP (V1.0) wie geplant umgesetzt werden?**
Das MVP konnte teilweise erfolgreich umgesetzt werden. Die Grundfunktionen wie das Erstellen von Einträgen und das Anzeigen der Aufgaben im Listenformat funktionieren stabil. Die grundlegende Struktur der App ist lauffähig und entspricht den Anforderungen an ein MVP.

### **2. Was konnte nicht umgesetzt werden und warum?**
Während der Entwicklung traten mehrere technische Probleme auf. Die Login‑Funktion konnte zunächst nicht umgesetzt werden, da das SWITCH‑Drive‑Passwort versehentlich im GitHub‑Repository sichtbar war. Dadurch mussten wir das Passwort zurücksetzen und die Datei secrets.toml mehrfach korrigieren, da sie sich im falschen Ordner befand.
Zusätzlich zeigte die Streamlit‑App lokal zeitweise keine Website an, weshalb wir mehrere Codeabschnitte überarbeiten mussten.
Nach mehreren Anpassungen konnten alle Fehler erfolgreich behoben werden. 

### **3. Müssen wir die Roadmap anpassen?**
Ja, wir haben die Roadmap in Woche 11 angepasst. Dabei haben wir festgestellt, dass einige wichtige Informationen fehlten und die Prioritäten für die kommenden Wochen klarer definiert werden mussten. Die Anpassung stellt sicher, dass wir realistisch planen und die wichtigsten Funktionen zuerst umsetzen.

### **4. Welche Unterstützung brauchen wir?**
Wir benötigen gezielte Unterstützung bei folgenden Punkten:
- Login‑System: Umgang mit Session State, Passwort‑Handling und korrekter Einsatz von secrets.toml.
- Fehleranalyse: Unterstützung bei der Diagnose von Streamlit‑Fehlern, wenn die App lokal nicht angezeigt wird.
- Strukturierung: Bestätigung, ob unsere Datenstruktur für zukünftige Funktionen (Wochenansicht, Punktesystem) sinnvoll aufgebaut ist.

Support erhalten wir aktuell von Ka Men, möchten aber in den kommenden Übungsstunden weitere technische Fragen klären.