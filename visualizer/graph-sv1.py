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

# Przechowywanie najwyższych wartości z każdego miesiąca
yearly_summary = {}

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

    # Aktualizacja najwyższych wartości dla każdego miesiąca
    max_values = month_data[['stone', 'silver', 'gold', 'wyp', 'likes', 'comments']].max()
    yearly_summary[(year, month)] = max_values

# Generowanie wykresu podsumowującego dla całego roku
for year in df['date'].dt.year.unique():
    # Dane dla konkretnego roku
    year_data = {k: v for k, v in yearly_summary.items() if k[0] == year}

    if year_data:  # Jeśli są dane dla roku
        plt.figure(figsize=(14, 8))

        # Przesunięcie słupków dla różnych kategorii
        bar_width = 0.12
        opacity = 0.7
        num_categories = 6  # Liczba kategorii (stone, silver, gold, wyp, likes, comments)
        total_bar_width = bar_width * num_categories  # Całkowita szerokość wykresu słupkowego

        months = list(range(1, 13))  # Miesiące od 1 do 12
        x = range(len(months))  # Użyj indeksów jako współrzędnych x

        # Przygotowanie wartości, ustawienie 0 jeśli brakuje danych dla miesiąca
        stone_values = [year_data.get((year, month), {'stone': 0})['stone'] for month in months]
        silver_values = [year_data.get((year, month), {'silver': 0})['silver'] for month in months]
        gold_values = [year_data.get((year, month), {'gold': 0})['gold'] for month in months]
        wyp_values = [year_data.get((year, month), {'wyp': 0})['wyp'] for month in months]
        likes_values = [year_data.get((year, month), {'likes': 0})['likes'] for month in months]
        comments_values = [year_data.get((year, month), {'comments': 0})['comments'] for month in months]

        # Tworzenie wykresów słupkowych obok siebie
        plt.bar([i - total_bar_width / 2 + bar_width * 0 for i in x], stone_values, color='brown', width=bar_width, alpha=opacity, label='Stone')
        plt.bar([i - total_bar_width / 2 + bar_width * 1 for i in x], silver_values, color='silver', width=bar_width, alpha=opacity, label='Silver')
        plt.bar([i - total_bar_width / 2 + bar_width * 2 for i in x], gold_values, color='gold', width=bar_width, alpha=opacity, label='Gold')
        plt.bar([i - total_bar_width / 2 + bar_width * 3 for i in x], wyp_values, color='blue', width=bar_width, alpha=opacity, label='Wyp')
        plt.bar([i - total_bar_width / 2 + bar_width * 4 for i in x], likes_values, color='green', width=bar_width, alpha=opacity, label='Likes')
        plt.bar([i - total_bar_width / 2 + bar_width * 5 for i in x], comments_values, color='red', width=bar_width, alpha=opacity, label='Comments')

        # Dodawanie tytułu i etykiet
        plt.title(f'Roczne podsumowanie dla {year}')
        plt.xlabel('Miesiąc')
        plt.ylabel('Najwyższe wartości')

        # Ustawienia osi X
        plt.xticks(x, [f'{year}-{month:02d}' for month in months], rotation=45)

        # Dodanie legendy
        plt.legend()

        # Dodanie siatki dla lepszej czytelności
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)

        plt.tight_layout()

        # Zapisz wykres do pliku PNG
        filename = os.path.join(output_dir, f'{year}.png')
        plt.savefig(filename, dpi=300)
        plt.close()  # Zamknij wykres po zapisaniu, aby uniknąć nakładania się wykresów
