import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}

villages = {
    'a': ['Akse', 'Akurdi', 'Akurli', 'Ambivali', 'Andheri', 'Anik', 'Are', 'Asalpha'],
    'b': ['Badhavan', 'Bandivali', 'Bandra', 'Bapanale', 'Belapur', 'Bhandup', 'Boli', 'Borala', 'Borivali', 'Bramhanvada'],
    'c': ['Chakala', 'Chandivali', 'Charkop', 'Chembur', 'Chinchavali', 'Chincholi', 'Chinchwad', 'Chuing'],
    'd': ['Dahisar', 'Danda', 'Daravali', 'Darave', 'Dehugaon', 'Dehurod-Cantonment', 'Devanar', 'Dindoshi', 'Divale'],
    'e': ['Eksar', 'Erangal'],
    'g': ['Ghatkopar', 'Gorai', 'Goregaon', 'Gundavali', 'Gundavali Gundavali', 'Gundgaon'],
    'h': ['Hariyali'],
    'i': ['Ismaliya'],
    'j': ['Juhu'],
    'k': ['Kandivali', 'Kanheri', 'Kanjur', 'Karave', 'Khari', 'Kinhai', 'Kirol', 'Kiwale', 'Klarebad', 'Kolekalyan', 'Kondivita', 'Kopari', 'Kukashet', 'Kurar', 'Kurla'],
    'm': ['Madh', 'Magathane', 'Mahul', 'Majas', 'Malad', 'Malavani', 'Malinagar', 'Mamuradi', 'Manbudruk', 'Mandale', 'Mandaneshwar', 'Mandapeshwar', 'Mankhurd', 'Manori', 'Maravali', 'Marol', 'Maroshi', 'Marve', 'Mogara', 'Mohili', 'Mulgaon', 'Mulund'],
    'n': ['Nagathane', 'Nahur', 'Nanole', 'Nerul', 'Nigadi'],
    'o': ['Oshivara'],
    'p': ['pahadi goregaon', 'Parajapur', 'Parighakhar', 'Pasapoli', 'Pavai', 'Pi.ena.pahadieksar', 'Poisar'],
    'r': ['Rahatani/kalewadi', 'Ravet'],
    's': ['Sahar', 'Sai', 'Saki', 'Sanapada', 'Santakrujh', 'Sarsole', 'Shahabaj', 'Shimpavali', 'Shiravane', 'Sonkhar'],
    't': ['Tirandaj', 'Tulasi', 'Tungaona', 'Turbhe'],
    'v': ['Vadhavali', 'Vadhavan', 'Valnai', 'Varsova', 'Vikroli', 'Vileparle', 'Viththalanagar', 'Vyaravali']
}
