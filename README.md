# 🎮 Projekt końcowy - Programowanie Grafiki 3D

**Interaktywna aplikacja 3D z OpenGL w Pythonie**

## 📋 Opis projektu

Projekt realizuje wszystkie wymagania projektu końcowego z przedmiotu Programowanie Grafiki 3D:

### ✅ Zrealizowane funkcjonalności

1. **Inicjalizacja środowiska graficznego** - GLFW + OpenGL
2. **Scena 3D** - wielość obiektów (kostki, sfery, podłoże, chmury)
3. **Interakcja użytkownika**:
   - Sterowanie kamerą (WASD, mysz, spacja, shift)
   - Kontrola wysokości chmur (strzałki góra/dół)
   - Zmiana parametrów oświetlenia (klawisze 1-4)
   - Przemieszczanie źródła światła (I/J/K/L/U/O)
4. **Oświetlenie Phonga**:
   - Ambient (światło otaczające)
   - Diffuse (światło rozproszone)
   - Specular (światło lustrzane)
5. **Tekstury** - wszystkie obiekty mają nałożone tekstury
6. **Dodatkowe efekty**:
   - Blending dla chmur (przezroczystość)
   - Billboard rendering dla chmur
   - Proceduralne generowanie tekstur

## 🎯 Wymagania techniczne

### Wymagane biblioteki

```bash
pip install PyOpenGL PyOpenGL_accelerate glfw Pillow numpy
```

### Minimalne wymagania systemowe

- Python 3.7+
- Obsługa OpenGL 2.1+
- Karta graficzna z akceleracją 3D
- System operacyjny: Windows/Linux/macOS

## 🚀 Instalacja i uruchomienie

### 1. Klonowanie/pobranie projektu

```bash
cd /home/swistek/Grafika3D/Projekt/projectGFK
```

### 2. Instalacja zależności

```bash
pip install -r requirements.txt
```

lub ręcznie:

```bash
pip install PyOpenGL PyOpenGL_accelerate glfw Pillow numpy
```

### 3. Uruchomienie aplikacji

```bash
python main.py
```

## 🎮 Sterowanie

### 🎥 Kamera

| Klawisz | Akcja |
|---------|-------|
| **W** | Kamera do przodu |
| **S** | Kamera do tyłu |
| **A** | Kamera w lewo |
| **D** | Kamera w prawo |
| **SPACJA** | Kamera w górę |
| **SHIFT** | Kamera w dół |
| **MYSZ** | Obracanie kamery (rozglądanie się) |

### ☁️ Chmury

| Klawisz | Akcja |
|---------|-------|
| **↑** (Strzałka góra) | Podnieś wszystkie chmury |
| **↓** (Strzałka dół) | Obniż wszystkie chmury |

### 💡 Oświetlenie (Model Phonga)

| Klawisz | Akcja |
|---------|-------|
| **1** | Zwiększ oświetlenie Ambient (otaczające) |
| **2** | Zmniejsz oświetlenie Ambient |
| **3** | Zwiększ oświetlenie Diffuse (rozproszone) |
| **4** | Zmniejsz oświetlenie Diffuse |

### 🔦 Pozycja źródła światła

| Klawisz | Akcja |
|---------|-------|
| **I** | Przesuń światło do przodu |
| **K** | Przesuń światło do tyłu |
| **J** | Przesuń światło w lewo |
| **L** | Przesuń światło w prawo |
| **U** | Przesuń światło w górę |
| **O** | Przesuń światło w dół |

### 🚪 Inne

| Klawisz | Akcja |
|---------|-------|
| **ESC** | Wyjście z programu |

## 📐 Struktura sceny

### Obiekty w scenie:

1. **Podłoże** - duża płaszczyzna z teksturą trawy (50x50 jednostek)
2. **Kostki (5 sztuk)** - rozmieszczone w różnych lokalizacjach, z czerwoną teksturą
3. **Sfery (4 sztuki)** - niebieskie kule rozmieszczone wokół sceny
4. **Chmury (5 sztuk)** - białe, przezroczyste billboardy na różnych wysokościach
5. **Źródło światła** - wizualizowane jako żółta sfera

### Parametry oświetlenia:

- **Ambient**: Światło otaczające (domyślnie: 0.3)
- **Diffuse**: Światło rozproszone (domyślnie: 1.0)
- **Specular**: Światło lustrzane (domyślnie: 1.0)
- **Shininess**: Połysk materiału (50.0)

## 🎨 Tekstury

Wszystkie tekstury są generowane proceduralnie w kodzie:

- **Trawa** - zielona tekstura z szumem dla realizmu
- **Chmury** - białe z gradientem alpha dla miękkości
- **Kostki** - czerwona tekstura (cegła)
- **Sfery** - niebieska tekstura

## 🔧 Szczegóły techniczne

### Użyte technologie:

- **OpenGL** - klasyczny pipeline z fixed function
- **GLFW** - zarządzanie oknem i inputem
- **PyOpenGL** - bindingi Python dla OpenGL
- **NumPy** - operacje matematyczne na wektorach/macierzach
- **Pillow (PIL)** - obsługa tekstur

### Implementacja modelu Phonga:

```python
# Komponenty:
- Ambient:  I_a = k_a * L_a
- Diffuse:  I_d = k_d * (N · L) * L_d
- Specular: I_s = k_s * (R · V)^n * L_s

# Gdzie:
- k_a, k_d, k_s - współczynniki materiału
- L_a, L_d, L_s - intensywności światła
- N - wektor normalny
- L - wektor do źródła światła
- R - wektor odbicia
- V - wektor do obserwatora
- n - współczynnik połysku
```

### Funkcjonalności dodatkowe:

1. **Alpha Blending** - przezroczystość chmur
2. **Billboard Rendering** - chmury zawsze zwrócone do kamery
3. **Proceduralne tekstury** - generowane w czasie rzeczywistym
4. **Smooth Shading** - gładkie cieniowanie obiektów

## 📊 Spełnienie wymagań projektu

### Minimalne wymagania (3.0-3.5): ✅

- ✅ Poprawna kompilacja i uruchomienie
- ✅ Kilka obiektów 3D w scenie
- ✅ Interakcja użytkownika (kamera, obiekty, parametry)
- ✅ Tekstury na obiektach
- ✅ Oświetlenie Phonga (ambient + diffuse)

### Dodatkowe funkcjonalności:

- ✅ Specular lighting (pełny model Phonga)
- ✅ Blending (przezroczystość)
- ✅ Billboard rendering
- ✅ Tekstury proceduralne
- ✅ Wizualizacja źródła światła
- ✅ Intuicyjne sterowanie
- ✅ Informacje o parametrach w konsoli

## 🐛 Rozwiązywanie problemów

### Błąd: "No module named 'OpenGL'"

```bash
pip install PyOpenGL PyOpenGL_accelerate
```

### Błąd: "Failed to initialize GLFW"

Upewnij się, że masz zainstalowane sterowniki graficzne i biblioteki OpenGL:

**Ubuntu/Debian:**
```bash
sudo apt-get install freeglut3-dev
```

**Fedora:**
```bash
sudo dnf install freeglut-devel
```

### Niska wydajność

- Sprawdź czy używasz akceleracji sprzętowej
- Zaktualizuj sterowniki karty graficznej
- Zmniejsz liczbę obiektów w scenie (edytuj `draw_scene()`)

### Czarny ekran

- Sprawdź czy kamera jest w odpowiedniej pozycji (domyślnie: [0, 5, 15])
- Upewnij się, że obiekty są w zasięgu widzenia kamery

## 📝 Autor i licencja

**Projekt:** Programowanie Grafiki 3D - Projekt końcowy  
**Data:** 30 listopada 2025  
**Technologia:** Python + OpenGL + GLFW

---

## 🎓 Dokumentacja dodatkowa

### Struktura kodu:

```
main.py
├── Inicjalizacja (init_opengl, init_textures)
├── Tworzenie tekstur (create_*_texture)
├── Rysowanie obiektów (draw_*)
├── Obsługa inputu (key_callback, mouse_callback)
├── Rendering (render)
└── Główna pętla (main)
```

### Przydatne linki:

- [PyOpenGL Documentation](http://pyopengl.sourceforge.net/)
- [GLFW Documentation](https://www.glfw.org/documentation.html)
- [OpenGL Tutorial](https://learnopengl.com/)

---

**Powodzenia z testowaniem aplikacji! 🚀**
