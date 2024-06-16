import asyncio
import os
import random
import shutil
from tkinter import *
from tkinter.ttk import *
from urllib.parse import urlparse

import PIL.Image
import mouse
import requests
from PIL import ImageTk, Image

all_urls = {
	'https://i.pinimg.com/originals/d6/8c/33/d68c333aae7879d9e08bf3e412e7ce84.jpg',
	'https://img10.reactor.cc/pics/post/Holo-Spice-and-Wolf-Anime-фэндомы-7825655.jpeg',
	'https://www.tapeciarnia.pl/tapety/normalne/107681_spice_and_wolf_uszy.jpg',
	'https://cs6.pikabu.ru/post_img/big/2015/01/25/9/1422194619_1364259629.jpeg',
	'https://sun9-75.userapi.com/impf/c845019/v845019287/28f4f/uRV7px4UZ-k.jpg?size=282x346&quality=96&sign=4fe7092d1d8885428340ff76a42256f1&type=album',
	'https://sun9-77.userapi.com/impf/c845218/v845218287/2627a/ZNedqyYjGlU.jpg?size=724x1024&quality=96&sign=e9fffdde2e854968260ab63d3595fba3&type=album',
	'https://sun9-73.userapi.com/impf/c840321/v840321287/7421d/nAba22ov0vc.jpg?size=807x554&quality=96&sign=9e1e39bb060f4981c8f5ffe89c3a6092&type=album',
	'http://img0.joyreactor.com/pics/post/full/anime-wolf-and-spice-Horo-Spice-and-Wolf-1647712.jpeg',
	'https://sun9-27.userapi.com/impf/c824603/v824603287/10f902/0DW5S5KDw30.jpg?size=1280x800&quality=96&sign=85e2ecbd17b204a8ca88654bf38a40b8&type=album',
	'https://img10.reactor.cc/pics/post/картинки-про-аниме-волчица-и-пряности-Inumimi-Animal-Ears-%28Anime%29-5910.jpeg',
	'https://img10.reactor.cc/pics/post/Holo-Spice-and-Wolf-Anime-фэндомы-7825652.jpeg',
	'https://cs14.pikabu.ru/post_img/big/2022/09/19/10/1663607366154358723.jpg',
	'https://img10.reactor.cc/pics/post/full/Anime-фэндомы-Spice-and-Wolf-Holo-7394005.jpeg',
	'https://klike.net/uploads/posts/2022-09/1662554302_g-57.jpg',
	'https://adonius.club/uploads/posts/2022-02/1645381459_47-adonius-club-p-kholo-art-71.png',
	'https://adonius.club/uploads/posts/2022-05/1653188691_51-adonius-club-p-volchitsa-i-pryanosti-oboi-krasivie-65.jpg',
	'https://2ch.hk/aa/src/61965/14940040610791.png',
	'https://external-preview.redd.it/rziJpJCA6Yi3aecegpUPPcocpb658ajBnquv08V89nk.jpg?auto=webp&v=enabled&s=bb6ff4d1c3dcdb8c8dbecd6b40d0edb92e074ec1',
	'https://avatars.mds.yandex.net/i?id=7023ba095ce352f8a3fee3c90e9b4ffe0fcf2d7c-8173266-images-thumbs&n=13',
	'https://media.kg-portal.ru/anime/o/ookamitokoushinryou2/fanart/ookamitokoushinryou2_5.jpg',
	'https://avatars.mds.yandex.net/i?id=b5a4495ae09ca32663c608bcded6cee9432f7f0c-8285735-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/i?id=1e7d3de0c08a3bf0ed5095b7ab106a624bc8c61a-7612999-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/i?id=c5660ba9ddc3ca40a7d97437c5ba1f80cca5b03b-7663734-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/i?id=fe87e2fe22ba1650858b46d1d7fef12070779aba-8496495-images-thumbs&n=13',
	'https://kartinkin.net/uploads/posts/2021-07/thumbs/1625751454_20-kartinkin-com-p-volchitsa-i-pryanosti-arti-art-krasivo-22.jpg',
	'https://c.wallhere.com/photos/d5/8e/anime_Holo_snow_Spice_and_Wolf_anime_girls_Okamimimi_fantasy_art-254177.jpg!d',
	'https://avatars.mds.yandex.net/i?id=2b29f00117a329655b10b77e1af08e471a86ff90-8438956-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/i?id=247923aa9b90df9e73618e98b4e0a4576bae6a8b-4297394-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/i?id=4cf93a701a573c37925619a74b02d259936a1364-8252971-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/i?id=cd01054477476a158945df958a106377283a03ba-5364864-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/i?id=b7611a647fa35bb68ae8d3212b828b90c0f571b2-7554427-images-thumbs&n=13',
	'https://avatars.dzeninfra.ru/get-zen_doc/4162493/pub_63fda095021a136684e8e0a8_63fde05ba4e0cd40a05a5a2c/scale_1200',
	'https://avatars.mds.yandex.net/i?id=26265f0cf22f4a044da688708830815f9921a849-8497168-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/i?id=247923aa9b90df9e73618e98b4e0a4576bae6a8b-4297394-images-thumbs&n=13',
	'https://i.imgur.com/DlKYylU.jpg',
	'https://img10.reactor.cc/pics/post/Spice-and-Wolf-Inumimi-Animal-Ears-%28Anime%29-Anime-4214978.jpeg',
	'https://avatars.mds.yandex.net/i?id=b5a4495ae09ca32663c608bcded6cee9432f7f0c-8285735-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/i?id=2b29f00117a329655b10b77e1af08e471a86ff90-8438956-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/i?id=7023ba095ce352f8a3fee3c90e9b4ffe0fcf2d7c-8173266-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/i?id=b7611a647fa35bb68ae8d3212b828b90c0f571b2-7554427-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/i?id=c5660ba9ddc3ca40a7d97437c5ba1f80cca5b03b-7663734-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/i?id=c0e960b0ed636b6a23350896c0f3094669fa204a-8219873-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/i?id=7bae24896b97f12b6b5c52a29cfdb9ccb221a37e-7756253-images-thumbs&n=13',
	'https://mobimg.b-cdn.net/v3/fetch/a5/a5c6df71b3761e6e6e5206dc2a1720bf.jpeg',
	'https://i.pinimg.com/originals/67/b8/6d/67b86dd8b4bee5ecd79ea21494dba56e.jpg',
	'https://avatars.mds.yandex.net/i?id=d317ac24bc75a9d23c549701607034171c852a56-8219219-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/i?id=26265f0cf22f4a044da688708830815f9921a849-8497168-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/i?id=174363208ad00055a1275ca3dc13e6f647e403c0-8553021-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/i?id=e57897a6e106316f790c1e6f5c8c5063d4884616-5584275-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/i?id=476f6ce9c24624d177c37972ca5ea7214cff5c9f-6390812-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/i?id=4c68b6a5e165a9e42afb01859f12d380628be4d2-8548977-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/i?id=27a068260055deb70e63512df0856d676b1e0a1b-8210080-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/i?id=bfd8c6c264cbc613cd5541ac804c289cd74eaac7-8497316-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/i?id=8f3e00b4ca663732919645a6e2df630b15df21a2-8228018-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/i?id=b6014f934aee035edba75c101e8d7d2c4877e304-5234779-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/i?id=5e577e986705b85ca1f1dd528b0a1855fc877352-3831708-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/get-pdb/472427/67a0887b-e6d6-45ef-8810-1312b51dbe22/s1200?webp=false',
	'https://avatars.mds.yandex.net/i?id=a51d09647cb6d8ec1d032082a41bccce6afb623d-8348537-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/i?id=9e4203fe9d854690d2c63c1f785eae6931114603-7942262-images-thumbs&n=13',
	'https://avatars.mds.yandex.net/i?id=bfbf18620832a0fea7ca515d2a77726fdae6fd77-8177077-images-thumbs&n=13',
	'https://img2.reactor.cc/pics/comment/full/anime-gif-Anime-Spice-and-Wolf-Inumimi-1048296.jpeg',
	'https://img2.reactor.cc/pics/comment/anime-gif-Anime-Spice-and-Wolf-Inumimi-1048303.jpeg',
	'https://i.mycdn.me/i?r=AzEPZsRbOZEKgBhR0XGMT1Rk6lWDaAyLkv_iJBmdSs45c6aKTM5SRkZCeTgDn6uOyic',
	'https://media.kg-portal.ru/anime/o/ookamitokoushinryou/fanart/ookamitokoushinryou_197.jpg',
	'https://cdn.ananasposter.ru/image/cache/catalog/poster/mult/83/11018-1000x830.jpg',
	'https://printstorm.ru/wp-content/uploads/2021/03/2b5d49d3afb27f3a8b59b7075c58ba17bbcf3296-1.jpg',
	'https://i.pinimg.com/originals/de/d0/15/ded0154fd233aade69e6a038cafbf5e6.jpg',
	'https://printstorm.ru/wp-content/uploads/2021/03/1583668787-54282d730439d400ad2be79e4d903aed-1.jpeg',
	'https://www.tapeciarnia.pl/tapety/normalne/107681_spice_and_wolf_uszy.jpg',
	'https://mobimg.b-cdn.net/v3/fetch/cb/cbd14fcdb64b33f3cd40d62627b7c130.jpeg',
	'https://mobimg.b-cdn.net/v3/fetch/a5/a5c6df71b3761e6e6e5206dc2a1720bf.jpeg',
	'https://cdn.ananasposter.ru/image/cache/catalog/poster/anime/78/31507-1000x830.jpg',
	'https://www.posterior.ru/products/detailed/31/spice-and-wolf-03.jpg',
	'https://media.kg-portal.ru/anime/o/ookamitokoushinryou/fanart/ookamitokoushinryou_241.jpg',
	'https://media.kg-portal.ru/anime/o/ookamitokoushinryou2/production/ookamitokoushinryou2_11.jpg',
	'https://printstorm.ru/wp-content/uploads/2021/03/ERd-CirXUAAs8hw-1.jpg',
	'https://media.kg-portal.ru/anime/o/ookamitokoushinryou2/fanart/ookamitokoushinryou2_6.jpg',
	'https://media.kg-portal.ru/anime/o/ookamitokoushinryou/fanart/ookamitokoushinryou_90.jpg',
	'https://pibig.info/uploads/posts/2022-06/1654365939_30-pibig-info-p-kholo-mudraya-art-krasivo-36.jpg',
	'https://i.artfile.ru/1920x1200_942926_[www.ArtFile.ru].jpg',
	'https://steamuserimages-a.akamaihd.net/ugc/31859743147664921/65D20A0BB79E76C6E1F2A613AFA2A144EB1F57E2/?imw=512&amp;imh=288&amp;ima=fit&amp;impolicy=Letterbox&amp;imcolor=%23000000&amp;letterbox=true',
	'https://mobimg.b-cdn.net/v3/fetch/b1/b1b6f8a6108235b6d3527a64d17102be.jpeg',
	'https://preview.redd.it/5myfwmig25i21.png?auto=webp&s=50e335d4625514615f10b6b26f96dfe9864741ea',
	'https://preview.redd.it/hw8dtot8vpe61.jpg?auto=webp&v=enabled&s=6cf6e0e24c462cb8aee8b5c8f0dd1fae570a3b26',
	'https://c4.wallpaperflare.com/wallpaper/372/399/641/horo-spice-and-wolf-holo-wolf-and-spice-spice-and-wolf-wolf-ears-wallpaper-preview.jpg',
	'https://c4.wallpaperflare.com/wallpaper/784/148/43/holo-spice-and-wolf-anime-girls-anime-wallpaper-preview.jpg',
	'https://img4.goodfon.ru/original/1920x1080/c/b0/kholo-volchitsa-i-prianosti-oboi-na-rabochii-stol-spice-an-8.jpg',
	'https://c4.wallpaperflare.com/wallpaper/197/551/811/anime-anime-girls-spice-and-wolf-holo-wallpaper-preview.jpg',
	'https://preview.redd.it/lbxm2imycn661.jpg?auto=webp&s=bd9b74d801b2548dcbdea542018fb2bb60d7afc4',
	'https://preview.redd.it/9lf6669ucxk61.jpg?auto=webp&s=5157c92ef8d9e96dd165da07f863e7bb700c153b',
	'https://preview.redd.it/x1zb3kbmvdo71.jpg?auto=webp&v=enabled&s=42f830da07b8b067dd8ff3ab3dc0fed42555fc3a',
	'https://preview.redd.it/t5jccxj56w851.jpg?auto=webp&s=9b512083823b5ea0dd08acc77d68a3e290464b12',
	'https://sun9-84.userapi.com/impg/c855024/v855024502/1a5656/Owcsb-M3EAc.jpg?size=1920x1920&quality=96&sign=6405e5f362cec85085ba6f937e485465&c_uniq_tag=Vx9XMyui5_Rbh20crADvbPBQin1oQTkR4lz1OFi_iOY&type=album'
}
all_urls = list(all_urls)

backupUrls = {}  # Just for debug url printing
downloaded_images = []


def is_valid(url):
	parsed = urlparse(url)
	return bool(parsed.netloc) and bool(parsed.scheme)


for i, url in enumerate(all_urls):
	if not is_valid(url):
		print("Url is broken :", i, url)


def download_image(url, name):
	res = requests.get(url, stream=True)
	
	try:
		if res.status_code != 200:
			return False
		
		with open(name, 'wb') as f:
			shutil.copyfileobj(res.raw, f)
		
		downloaded_images.append(name)
		backupUrls[name] = url
		return True
	except Exception as e:
		pass
	return False


async def create_window(img_numb):
	global cur_img, fun_level, images_folder
	
	try:
		img = Image.open(downloaded_images[img_numb])
		
		height = img.height
		width = img.width
		change = False
		
		# Resize if image doesn't fit
		while height > screen_height // 1.5 or width > screen_width // 1.5:
			height //= 1.5
			width //= 1.5
			height, width = int(height), int(width)
			change = True
		if change:
			img = img.resize((width, height))
		
		new_window_x = random.randint(0, screen_width - width)
		new_window_y = random.randint(0, screen_height - height - 70)
		
		new_window = Toplevel(root)
		new_window.geometry(f"{width}x{height}+{new_window_x}+{new_window_y}")
		new_window.title(downloaded_images[img_numb])
		new_window.resizable(False, False)
		new_window.protocol("WM_DELETE_WINDOW", lambda: ...)
		
		img = ImageTk.PhotoImage(img)
		panel = Label(new_window, image=img)
		panel.image = img
		panel.pack()
		
		if fun_level >= 1:
			new_window.attributes('-topmost', 1)
			if fun_level >= 2:
				mouse.move((new_window_x + width // 2), (new_window_y + height // 2))
		root.update()
	except PIL.UnidentifiedImageError:
		print("Image is broken:", downloaded_images[img_numb], backupUrls[downloaded_images[img_numb]])
		downloaded_images.pop(img_numb)
		backupUrls.pop(img_numb)


async def await_first_image():
	while len(downloaded_images) == 0:
		await asyncio.sleep(0.01)
	await asyncio.sleep(3)


async def create_timer():
	global delay, max_images
	await await_first_image()
	
	curr_image = 0
	tot_images = 0
	while True:
		if curr_image >= len(downloaded_images):
			tot_images += curr_image - 1
			if tot_images > max_images:
				root.destroy()
				return
			curr_image = 0
			random.shuffle(downloaded_images)
		await create_window(curr_image)
		await asyncio.sleep(delay / 1000)
		curr_image += 1


cycles = 0


async def download_new():
	global cycles, delay, max_download_retries
	
	while cycles <= max_download_retries:
		url_num = 0
		random.shuffle(all_urls)
		while url_num < len(all_urls):
			url = all_urls[url_num]
			try:
				successfully_downloaded = download_image(url, f"{images_folder}Holo{len(downloaded_images)}.png")
				if not successfully_downloaded:
					print("Download failed", all_urls[url_num])
					raise Exception
				
				all_urls.pop(url_num)
				await create_window(-1)  # Create window with last downloaded image
			except Exception as e:
				url_num += 1
			
			await asyncio.sleep(delay / 1000)
		cycles += 1
	
	print("No more download attempts")


# Controls
# To change urls which you want to download / spam - change all_urls at the top of a code

delay = 20  # Milliseconds delay between images
images_folder = "Best_images/"  # Empty to spam in a program folder
max_images = 500  # After how many images would it stop, set to -1 for real fun
max_download_retries = 3
fun_level = 0
# At 0 it just spawns images. At 1 it will make them always topmost, even higher than task manager - harder to disable.
# At 2 it will move your mouse to images, so you can't move the mouse properly
if images_folder != "" and not os.path.exists(images_folder):
	os.mkdir(f"./{images_folder}")

root = Tk()
root.geometry("1x1+2000+2000")

screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()

print("There are:", len(all_urls), "images")


async def start():
	global max_images
	if max_images == -1:
		max_images = float("inf")
	await asyncio.gather(create_timer(), download_new())


root.protocol("WM_DELETE_WINDOW", lambda: ...)
asyncio.run(start())
