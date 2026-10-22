import os, requests, feedparser, asyncio, edge_tts
from PIL import Image, ImageDraw, ImageFont
import textwrap

def buscar_noticia():
    feeds = [
        "https://www.listindiario.com/rss/portada",
        "https://hoy.com.do/feed/",
        "https://www.diariolibre.com/rss/portada.xml"
    ]
    for url in feeds:
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                return feed.entries[0].title, feed.entries[0].summary[:250]
        except:
            pass
    return "Última hora en República Dominicana", "Atención, esto acaba de pasar y nadie te lo está contando."

async def crear_voz(texto):
    os.makedirs("output", exist_ok=True)
    communicate = edge_tts.Communicate(
        texto, "es-DO-JoseManuelNeural",
        rate="-10%", pitch="-20Hz"
    )
    await communicate.save("output/voz.mp3")
    print("Voz creada con exito")

def crear_video(titulo):
    img = Image.new('RGB', (1080, 1920), color=(5,5,5))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 65)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 35)
    except:
        font = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Decor
    draw.rectangle([0,0,1080,25], fill=(0,255,136))
    draw.text((40, 70), "NOTICIAS RD • EN VIVO", font=font_small, fill=(0,255,136))
    
    lineas = textwrap.wrap(titulo, width=22)
    y = 550
    for linea in lineas:
        draw.text((82, y+4), linea.upper(), font=font, fill=(30,30,30))
        draw.text((80, y), linea.upper(), font=font, fill=(255,255,255))
        y += 110
    
    draw.text((80, 1600), "SIGUEME PARA MAS", font=font_small, fill=(150,150,150))
    
    img.save("output/fondo.jpg")
    os.system('ffmpeg -y -loop 1 -i output/fondo.jpg -i output/voz.mp3 -c:v libx264 -c:a aac -shortest -vf "scale=1080:1920,format=yuv420p" -t 30 output/video_final.mp4')
    print("Video creado")

if __name__ == "__main__":
    titulo, resumen = buscar_noticia()
    texto_voz = f"{titulo}. {resumen}. Sígueme para más noticias virales de República Dominicana."
    print(f"Noticia: {titulo}")
    asyncio.run(crear_voz(texto_voz))
    crear_video(titulo)
