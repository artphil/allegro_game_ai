

class finder:
	def __init__(self, file_name):
		try:
			self.file = open(file_name, 'r').read()
		except:
			print("File {} not found.".format(file_name))
			return
			
		self.words = self.to_list(self.file)
		self.keys = self.get_keys('ALLEGRO_KEY_')
		

	def to_list(self, txt):
		simbols = []
		valids = [' ','_']
		for a in txt:
			if not a.isalnum() and a not in valids:
				if a not in simbols:
					simbols.append(a)
		
		new_txt = txt
		
		for s in simbols:
			new_txt = new_txt.replace(s, ' ')

		return [w for w in new_txt.split(' ') if len(w) > 0 ]

	def search(self, name):
		word_list = []

		for word in self.words:
			if len(word) < len(name):
				continue

			for i in range(len(word)):
				if len(word)-i < len(name):
					break

				if name[0] == word[i]:
					found = False

					for j in range(len(name)):
						if name[j] == word[i+j]:
							found = True
						else:
							found = False
							break

					if found and word not in word_list:
						word_list.append(word)
						break

		return word_list

	def get_keys(self, prefix):
		w_list = self.search(prefix)
		k_list = []
		
		for w in w_list:
			k_list.append(w.replace(prefix, ''))
		
		return [k.lower() for k in k_list if len(k) > 0 ]
