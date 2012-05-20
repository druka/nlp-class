import sys, traceback, re

class Wiki:
    
    # reads in the list of wives
    def addWives(self, wivesFile):
        try:
            input = open(wivesFile)
            wives = input.readlines()
            input.close()
        except IOError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback)
            sys.exit(1)    
        return wives
    
    
    def namesMatch(self, name1, name2):
        match = True
        for word in re.split('\s+', name1.strip()):
            if not re.search(word, name2):
                match = False
        return match
    
    # read through the wikipedia file and attempts to extract the matching husbands. note that you will need to provide
    # two different implementations based upon the useInfoBox flag. 
    def processFile(self, f, wives, useInfoBox):
        
        husbands = []
        mapping = []
        text = f.read()
        
        if useInfoBox:
            for box in re.findall('\{\{Infobox([^|]+)(.*?)\n\}\}', text, re.S):
                name = re.search('\|(?:N|n)ame\s*=(.*?)(\n|\|)', box[1])
                spouse = re.search('\|(?:S|s)pouse\s*=(.*?)\n', box[1])
                if name and spouse:
                    name = name.groups()[0].strip()
                    for wife in re.split('&lt;br\s*/&gt;', spouse.groups()[0]):
                        wife = re.sub('\[|\]|\(.*|.*\|', '', wife).strip()
                        mapping.append((name, wife))
        else:
            for page in re.findall('<page>(.*?)</page>', text, re.S):
                title   = re.search('<title>(.*?)</title>', page).groups()[0]
                surname = re.split('\s+', title.strip()).pop()
                
                text = re.search('<text.*?>(.*?)</text>', page, re.S).groups()[0]
                text = re.sub('\{\{Infobox([^|]+)(.*?)\n\}\}', '', text)
                
                name_match = '(?:((?: [A-Z][a-zA-Z]*)+)| \[\[(.*?)\]\])'
                prefixes = [
                    surname + ' married',
                    surname + ' met',
                    surname + ' proposed to',
                    ' he married',
                    ' he met',
                    ' he proposed to',
                    ' is married to',
                    ' has been married to',
                    ' was married to'
                ]
                for prefix in prefixes:
                    m = re.search(prefix + name_match, text, re.S)
                    if m:
                        for wife in m.groups():
                            if wife: mapping.append((title, wife.strip()))
                
                m = re.search('((?:[A-Z][a-zA-Z]* )+)who married((?: [A-Z][a-zA-Z]*)+)', page, re.S)
                if m:
                    groups = m.groups()
                    mapping.append((groups[1].strip(), groups[0].strip()))
        
        for wife in wives:
            match = None
            for pair in mapping:
                if not match:
                    if self.namesMatch(wife, pair[1]) or self.namesMatch(pair[1], wife):
                        match = pair[0]
            if match:
                husbands.append('Who is ' + match + '?')
            else:
                husbands.append('No Answer')
        
        f.close()
        return husbands
    
    # scores the results based upon the aforementioned criteria
    def evaluateAnswers(self, useInfoBox, husbandsLines, goldFile):
        correct = 0
        wrong = 0
        noAnswers = 0
        score = 0 
        try:
            goldData = open(goldFile)
            goldLines = goldData.readlines()
            goldData.close()
            
            goldLength = len(goldLines)
            husbandsLength = len(husbandsLines)
            
            if goldLength != husbandsLength:
                print('Number of lines in husbands file should be same as number of wives!')
                sys.exit(1)
            for i in range(goldLength):
                if husbandsLines[i].strip() in set(goldLines[i].strip().split('|')):
                    correct += 1
                    score += 1
                elif husbandsLines[i].strip() == 'No Answer':
                    noAnswers += 1
                else:
                    wrong += 1
                    score -= 1
        except IOError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback)
        if useInfoBox:
            print('Using Info Box...')
        else:
            print('No Info Box...')
        print('Correct Answers: ' + str(correct))
        print('No Answers: ' + str(noAnswers))
        print('Wrong Answers: ' + str(wrong))
        print('Total Score: ' + str(score)) 

if __name__ == '__main__':
    wikiFile = '../data/small-wiki.xml'
    wivesFile = '../data/wives.txt'
    goldFile = '../data/gold.txt'
    useInfoBox = True;
    wiki = Wiki()
    wives = wiki.addWives(wivesFile)
    husbands = wiki.processFile(open(wikiFile), wives, useInfoBox)
    wiki.evaluateAnswers(useInfoBox, husbands, goldFile)