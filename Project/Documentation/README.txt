--- english version ---
--- deutsche Version darunter ---

	INSTALLATION
	last tested with python 3.9.1 on Windows 10

	1. install python:
	https://www.python.org/downloads/

	2. in python installer:
	check "install pip"
	check "add python to PATH"

	3. on console (cmd):
	pip install pygame
	pip install pygame_gui


	HOW TO USE
	"data/properties.txt":
		--- server ---
		You can specify the IPv4 address you want to connect to on line server ("127.0.0.1" does not work)
		The port can also be changed, but "5555" is the commonly used port
		If you start server.py the created server will use your address and the specified port

		--- ip notes ---
		In ip notes you can save addresses to easily copy-paste them into the server field
		There are no programmed features for those ip notes, so this section is purly for your convenience

		--- layout ---
		"width" specifies the width of the created client window on startup. The ratio is locked to 16:9. 
		If behind "fullscreen" is written "true", the client window will startup in fullscreen. / not tested on not 16:9 Screens

		Any other section is used as color theme saving slot
		These sections are recommended to be edited via the client command "//save themeName"
		This adds or replaces the theme
		To load a theme use the "//load themeName" command
		To list all the themes use the "//themes" command
		To delete a theme, just delete the section including both "--- themeName ---" tags

		If something goes wrong with the "data/properties.txt" file, use the "data/properties backup.txt" to copy-paste it's contents over
		This will delete all themes except the classic theme!

	"server.py":
		execute the server.py file to start a 4InARow server
		The server.py can be closed anytime normally, which closes all connected clients

	"client.pyw":
		execute the client.pyw file to start a game Instance
		read data/properties to learn about connecting to the right server
		The client window can be closed via: the usual close, the "ESC" key or the "/close" command
		This will also close all other client Instances connected to this game

		basic client controlls:
			Some commands can be shown in the client windows chat via "/help"
			The window size can be changed via the chat command "//scale 'width'" (in pixels)
			The fullscreen can be toggled in the client window via the "TAB" key
			A message is send via the "RETURN" key
			A list of send messages can be reloaded into the chat entry via the "UP" and "DOWN" keys


	Developer: Niklas Ertle

		
--- deutsche Version ---
--- english version above ---

	INSTALLATION
	zuletzt getestet mit python 3.9.1 auf Windows 10

	1. installiere Python:
	https://www.python.org/downloads/

	2. im Python installer:
	markiere "installiere pip"
	markiere "Python zum PATH hinzufügen"

	3. in der Konsole (cmd):
	pip install pygame
	pip install pygame_gui


	GEBRAUCHSANWEISUNG
	"data/properties.txt":
		--- server ---
		Die IPv4 Serveraddresse muss auf der Zeile server angegeben werden ("127.0.0.1" funktioniert nicht)
		Der verwendete Port kann geändert werden, aber "5555" ist der verwendete Standart Port
		Beim Start des Servers wird deine Addresse verwendet, aber der Port wird aus "data/properties.txt" geladen

		--- ip notes ---
		In IP Notizen kannst du IP-Addressen speichern um diese schnell in die Zeile server einfügen zu können
		Die Ip Notizen werden programm technisch nicht genutzt, also sind diese nur zur einfachheit da

		--- layout ---
		"width" beschreibt die breite des Client Fensters beim Start. Das Seitenverhältnis ist auf 16:9 beschränkt
		Wenn hinter "fullscreen" "true" geschrieben ist, wird das Client Fenster im Vollbild gestartet. / nicht getestet auf nicht 16:9 Monitoren

		Alle anderen Sektionen werden als Farb-Thema Speicherplatz genutzt
		Es wird empfohlen diese Themen in einem Client Fenster mit dem Chat Befehl "//save ThemaName" zu bearbeiten
		Dies ersetzt oder fügt das Thema hinzu
		Um ein Thema zu laden, benutze den "//load ThemaName" Befehl
		Um eine Liste von Themen zu laden, benutze den "//themes" Befehl
		Um ein Thema zu löschen, lösche die Zeilen von/bis "--- ThemaName ---"

		Wenn etwas mit der Datei "data/properties.txt" schiefläuft, nutze die Datei "data/properties backup.txt" um dessen Inhalte einzufügen
		Dass wird alle Themen bis auf "classic" löschen!

	"server.py":
		führe die server.py Datei aus um einen 4InARow Server zu starten
		Das Programm "server.py" kann jederzeit normal geschlossen werden, was all verbundenen Clients schließt

	"client.pyw":
		führe die "client.pyw" Datei aus, um eine Spiel Instanz zu starten
		Lies "data/properties.txt" um herauszufinden, wie du dich mit dem richtigen Server verbindest
		Das Client Fenster kann kann mit der "ESC" Taste, mit dem "/close" Befehl oder ganz normal geschlossen werden
		Dass wird auch alle anderen Client Instanzen schließen, die auf das Spiel zugreifen

		Grundlegende Client Steuerung:
			Einige Befehle können mit dem "/help" Befehl angezeigt werden
			Die Fenstergröße kann mit dem Befehl "/scale 'breite'" (in Pixel) geändert werden
			Der Vollbildmodus kann mit der Taste "TAB" gewechselt werden
			Eine Nachricht wird mit der "ENTER" Taste versendet
			Eine Liste der versendeten Nachrichten kann mit den Tasten "PFEIL HOCH" und "PFEIL RUNTER" in die Texteingabe geladen werden


	Entwickler: Niklas Ertle