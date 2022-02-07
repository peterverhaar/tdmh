
import re
import os
import nltk

def word_tokenise( text ):
    tokens = []
    text = text.lower()
    text = re.sub( r'--' , ' -- ' , text)
    text = re.sub( r'-\"' , ' -- ' , text)
    text = re.sub( r'-\'' , ' -- ' , text)
    words = re.split( r'\s+' , text )
    for w in words:
        w = w.strip( string.punctuation )
        if re.search( r"[a-zA-Z]" , w ):
            tokens.append(w)
    return tokens

def flesch_kincaid( asl , asw ):
    fk = 0.39 * ( asl )
    fk = fk + 11.8 * ( asw )
    fk = fk - 15.59
    return fk

def sortedByValue( dict ):
    return sorted( dict , key=lambda x: dict[x])


def divideIntoSegments( full_text , nr_segments ):

    segments = []


    all_words = word_tokenise( full_text )

    segmentSize = int( len(all_words) / nr_segments )

    count_words = 0
    text = ''

    for word in all_words:
        count_words += 1
        text += word + ' '

        ## This line below used the modulo operator:
        ## We can use it to test if the first number is
        ## divisible by the second number
        if count_words % segmentSize == 0:
            segments.append(text.strip())
            text = ''
    return segments


def removeExtension(text):
    new_text = re.sub( '\.txt' , '' , text )
    return new_text

def removeStopWords( freq ):

    from nltk.corpus import stopwords
    stopwords_list = stopwords.words('english')

    filtered = dict()

    for w in freq:
            if w not in stopwords_list:
                filtered[w] = freq[w]

    return filtered

def countSyllables( word ):
    pattern = "e?[aiou]+e*|e(?!d$|ly).|[td]ed|le$|ble$|a$|y$"
    syllables = re.findall( pattern , word )
    return len(syllables)

def ptb_to_wordnet(PTT):

    if PTT.startswith('J'):
        ## Adjective
        return 'a'
    elif PTT.startswith('V'):
        ## Verb
        return 'v'
    elif PTT.startswith('N'):
        ## Noune
        return 'n'
    elif PTT.startswith('R'):
        ## Adverb
        return 'r'
    else:
        return ''


def remove_punctuation(words):
    new_list= []
    for w in words:
        if w.isalpha():
            new_list.append( w )
    return new_list


def remove_pg_boilerplate(complete_file):

    lines = re.split( r'\n' , complete_file )
    read_mode = 0
    full_text = ''

    for line in lines:
        #print(line)
        if read_mode == 1:
            full_text += line + '\n'

        if re.search( r'\*{3,}\s+START\s+OF\s+TH(E|IS)\s+PROJECT\s+GUTENBERG\s+EBOOK' ,  str(line) , re.IGNORECASE ):
            read_mode = 1
        if re.search( r'\*{3,}\s+END\s+OF\s+TH(E|IS)\s+PROJECT\s+GUTENBERG\s+EBOOK' ,  str(line) , re.IGNORECASE ):
            read_mode = 0

    full_text = full_text.strip()
    if re.search( r'^Produced by' , full_text , re.IGNORECASE ):
        full_text = full_text[ full_text.index('\n') : len(full_text) ]
    return full_text
