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