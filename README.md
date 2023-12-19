# Jakwywioze_web_crawler
Web crawler for Jakwywioze.pl project

1) ### Wymagania:
- Pycharm
- Python 3.7.8
2) ### Biblioteki:
- urlopen (z urllib.request)
- re
- bs4
- requests
- pandas
- time
- os
- webbrowser
- random
- easyocr

3. ### Omówienie funkcji w potrzebnej kolejności ich wykonywania:
	1) **main.py**
- Na początku uruchamiamy main.py (funkcję get_points()), aby uzyskać podstawowe informacje o punktach.
	
    2) **photo_phone_page.py**
- **UWAGA!!!** Zmienić zmienną browser_path na własną - linijka 4.
- Później uruchamiamy photo_phone_page.py z funkcjami do odczytu pliku (read_file()), samego procesu pozyskiwania danych (open_urls_and_read_input()) i na koniec zapisująca te dane (save_new_points(new_data)).
	
    3) **get_cities.py**
- Następnie get_cities.py zapisze największe miasta w Polsce (funkcja biggest_cities_new_dataset()) oraz dokona potrzebnej poprawki przecinków na kropki w liczbach (funkcja change_coma_for_dot()).
	
    4) **get_waste_types.py**
- **UWAGA!!!** Zmienić zmienną browser_path na własną - linijka 6.
- Po kolei uruchamiamy funkcje:
	- go_through_websites_1() - ustalamy czy na znalezionej stronie jest informacja o typie odpadów lub czy trzeba ewentualnie stronę zmienić
	- change_website() - zamienia adres podanych stron na nowe
	- get_img() - funcja otwiera punkty, które mają informacje o typie odpadów na swojej stronie i czeka na input (jest to znak, że zmieniliśmy image.png z zaznaczonym fragmetem strony gdzie te informacje się znajdują), a następnie zapisuje rozpoznany z obrazu tekst
	- correct_common_mistakes() - poprawia on częste błędy takie jak "zuzyte" -> "zużyte" itd.
	- create_files_to_insert() - aktualizuje pliki DB_waste_types.txt i DB_point_waste.txt aby były zgodne z aktualnymi danymi

    5) **manipulate_data.py**
- Opcjonalnie można uruchomić delete_points(), gdy jakieś punkty np. już nie istnieją. UWAGA!!! Trzeba zmienić wtedy indeksy na własne od najwiekszego według linijek pliku test_dane.
- Funkcje w manipulate_data.py zamienią dane oznaczające ich brak na nulle (change_unknown_and_none_to_null()) oraz zapisze dane w formie gotowej do zainsertowania w bazie danych(save_new_points()).

