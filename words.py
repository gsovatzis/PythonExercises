
words = []
biggestWords = []
vowels = ['a','e','i','o','u','y']

def readFile():
    # Αυτή η μέθοδος ανοίγει το αρχείο, διαβάζει τις γραμμές του
    # και σπάει κάθε γραμμή σε λέξη όπου αφαιρεί το ΕΝΤΕΡ και βάζει την λέξη
    # στην λίστα words
    
    fp = open('words.txt','r')

    lines = fp.readlines()

    for line in lines:
        for word in line.split(" "):
            words.append(word.replace('\n',''))

def findBiggestWords():
    # Αυτή η μέθοδος βρίσκει τις 5 μεγαλύτερες λέξεις στην λίστα words και τις βάζει
    # στην λίστα biggestWords
    for word in words:
        if len(biggestWords) < 5:
            biggestWords.append(word)
        else:
            bwi = getSmallestWordIndex()
            if len(word) > len(biggestWords[bwi]):
                biggestWords[bwi] = word

def getSmallestWordIndex():
    # Βοηθητική μέθοδος που μας επιστρέφει τη θέση της μικρότερης λέξης
    # στην λίστα biggestWords
    smallest = 0

    for i in range(1,5):
        if len(biggestWords[i]) < len(biggestWords[smallest]):
            smallest = i

    return smallest

def returnWordWithoutVowels(word):
    # Βοηθητική μέθοδος που επιστρέφει μια αγγλική λέξη χωρίς τα φωνήεντα
    vowelFound=False
    result = ''
    for c in word:
        for v in vowels:
            if c.lower()==v:
                vowelFound = True
                break
            else:
                vowelFound = False

        if not vowelFound:
            result = result + c
    return result

def reverseWord(word):
    # Βοηθητική μέθοδος που αντιστρέφει τους χαρακτήρες μιας λέξης
    return word[::-1]

######## ΑΠΟ ΕΔΩ ΞΕΚΙΝΑΕΙ ΤΟ ΠΡΟΓΡΑΜΜΑ - ΑΡΧΗ ############

readFile()          # Ανάγνωση του αρχείου
findBiggestWords()  # Βρες τις 5 μεγαλύτερες λέξεις

# Για κάθε μια από τις 5 μεγαλύτερες λέξεις, τύπωσε τες χωρίς τα φωνήεντα
# και με αντεστραμένους χαρακτήρες
for word in biggestWords:
    print(reverseWord(returnWordWithoutVowels(word)))
