from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

def process_input(request):
    try:
        rejected_letters = request.POST['rejected_letters'].lower()
    except:
        rejected_letters = ''
    #Wrong place letters

    w1 = request.POST['wrong_place_letters1'].lower()
    if w1 == '':
        w1 = '-'

    w2 = request.POST['wrong_place_letters2'].lower()
    if w2 == '':
        w2 = '-'

    w3 = request.POST['wrong_place_letters3'].lower()
    if w3 == '':
        w3 = '-'

    w4 = request.POST['wrong_place_letters4'].lower()
    if w4 == '':
        w4 = '-'

    w5 = request.POST['wrong_place_letters5'].lower()
    if w5 == '':
        w5 = '-'

    #correct place letters

    c1 = request.POST['correct_letters1'].lower()
    if c1 == '':
        c1 = '-'

    c2 = request.POST['correct_letters2'].lower()
    if c2 == '':
        c2 = '-'

    c3 = request.POST['correct_letters3'].lower()
    if c3 == '':
        c3 = '-'

    c4 = request.POST['correct_letters4'].lower()
    if c4 == '':
        c4 = '-'

    c5 = request.POST['correct_letters5'].lower()
    if c5 == '':
        c5 = '-'


    wrong_place_letters = w1+w2+w3+w4+w5
    correct_letters = c1+c2+c3+c4+c5


    return rejected_letters,wrong_place_letters,correct_letters



def make_word_list():
    five_letter_words = []
    #Using file
    with open(BASE_DIR/'to_do_app/five_letter_words.txt') as f:
            contents = f.read()
            all_words = contents.strip('[]').replace("'",'').split(', ')
    for word in all_words:
        if len(word) == 5:
            five_letter_words.append(word)
    return five_letter_words


def wordle_solver_program(five_letter_words,rejected_letters,wrong_place_letters,correct_letters):

    #---------------ACTUAL LOGIC---------------------------

    if type(five_letter_words) == str:
        five_letter_words = five_letter_words.strip('][').replace("'",'').split(', ')


    #removing words without correct letters in correct spots
    removed = []
    for word in five_letter_words:
        for i in range(len(correct_letters)):
            if correct_letters[i] != '-' and word[i] != correct_letters[i]:
                removed.append(word)
                break

    for word in removed:
        five_letter_words.remove(word)

    #removing words without a letter in wrong spot
    removed = []
    for word in five_letter_words:
        word_list = []
        for letter in word:
            word_list.append(letter)
        for i in range(len(wrong_place_letters)):
            if wrong_place_letters[i] in correct_letters:
                if wrong_place_letters[i] in word and word.index(wrong_place_letters[i]) == correct_letters.index(wrong_place_letters[i]) and wrong_place_letters[i] != '-':
                    word_list[word.index(wrong_place_letters[i])] = '-'
            if wrong_place_letters[i] not in word_list and wrong_place_letters[i] != '-':
                removed.append(word)
                break

    for word in removed:
        five_letter_words.remove(word)

    #removing words with letter placed in wrong spot 
    removed = []           
    for word in five_letter_words:
        for i in range(len(wrong_place_letters)):
            if word[i] == wrong_place_letters[i]:
                removed.append(word)
                break

    for word in removed:
        five_letter_words.remove(word)

    #removing words with rejected letters
    removed = []
    for word in five_letter_words:
        word_list = []
        for letter in word:
            word_list.append(letter)
        for letter in word:
            if letter in correct_letters:
                if word.index(letter) == correct_letters.index(letter):
                    try:
                        word_list[word_list.index(letter)] = '-'
                    except:
                        pass
            if letter in wrong_place_letters:
                try:
                    word_list[word_list.index(letter)] = '-'
                except:
                    pass
            if letter in rejected_letters and letter in word_list:
                removed.append(word)
                break

    for word in removed:
        five_letter_words.remove(word) 

    if len(five_letter_words) == 1:
        return len(five_letter_words),five_letter_words,True
    else:
        return len(five_letter_words),five_letter_words,False