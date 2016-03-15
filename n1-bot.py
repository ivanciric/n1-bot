import requests
import json
import urllib
import urllib2
import random
import time
import Tkinter
import cookielib


class nbot_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
	self.parent = parent
	self.initialize()

    def initialize(self):
        self.grid()

	#entry
	self.urlVariable = Tkinter.StringVar()
        self.entryUrl = Tkinter.Entry(self,
					textvariable=self.urlVariable)
        self.entryUrl.grid(column=0, row=0, columnspan=2, sticky='EW')
	self.urlVariable.set("URL strane komentara")
	#entry

	#entry
	self.comIdVariable = Tkinter.StringVar()
        self.entryComId = Tkinter.Entry(self,
					textvariable=self.comIdVariable)
        self.entryComId.grid(column=0, row=1, columnspan=2, sticky='EW')
	self.comIdVariable.set("data-comid")
	#entry

	#entry
	self.idVariable = Tkinter.StringVar()
        self.entryId = Tkinter.Entry(self,
					textvariable=self.idVariable)
        self.entryId.grid(column=0, row=2, columnspan=2, sticky='EW')
	self.idVariable.set("data-docmeniid")
	#entry


	#entry
	self.typeVariable = Tkinter.StringVar()
        self.entryType = Tkinter.Entry(self,
					textvariable=self.typeVariable)
        self.entryType.grid(column=0,row=3, columnspan=2, sticky='EW')
	self.typeVariable.set("1")
	#entry

	#entry
	self.votesVariable = Tkinter.StringVar()
        self.entryVotes = Tkinter.Entry(self,
					textvariable=self.votesVariable)
        self.entryVotes.grid(column=0,row=4, columnspan=2, sticky='EW')
	self.votesVariable.set("15")
	#entry

	#label
        self.labelVariable = Tkinter.StringVar()
	label = Tkinter.Label(self,
				textvariable=self.labelVariable,
				wraplength=160,
 				anchor="nw",fg="white",bg="black",
				)
        label.grid(column=0, row=5, rowspan=2, columnspan=2, sticky='EWNS')
	self.labelVariable.set("Status...")
	#label

	#button
	button = Tkinter.Button(self,
				text="Glasaj",
				command=self.OnButtonClick)
        button.grid(column=0,row=7)
	#button

	"""
	#button
	stopButton = Tkinter.Button(self,
				text="Prekini",
				command=self.OnStopButtonClick)
        stopButton.grid(column=1,row=6)
	#button
	"""

	#label
        self.copyrightVariable = Tkinter.StringVar()
	copyrightLabel = Tkinter.Label(self,
				textvariable=self.copyrightVariable,
				font=("Helvetica", 8, "italic"),
				anchor="center",fg="black")
        copyrightLabel.grid(column=0, row=8, columnspan=2, sticky='EWNS')
	self.copyrightVariable.set(u"\N{COPYRIGHT SIGN}2016, Hamato Yoshi")
	#label


	self.grid_columnconfigure(0,weight=1)
	self.grid_rowconfigure(4,weight=2)
	self.resizable(True,True)
	self.update()
        #self.geometry(self.geometry())
	self.geometry('300x170')

	self.entryId.focus_set()
        self.entryId.selection_range(0, Tkinter.END)

    def OnButtonClick(self):
	self.running = True
	self.ExecuteVoting()

    def OnStopButtonClick(self):
	self.stop()

    def stop(self):
        self.running = False

	"""
    def OnPressEnter(self,event):
        self.labelVariable.set(self.entryIdVariable.get()")
	"""

    def getToken(self):
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	r = opener.open(self.urlVariable.get())

	token = False

	for cookie in cj:
	    if(cookie.name == '__RequestVerificationToken_Lw__'):
	    	token = cookie.value

	return token


    def ExecuteVoting(self):

	if(self.running == True):

		num_votes = self.votesVariable.get()

		for i in range(1, int(num_votes) + 1):


			token = self.getToken();

			self.labelVariable.set("Glas br. " + str(i) + ": pokusavam...")
			self.update()

			vType = 'Like'
			if(self.typeVariable.get() == '-1'):
			    vType = 'Dislike'

			comm_payload = {}

			url_vote = 'http://rs.n1info.com/Comment/Recommend' + vType + '/' + self.comIdVariable.get() + '/' + self.idVariable.get()

			data = urllib.urlencode(comm_payload)

			headers = {
				"Host": "rs.n1info.com",
				"Referer": "http://rs.n1info.com/",
				"Cookie": "__RequestVerificationToken_Lw__=" + token
			}

			try:
			    req = urllib2.Request(url_vote, data, headers)
			    response = urllib2.urlopen(req)
			except urllib2.HTTPError, e:
			    self.labelVariable.set('Greska - %s.' % e.code)

			self.labelVariable.set("Glas br. " + str(i) + ": OK")
			self.update()

			time.sleep(random.randint(1,3))

		self.labelVariable.set("Glasanje zavrseno.")
		self.update()

	else:
		self.labelVariable.set("Glasanje prekinuto.")
		self.update()



if __name__ == "__main__":
    app = nbot_tk(None)
    app.title('N1Bot')
    app.mainloop()
