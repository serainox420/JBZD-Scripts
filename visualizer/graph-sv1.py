import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

# Wczytaj dane z pliku JSON
with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Przetwórz dane do DataFrame
df = pd.DataFrame(data)

# Przetwórz daty
df['date'] = pd.to_datetime(df['date'])

# Wyodrębnij różne rodzaje monet
df['stone'] = df['coins'].apply(lambda x: x['stone'])
df['silver'] = df['coins'].apply(lambda x: x['silver'])
df['gold'] = df['coins'].apply(lambda x: x['gold'])
df['wyp'] = df['coins'].apply(lambda x: x['wyp'])

# Tworzenie folderu wyjściowego
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Grupowanie danych według roku i miesiąca
grouped = df.groupby([df['date'].dt.year, df['date'].dt.month])

# Przetwarzanie każdego roku i miesiąca
for (year, month), group in grouped:
    # Tworzenie folderu dla roku
    year_folder = os.path.join(output_dir, str(year))
    if not os.path.exists(year_folder):
        os.makedirs(year_folder)

    # Filtruj dane dla konkretnego miesiąca i roku
    month_data = group

    # Dynamiczne ustawienie szerokości wykresu w zależności od liczby dni
    num_days = (month_data['date'].dt.date.max() - month_data['date'].dt.date.min()).days + 1
    fig_width = max(14, num_days * 0.5)  # Minimalna szerokość 14, zwiększa się o 0.5 jednostki na każdy dzień

    # Ustawienia wykresu
    plt.figure(figsize=(fig_width, 8))

    # Konfiguracja wykresów słupkowych
    bar_width = 0.12  # Mniejsza grubość słupków
    opacity = 0.7

    # Daty w formacie numerycznym
    dates = mdates.date2num(month_data['date'].dt.date)

    # Przesunięcie słupków dla różnych kategorii
    offset = bar_width * 3  # Przesunięcie dla każdego zestawu słupków

    plt.bar(dates - 2 * offset, month_data['stone'], color='brown', width=bar_width, alpha=opacity, label='Stone')
    plt.bar(dates - offset, month_data['silver'], color='silver', width=bar_width, alpha=opacity, label='Silver')
    plt.bar(dates, month_data['gold'], color='gold', width=bar_width, alpha=opacity, label='Gold')
    plt.bar(dates + offset, month_data['wyp'], color='blue', width=bar_width, alpha=opacity, label='Wyp')
    plt.bar(dates + 2 * offset, month_data['likes'], color='green', width=bar_width, alpha=opacity, label='Likes')
    plt.bar(dates + 3 * offset, month_data['comments'], color='red', width=bar_width, alpha=opacity, label='Comments')

    # Dodawanie tytułu i etykiet
    plt.title(f'Wykres czasowy dla {year}-{month:02d}')
    plt.xlabel('Data')
    plt.ylabel('Liczba')

    # Ustawienia osi X dla równomiernych odstępów w zakresie od min_date do max_date
    plt.gca().set_xlim(month_data['date'].min(), month_data['date'].max())
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    # Dostosowanie częstotliwości etykiet na osi X
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

    # Dodanie legendy
    plt.legend()

    # Dodanie siatki dla lepszej czytelności
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Ustawienia wykresu dla lepszej czytelności
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Zapisz wykres do pliku PNG
    filename = os.path.join(year_folder, f'{year}-{month:02d}.png')
    plt.savefig(filename, dpi=300)
    plt.close()  # Zamknij wykres po zapisaniu, aby uniknąć nakładania się wykresów
