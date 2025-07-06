# Projektkonzept: Urbane Hitzeinseln in Münster

## Zielsetzung
Untersuchung und Visualisierung urbaner Hitzeinseln in Münster durch Vergleich von Frühjahrs- und Sommerdaten der letzten fünf Jahre. Der Fokus liegt auf:
- Temperaturverteilung nach Flächennutzung
- Einfluss von Vegetation und Bodenfeuchte
- Darstellung relativer sowie absoluter Unterschiede

---

## Datengrundlage

**Satellitendaten:** Landsat 8 / 9 (OLI + TIRS)

**Zeitraum:**
- Frühling: 5–8 cloudfreie Szenen aus März–Mai (letzte 5 Jahre)
- Sommer: 5–8 cloudfreie Szenen aus Juni–August (letzte 5 Jahre)

**Benötigte Kanäle:**
- TIRS: Band 10 (ggf. Band 11 für Emissivität)
- OLI: Band 4 (Rot), Band 5 (NIR)

---

## Verarbeitungsschritte

### 1. Berechnung der Landoberflächentemperatur (LST)
- Umrechnung von DN-Werten → Radianz → Temperatur mittels Planck-Gleichung
- Optional: Emissivitätskorrektur (z. B. NDVI-basiert)

### 2. Berechnung von NDVI und NDMI
- NDVI = (NIR − Red) / (NIR + Red)
- NDMI = (NIR − SWIR) / (NIR + SWIR) *(sofern SWIR vorhanden)*

### 3. Bildung saisonaler Mittelwerte
- Sommer-Mittelwertkarte (aus 5–8 Sommer-Szenen)
- Frühling-Mittelwertkarte (aus 5–8 Frühlings-Szenen)

---

## Normalisierung

Ziel: Vergleichbarkeit der Temperaturverteilungen zwischen den Jahreszeiten

**Methode:** Z-Transformation (oder alternativ Min-Max-Normalisierung)

Formel:
$T_{norm} = (T - \mu_{Saison}) / \sigma_{Saison}$


Ergebnis: Darstellung relativer Hitze innerhalb der jeweiligen Szene → Frühling und Sommer werden vergleichbar.

---

## Analyse und Visualisierung

### A. Klassifizierung von Flächentypen

**Zielklassen:**
- Infrastruktur (versiegelt)
- Wald
- Gewässer
- Wiese/Feld

**Methodik:** Schwellenwertbasierte oder überwachte Klassifikation

---

### B. Temperaturvergleich pro Klasse

**Darstellung:**
- Boxplots (Whiskerplots) je Klasse:
  - Relative Temperatur im Frühling
  - Relative Temperatur im Sommer

Ziel: Erkennung der typischen thermischen Eigenschaften jeder Landbedeckung.

---

### C. Korrelationen mit Vegetation und Feuchte

**Visualisierung:** Scatterplots (inkl. Regressionslinie)

**Beziehungen:**
- NDVI vs. LST (Frühling und Sommer separat)
- NDMI vs. LST (sofern NDMI verfügbar)

Ziel: Quantitative Analyse der Kühlwirkung von Vegetation und Bodenfeuchte.

---

### D. Differenzbild (Sommer − Frühling)

**Berechnung:**
$\Delta T = T_{Sommer} − T_{Frühling}$


**Ziel:** Darstellung des tatsächlichen Temperaturanstiegs im Stadtgebiet

**Darstellung:** Karte mit abgestufter Farblegende

---

## Zusammenfassende Darstellung (Posteraufbau-Vorschlag)

1. Übersichtskarte Münster mit Klassifikation der Flächentypen
2. Temperaturkarten (Frühling und Sommer, normalisiert)
3. Differenzkarte ΔT
4. Whiskerplots pro Klasse (Frühling/Sommer)
5. Scatterplots zu NDVI/LST und NDMI/LST
6. Fazit und Handlungsempfehlungen (z. B. gezielte Begrünung, Entsiegelung)
