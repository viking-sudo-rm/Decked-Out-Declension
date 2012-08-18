from Tkinter import *
import re

#---------------
#
#	Latin Noun Decliner
#	declines most regular Latin nouns in the nominative, genitive, dative, accusative, and ablative
#	developed in less than two hours
#	the process is not totally historically accurate (the results are pretty much the same, but the process is a bit different)
#
#---------------

class Noun:

	def __init__(self,nom,gen,gender="m"):
		self.dict = {"nom":nom,"gen":gen,"gender":gender}
		self.paradigm = self.getdeclensionparadigm()
		self.stem = self.dict["gen"][:-self.paradigm.stemnumber]
		self.syllable = re.compile("[bcdfghklmnpqrstvxz]*[aeiou]+[bcdfghklmnpqrstvxz]*")
		self.consonantalending = re.compile("[bcdfghklmnpqrstvxz]{2}\Z")
	
	def getforms(self):
		forms = []
		endings = self.paradigm.getendings()
		if endings:
			for number in ("singular","plural"):
				for case in ("nom","gen","dat","acc","abl"):
					if number == "singular" and (case == "nom" or (case == "acc" and self.dict["gender"] == "n")): forms.append(self.dict["nom"])
					else: forms.append(self.stem + self.applyistem(endings[number][case]))
			return forms
		return None
	
	def getdeclensionparadigm(self):
		if self.dict["gen"].endswith("is"): return Paradigm(3,self.dict["gender"])
		elif self.dict["nom"].endswith("a") and self.dict["gen"].endswith("ae"): return Paradigm(1,self.dict["gender"])
		elif self.dict["gen"].endswith("us") and self.dict["nom"].endswith("us"): return Paradigm(4,self.dict["gender"])
		elif self.dict["gen"].endswith("ei") and self.dict["nom"].endswith("es"): return Paradigm(5,self.dict["gender"])
		elif self.dict["gen"].endswith("i"): return Paradigm(2,self.dict["gender"])
		return Paradigm(0,self.dict["gender"])
	
	def getnumberofsyllables(self,s):
		return len(self.syllable.findall(s))
	
	def endsintwoconsonants(self,s):
		return self.consonantalending.findall(s)
	
	def isistem(self):
		return self.paradigm.declension == 3 and (((self.dict["nom"].endswith("s") or self.dict["nom"].endswith("x")) and self.endsintwoconsonants(self.stem)) or ((self.dict["nom"].endswith("es") or self.dict["nom"].endswith("is")) and self.getnumberofsyllables(self.dict["nom"]) == self.getnumberofsyllables(self.dict["gen"])))
	
	def applyistem(self,ending):
		if self.isistem() and (ending.startswith("a") or ending.startswith("u")): ending = "i" + ending
		return ending
		
class Paradigm:

	def __init__(self,number,gender):
		self.declension = number
		self.gender = gender
		self.stemnumber = 2
		if number == 2:	self.stemnumber = 1
	
	def getendings(self):
		return self.applyneuterchanges(self.getnormalendings())

	def getnormalendings(self):
		n = self.declension
		if n == 1: return {"singular":{"nom":"a","gen":"ae","dat":"ae","acc":"am","abl":"a"},"plural":{"nom":"ae","gen":"arum","dat":"is","acc":"as","abl":"is"}}
		if n == 2: return {"singular":{"nom":"us","gen":"i","dat":"o","acc":"um","abl":"o"},"plural":{"nom":"i","gen":"orum","dat":"is","acc":"os","abl":"is"}}
		if n == 3: return {"singular":{"nom":"","gen":"is","dat":"i","acc":"em","abl":"e"},"plural":{"nom":"es","gen":"um","dat":"ibus","acc":"es","abl":"ibus"}}
		if n == 4: return {"singular":{"nom":"us","gen":"us","dat":"ui","acc":"um","abl":"u"},"plural":{"nom":"us","gen":"uum","dat":"ibus","acc":"us","abl":"ibus"}}
		if n == 5: return {"singular":{"nom":"es","gen":"ei","dat":"ei","acc":"em","abl":"e"},"plural":{"nom":"es","gen":"erum","dat":"ebus","acc":"es","abl":"ebus"}}
		else: return None
	
	def applyneuterchanges(self,endings):
		if self.gender == "n":
			if self.declension == 2:
				endings["singular"]["nom"] = "um"
				endings["plural"]["nom"] = "a"
				endings["plural"]["acc"] = "a"
			if self.declension == 3:
				endings["singular"]["acc"] = ""
				endings["plural"]["nom"] = "a"
				endings["plural"]["acc"] = "a"
			if self.declension == 4:
				endings["singular"]["nom"] = "u"
				endings["singular"]["gen"] = "us"
				endings["singular"]["dat"] = "u"
				endings["singular"]["acc"] = "u"
				endings["plural"]["nom"] = "ua"
				endings["plural"]["acc"] = "ua"
		return endings

if __name__ == "__main__":

	class Field:
		
		def __init__(self,root):
			self.var = StringVar()
			self.entry = Entry(root,textvariable=self.var)
			self.entry.pack(side=LEFT)

		def get(self):
			return self.var.get()
	
	class Cell:
	
		def __init__(self,root,msg):
			self.label = Label(root,text=msg,bg="#DDDDDD",width=20)
			self.label.pack(side=LEFT)
			
	class Header:
	
		def __init__(self,root,msg):
			self.label = Label(root,text=msg,bg="#444444",fg="#FFFFFF",width=20)
			self.label.pack(side=LEFT)

	def go():
		noun = Noun(nom.get(),gen.get(),gender.get())
		toplevel = Toplevel(root)
		new = True
		forms = noun.getforms()
		cases = ["Nominative","Genitive","Dative","Accusative","Ablative"]
		frame = Frame(toplevel)
		frame.pack()
		Header(frame,"")
		Header(frame,"Singular")
		Header(frame,"Plural")
		for i in range(0,5):
			frame = Frame(toplevel)
			frame.pack()
			header = Header(frame,cases[i])
			sing = Cell(frame,forms[i])
			plur = Cell(frame,forms[i + 5])

	root = Tk()
	root.title("Latin Noun Decliner")
	nom = Field(root)
	gen = Field(root)
	gender = Field(root)
	button = Button(root,text="Decline",command=go)
	button.pack(side=LEFT)
	root.mainloop()