
goals =[]
for tr in table.findAll('tr'):
	if tr.findAll('a', href=True, text=teamLink[7:10]):
       goalz=tr.find_all("a", {'class' : 'highlight_text'}, re.compile(player))
       goals.append(goalz)
