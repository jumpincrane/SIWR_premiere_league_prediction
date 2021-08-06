# Sztuczna Inteligencja w Robotyce - football projekt

## Opis projektu
Program przewiduje wyniki meczów w angielskiej lidze Premiere League. Wykorzystuje sieć bayesowską, która korzysta z zależności takich jak:

* oddana liczba strzałów na bramkę
* strzelone gole w całym meczu drużynie przeciwnej
* wyliczona siła drużyny

Siła drużyny obliczana jest na podstawie wygranych gier i remisów w całym sezonie. Wygrana gra jako gość jest liczona za 5pkt., a remis za 2pkt.. Natomiast wygrana jako gospodarz za 3pkt., a remis za 1pkt..

Po stworzeniu sieci bayesowskiej, CPD są tworzone automatycznie za pomocą funkcji model.fit(data).
