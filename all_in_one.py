import requests
from bs4 import BeautifulSoup
import os
import time
tic = time.perf_counter()
toremove = []
alphabet=[]
links = []
total_poem_text = []
poem_txt = []
text = []
test = 'yabba dabba do i see you'
extensions = []
poems = {'Titles': [],'Authors': [],'Links': [],'Texts': []}
duds = []
error_links = {
  'linknum': [], 
  'link': [] 
}

def clear_terminal():
  os.system('cls')

def poem_stz_folder(linknum):
  if not os.path.isdir(("C:\\Users\\merpd\\Desktop\\poem\\apoems\\%s" % linknum)) :
      os.makedirs(("C:\\Users\\merpd\\Desktop\\poem\\apoems\\%s" % linknum))

def fill_alphabet():
  for x in range(65,91):
    alphabet.append(chr(x))

def clear_links_txt():
  with open('Links.txt','w'):
    pass

def find_indices(list_to_check, item_to_find):
    indices = []
    for idx, value in enumerate(list_to_check):
        if value == item_to_find:
            indices.append(idx)
    return indices
# just stole this   very useful

def fill_extensions():
  for x in range(0,26):
    extensions.append(('indexpage/by_title/start_char/%s' % alphabet[x]))

def write_links_txt(extension):
    r = requests.get(('https://100.best-poems.net/%s' % extension)) #https://100.best-poems.net/top-100-best-poems.html 
    soup = BeautifulSoup(r.content, 'html.parser')
    for link in soup.find_all('a'):
        if link.get('href')[0] == '/':
            address = link.get('href')
            if len(address) > 1 and address[-4::] == 'html':
                address = '%s\n' % address
                with open('Links.txt', 'a') as f:
                  f.write(address)
                '''links.append('https://100.best-poems.net'+address) 
                poems['Links'].append(address)'''

def get_all_addresses():
  for x in range(len(extensions)):
    print((extensions[x])[-1::])
    write_links_txt(extensions[x])

def get_titles(linknum):
    print(linknum)
    r = requests.get(('https://100.best-poems.net/%s' % str((poems['Links'])[linknum])))
    soup = BeautifulSoup(r.content, 'html.parser')
    for line in soup.find_all('h1'): #title
        string_line = str(line)
        front_cut = string_line.split(">")[1]
        back_cut = front_cut.split("<")[0]
        titles = back_cut
        titles = titles.strip()
        poems['Titles'].append(titles) 

def get_authors(linknum):
    x = 0 
    #print('linknum',linknum,(poems['Links'])[linknum])
    r = requests.get(('https://100.best-poems.net/%s' % str((poems['Links'])[linknum])))
    soup = BeautifulSoup(r.content, 'html.parser')
    for line in soup.find_all('h2'): #author  
      if '\"author\"' in str(line):
          x = 1
          string_line = str(line)
          front_cut = string_line.split(">by ")[1]
          back_cut = front_cut.split("<")[0]
          authors = back_cut
          authors = authors.strip()
          #print(linknum, authors)
          with open('Authors.txt', 'a') as f:
            f.write(authors)
            f.write('\n')
          #poems['Authors'].append(authors)
    if x != 0:
      for line in soup.find_all('h1'): #put in same function for faster 
        string_line = str(line)
        front_cut = string_line.split(">")[1]
        back_cut = front_cut.split("<")[0]
        titles = back_cut
        titles = titles.strip()
        with open('Titles.txt', 'a') as f:
          f.write(titles)
          f.write('\n')
        #poems['Titles'].append(titles)
    else:
      with open('duds.txt','a') as f:
        f.write(linknum)
        f.write('\n')
      duds.append(linknum)      

def get_texts(linknum):
  poem_txt.clear()
  text.clear()
  r = requests.get(str('https://100.best-poems.net'+poems['Links'][linknum]))
  soup = BeautifulSoup(r.content, 'html.parser')
  txt_name = ('poems/'+'%s.txt' % linknum)
  for line in soup.find_all('p'):
    if str(line)[1] == 'p':
      text.append(line)
  poem_stz_folder(linknum)
  for x in range(len(text)):
    if (str(text[x])[:8:]) == "<p><br/>" or 'div' in str(text[x]):
      #print(x)
      end = x
      
      for b in range(end): #each paragraph        
        no_br = str(text[b])
        no_br = str(no_br)
        '''basictext = str(text[b])
        fp_cut = basictext.split('<p>')[1]
        bp_cut = fp_cut.split('</p>')[0]
        no_br = bp_cut.replace('<br/>','')'''
        #print(no_br)
        #print('checking----------------------------')
        if '<' in str(no_br):
          open_tags = find_indices(no_br,'<')
          close_tags = find_indices(no_br,'>')
          for x in range(len(open_tags)):
            opn_tag = find_indices(no_br,'<')
            clse_tag = find_indices(no_br,'>')
            if len(opn_tag) > 0:
              tag_to_replace = no_br[opn_tag[0]:(clse_tag[0]+1)]
              no_br = no_br.replace(tag_to_replace,'')
              if 'href' not in no_br and 'www.' not in no_br and 'Share this Poem:' not in no_br and '&lt;' not in no_br:
                poem_txt.append(no_br)
              '''with open(('apoems\\%s\\%s.txt' % (linknum, b)), 'w') as f:
                f.write(no_br)'''

          '''
          for tags in range(len(open_tags)):
            diff = int(close_tags[tags])-int(open_tags[tags])
          my_test = 'yabba dabba do i see you <center> </center>'
          for x in range(len(open_tags)):
            no_tags = no_br[open_tags[x]:close_tags[x]]
            print('linknum:',linknum)
            print(x,open_tags[x],close_tags[x])
            print(no_br[open_tags[x]:close_tags[x]])
            print(no_br[413:421])
            no_br = no_br.replace(str(no_tags),'')
          print('----------------------\n') some checking statements, not needed
          '''
          \
        '''if b == 0:
          with open(txt_name, 'w') as l:
            pass
          f = open(txt_name, 'a') #'poems.txt'
          f.write(poems['Titles'][linknum])
          f.write('\n\n')
          f.write(poems['Authors'][linknum])
          f.write('\n\n')
          f.write(no_br) #.replace('\\n',' LINEBR ')
          f.write('\n')
          f.close
          total_poem_text.clear()
          total_poem_text.append(no_br)
        else:
          with open(txt_name, 'a') as f: #'poems.txt'
            f.write(no_br) #.replace('\n',' LINEBR ')
        total_poem_text.append(no_br) #flag
    poems['Texts'].append(total_poem_text)'''
  with open('presentableallpoems.txt', 'a') as f: 
    str_poem_txt = str(poem_txt).replace('\\n',' ')
    str_poem_txt = str_poem_txt.replace('<br/>',' ')
    str_poem_txt = str_poem_txt.replace('</p>',' ')
    f.write(str_poem_txt)
    f.write('\n')
  
def print_poem_from_txt(linknum):
  os.system('clear')
  with open('%s.txt' % linknum) as f:
    print(f.read())
    
def print_poem(x):
    print('Poem',(x+1),'\n','Title:',poems['Titles'][x],'\n','Author:',poems['Authors'][x],'\n','Found at:',poems['Links'][x])

def populate_links(): 
  with open('Links.txt') as links:
    for link in links:
      poems['Links'].append(link.split('\n')[0])

def populate_auth_titles():
  with open('Authors.txt') as authors:
    for author in authors:
      poems['Authors'].append(author.split('\n')[0])
  '''with open('Links.txt') as links:
    for link in links:
      poems['Links'].append(link.split('\n')[0])'''
  with open('Titles.txt') as titles:
    for title in titles:
      poems['Titles'].append(title.split('\n')[0])

def clear_poems_txt():
  with open('poems.txt', 'w'):
    pass


def actual_poem_texts(): 
  with open('allpoems.txt','w'):
    pass
  with open('presentableallpoems.txt','w'):
    pass
  #get_texts(19)
  for x in range(len(poems['Links'])):
    get_texts(x)
    #pass
def fill_dicts_from_links():
  with open('Titles.txt','w'):
    pass
  with open('Authors.txt', 'w'):
    pass
  for x in range(len(poems['Links'])) : #len(poems['Links'])
      #get_titles(x) faster when titles and authors is in one fx
      try:
        get_authors(x) 
      except:
        with open('errors.txt','a') as f:
          f.write(str(x))
          f.write('\n')
        error_links['linknum'].append(x)
        error_links['link'].append((poems['Links'])[x])

def writing():
  with open('Links.txt', 'w') as f:
      for x in range(len(poems['Links'])):
          f.write(poems['Links'][x])
          f.write('\n')
  with open('Titles.txt', 'w') as f:
      for x in range(len(poems['Titles'])):
          f.write(poems['Titles'][x])
          f.write('\n')
  with open('Authors.txt', 'w') as f:
      for x in range(len(poems['Authors'])):
          f.write(poems['Authors'][x])
          f.write('\n')
#dont need if txt files are already written

def look_up():   
  if lookup.isdigit() == True:
    print_poem(int(lookup)-1)
    x = int(lookup)
    see_text = input('Want to see the poem?\nY/N\n')
    if see_text.lower() == 'y':
      print_poem_from_txt(x-1)
  else:
    if poems['Authors'].count(lookup) > 1: #multiple poems same author
        repetitions = find_indices((poems['Authors']),lookup)
        for repeats in repetitions:
            x = repeats
            print_poem(x)
          
        return True
    else:
        for name in poems['Authors']:
            if lookup in name:
                print('check')
                x = poems['Authors'].index(lookup)
                print_poem(x) #'https://
                see_text = input('Want to see the poem?\nY/N\n')
                if see_text.lower() == 'y':
                  print_poem_from_txt(x-1)
        for title in poems['Titles']:
            if lookup in title:
                x = poems['Titles'].index(lookup)
                print_poem(x)   
                see_text = input('Want to see the poem?\nY/N\n')
                if see_text.lower() == 'y':
                  print_poem_from_txt(x-1)
                  
        return False    

def clean_links():
  with open("Links.txt", "r") as fp:
    lines = fp.readlines()

  with open("Links.txt", "w") as fp:                          
    for x in range(len(error_links['link'])):
        toremove.append(str((error_links['link'])[x]))    
    for line in lines:
      if line.strip("\n") not in toremove:
          fp.write(line)

clear_terminal()
#fill_alphabet()
#clear_links_txt()
#fill_extensions()
#get_all_addresses()
populate_links() #only need this for getting links in dict if Links.txt is written
populate_auth_titles()
clear_poems_txt()
#fill_dicts_from_links()
#clean_links()
#print(duds)
actual_poem_texts()
print(len(poems['Authors']),len(poems['Titles']))

'''with open('presentableallpoems.txt') as f:
  print(f.read())
'''
lookup = input('Looking for something?\nCapitalization matters!\n')

while look_up() == True: #when multiple poems by same author
    lookup = input('Which one?\n')
    print()
