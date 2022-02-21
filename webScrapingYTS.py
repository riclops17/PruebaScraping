from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
baseUrl = 'https://yts.mx/'


movieLinks= []
#recorrer la cantidad deseada de paginas de yts
for x in range(1,12):
    r = requests.get((f'https://yts.mx/browse-movies?page={x}'))
    soup = BeautifulSoup(r.content,'lxml')
    movieList = soup.findAll('div', class_='browse-movie-wrap col-xs-10 col-sm-4 col-md-5 col-lg-4')
    #Obtencion de todos los enlaces de peliculas
    for item in movieList:
            link = item.find('a')['href']
            #print(link)
            movieLinks.append(link)

    print('cantidad de peliculas ',len(movieLinks))
movieCatalogue = []
#obtener toda la informacion de un contenido-------------------------------------------
#testLink ='https://yts.mx/movies/pirates-of-the-caribbean-at-worlds-end-2007'
testLink ='https://yts.mx/movies/jesus-1999'
for link in movieLinks:
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'lxml')
    #obtener nombre
    try:
     name = soup.find('h1',itemprop='name').text.strip()
    except:
     name = 'error'
    e = []
    #obtener genero y anio
    res = soup.find('div',id='mobile-movie-info')
    for j in res:
      find = res.find_all('h2')

    for i in find:
        e.append(i.text)

    #uso de expresiones regulares para year
    regex = re.compile('[^0-9]')
    year = regex.sub('', e[0])
    genre= e[1]

    #obtner likes
    likes = soup.find('span',id='movie-likes').text.strip()
    # obtener puntuacion de imdb
    imbdScore = soup.find('span', itemprop='ratingValue').text
    control = soup.find('span', itemprop='ratingValue')

    #obtener rating de audiencia y criticos
    rat = []
    try:
          rating = soup.find_all('div',class_='rating-row')
          # print(rating)
          #print('-------------------------------------')
          for k in rating:
            #print(k)
            rat.append(k.find('span'))
          #print('......................................')

          critics = rat[1].text
          if(rat[2] == control):
              rating = '-'
          else:
           rating = rat[2].text

    except:
           critics='-'
           rating ='-'



    #obtener los torrents dependiendo la calidad
    enlacesT = soup.find('p',class_='hidden-md hidden-lg')
    for enlace in enlacesT.findAll("a"):
          if (enlace.text[:3] == "720"):
             link720 = enlace["href"]
          if enlace.text[:4] == "1080":
             link1080 = enlace["href"]
    #obtener director
    try:
     director = soup.find('span',itemprop='name').text.strip()
    except:
           director = None

    #obtener sinopsis
    synopsis = soup.find('p',class_='hidden-sm hidden-md hidden-lg').text.strip()
    #print(synopsis)
    #obtener cantidad de comentarios
    cantComment = soup.find('span',id='comment-count').text
    movie={'name':name,
           'director':director,
          'year':year,
          'genre':genre,
          'likes':likes,
          'rating':rating,
          'critics':critics,
          'imbdScore':imbdScore,
          'Torrent720':link720,
          'Torrent1080':link1080,
          'cantComent':cantComment,
          'synopsis':synopsis
          }

    movieCatalogue.append(movie)
    print('saving: ', movie['name'])
# Guardar Infomacion
df = pd.DataFrame(movieCatalogue)
print(df.head(10))
df.to_csv('peliculas.csv',index=False)




