import csv

class Data:
    def __init__(self, filepath):
        self.filepath = filepath
        self.allData = []
        self.update()
    
    def update(self):
        try:
            self.allData = []
            with open(self.filepath, 'r') as fd:
                reader = csv.reader(fd)
                for row in reader:
                    if row != []:
                        self.allData.append(row)
        except:
            print("can't load file")

    # searches for first value with index
    def find(self, index):
        for element in self.allData:
            if element[0] == index:
                return element[1]

    def findColorList(self, themeName):
        fromTo = []
        theme = f"--- {themeName} ---"
        for i, element in enumerate(self.allData):
            if element[0] == theme:
                fromTo.append(i)
                
        dictionary = { f"{self.allData[i][0]}" : f"{self.allData[i][1]}" for i in range(fromTo[0]+1,fromTo[1]) }

        for x in dictionary:
            c = dictionary[x]
            dictionary[x] = tuple(int(c[i:i+2], 16) for i in (0, 2, 4))

        return dictionary

    def listThemes(self):
        themes = []
        for element in self.allData:
            if element[0][:3] == "---":
                if themes == []:
                    themes.append(element[0][4:-4])
                elif element[0][4:-4] != themes[-1]:
                    themes.append(element[0][4:-4])
        themes.remove('server')
        themes.remove('ip notes')
        themes.remove('layout')
        return themes

    '''
    # could be used to return a specific section of the file via the tag

    def findList(self, index):
        fromTo = []
        for i, element in enumerate(self.allData):
            if element[0] == index:
                fromTo.append(i)
        dictionary = { f"{self.allData[i][0]}" : f"{self.allData[i][1]}" for i in range(fromTo[0]+1,fromTo[1]) }
        return dictionary
    '''

    def formatSave(self, themeName, colorDictionary):
        theme = f"--- {themeName} ---"
        toSave = [[theme]]
        for element in colorDictionary:
            toSave.append([element,f"{'%02x%02x%02x' % colorDictionary[element]}"])
        toSave.append([theme])
        return toSave

    def save(self, themeName, colorDictionary):
        toSave = self.formatSave(themeName, colorDictionary)
        print(toSave)
        with open(self.filepath, 'r') as fd:
            reader = csv.reader(fd)
            file = list(reader)

        if len(toSave) == 10:
            with open(self.filepath, 'w', newline='') as fd:
                writer = csv.writer(fd)
                found = False
                # find and replace
                for row in file:
                    try:
                        if len(toSave) > 0:
                            if row == toSave[0] and len(toSave[0]) == 1:
                                found = True
                            if found:
                                row = toSave[0]
                                toSave.pop(0)
                        else:
                            break
                    except:
                        print(toSave)
                # add at the end
                if len(toSave) != 0:
                    for line in toSave:
                        file.append([])
                        file[-1] = line
                    file.append([])
                # write to file
                for row in file:
                    writer.writerow(row)
        else:
            print("save format not valid")
        self.update()


#d = Data('properties.txt')
#print(d.allData)
#print(d.server)
#print(type(d.find("width")))
#print(d.findColorList("classic"))
#print(d.findList("--- layout ---"))
#d.formatSave("new", d.findColorList("--- colors ---"), 'properties.txt')