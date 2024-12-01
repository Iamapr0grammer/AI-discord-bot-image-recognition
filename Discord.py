import discord
import os
import time
import subprocess
from imageai.Detection import ObjectDetection

# Zmienna intencje przechowuje uprawnienia bota
intents = discord.Intents.default()
# Włączanie uprawnienia do czytania wiadomości
intents.message_content = True
# Tworzenie bota w zmiennej klienta i przekazanie mu uprawnień
client = discord.Client(intents=intents)

# Pełna ścieżka pliku
current_directory = os.path.dirname(__file__)

def detect_objects_on_road(input_image, output_image, model_path):
    if not os.path.isfile(input_image):
        raise FileNotFoundError(f"Input image {input_image} not found.")
    if not os.path.isfile(model_path):
        raise FileNotFoundError(f"Model file {model_path} not found.")

    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(model_path)
    detector.loadModel()

    detections = detector.detectObjectsFromImage(
        input_image=input_image,
        output_image_path=output_image,
        minimum_percentage_probability=30
    )

    return detections

def generate_description(detections):
    object_names = [detection["name"] for detection in detections]
    
    if not object_names:
        return "Nie wykryto żadnych obiektów na obrazku."
    
    object_counts = {name: object_names.count(name) for name in set(object_names)}

    description = "Na obrazku widzimy: "
    descriptions = []

    for obj, count in object_counts.items():
        if count == 1:
            descriptions.append(f"jednego {obj}")
        else:
            descriptions.append(f"{count} {obj}")

    description += ", ".join(descriptions) + "."

    return description

input_image = "Istanbul_Otoyol_2_Richtung_FSM_2.jpg"
output_image = "output_image.jpg"
model_path = "yolov3.pt"

nazwa_folderu = "Wiadomości"
obecny_rok = 2024

# ścieżka do folderu
folder_path = os.path.join(current_directory, nazwa_folderu)

# Sprawdź, czy folder już istnieje
if not os.path.exists(folder_path):
    # Jeśli folder nie istnieje, utwórz go
    os.makedirs(folder_path)
    print(f"Folder '{nazwa_folderu}' został utworzony w {folder_path}.")
else:
    print(f"Folder '{nazwa_folderu}' już istnieje w {folder_path}.")

file_path = os.path.join(current_directory, "token.txt")

token = "0"

with open(file_path, 'r') as file:
    token = file.read().strip()

file_path = os.path.join(current_directory, "admin.txt")

admin = "0"

with open(file_path, 'r') as file:
    admin = file.read().strip()

@client.event
async def on_ready():
    print(f'Zalogowaliśmy się jako {client.user}')

async def check(message):
    if message.attachments:
        for attachment in message.attachments:
            input_image = attachment.filename
            await attachment.save(input_image)
            input_image = attachment.filename

            try:
                detections = detect_objects_on_road(input_image, output_image, model_path)
                description = generate_description(detections)

                await message.channel.send(description)
                await message.channel.send(file=discord.File(output_image))
                await message.channel.send(f"Zapisano obraz w ./{output_image}")
            except Exception as e:
                await message.channel.send(f"Wystąpił błąd: {e}")
    else:
        await message.channel.send("Zapomniałeś załadować obraz :(")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(message.content)

    await check(message)

    if message.content == "$segregacja":
        await message.channel.send("Tryb Segregacji włączony! Jaki rodzaj odpadów posiadasz?")
    
    if message.content == "$plastik":
        await message.channel.send("Plastik należy wrzucić do żółtego kontenera")

    if message.content == "$givememe":
        await message.channel.send("I give you meme")
    
    if message.author.name == "ironfrankpl":
        await message.channel.send("Witaj! IronFrank! Miło Cię widzieć!")
    
    if str(message.author) == admin:
        if message.content == "$open warhammer":
            warhammer_path = r"D:\Program Files (x86)\Steam\steamapps\common\Total War WARHAMMER III\warhammer3.exe"
            await message.channel.send("Opening Warhammer")
            try:
                subprocess.Popen(warhammer_path)
                print(f"Pomyślnie otworzono program: {warhammer_path}")
            except Exception as e:
                print(f"Wystąpił błąd podczas otwierania programu: {e}")
        if message.content == "$Witaj Nowy rok!":
            await message.channel.send(f"Szczęśliwego nowego roku! {obecny_rok}")
    
    if message.content == "$Hello":
        await message.channel.send("Hi!")
    
    if message.content == "$Koty":
        await message.channel.send("Nie, psy są lepsze!")
    
    if message.content == "$Who is Jicks?":
        await message.channel.send("Jicks is a Playerground addict and a nerd!")
    
    if message.content == "$bla":
        for i in range(100):
            await message.channel.send("blablablablablablablablabla")
    
    if message.content == "$Niemampomysłu":
        await message.channel.send("To pomyśl coś szybko")

    nazwa_pliku = f"{message.author}.txt"
    file_path = os.path.join(current_directory, nazwa_folderu, nazwa_pliku)

    obecny_czas_unix = int(time.time())
    obecny_czas = time.strftime("dzień:%d miesiąc:%m rok:%Y _ godzina:%H minuta:%M sekunda:%S", time.localtime(obecny_czas_unix))
    czas_z_odstepem = f"   |   {obecny_czas}"

    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            text = f"{message.content}{czas_z_odstepem}\n"
            file.write(text)
    else:
        with open(file_path, 'a') as file:
            text = f"{message.content}{czas_z_odstepem}\n"
            file.write(text)

client.run(token)
