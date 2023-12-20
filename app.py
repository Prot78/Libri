"""
Catalogo libri
In questo programma un csv contenente un database di libri viene letto
e un website mostra i risultati della ricerca nel database. la ricerca e' prima salvata su output.txt e poi riportata nel sito.
http://127.0.0.1:5000/hello      to open the website
http://127.0.0.1:5000/greet      to interacte with the server
"""

import pandas as pd
import numpy as np
from flask import Flask, request, render_template, flash


app = Flask(__name__)

def your_python_code(input_frase):
    # Your Python code here
    ####   INPUT   ###############
    word_input = input_frase
    catalogo_libri_file_name = 'Catologo_Libri.csv'
    #############################


    #######    MAIN   #######################################################

    # Read the CSV file
    print(word_input)
    word = ''.join(word_input)   # Make the words string type
    print(word)
    word = word.lower()    # Convert words to lowercase
    print(word)

    df = pd.read_csv(catalogo_libri_file_name)
    row_count = len(df)

    #####################
    ## This function takes a list and returns a new list excluding all numbers.
    def exclude_numbers(data_list):
        filtered_list = [item for item in data_list if not isinstance(item, (int, float))]
        return filtered_list

    ## Compares a word to each element in a list and prints the entire row if there's a match.
    def compare_word_to_list(word, list_of_words):
        nessuna_corrispondenza = 0
        titolo_o_autore_corrispondenza = 0
        titolo_o_autore_lista = []
        for row in list_of_words:
            if word in row or any(word in element for element in row): 
                #print(row)  # Print the entire row if there's a match
                titolo_o_autore_lista.append (row)
                titolo_o_autore_corrispondenza += 1  #this is needed to truck the correspondance in the next if
            else:
                nessuna_corrispondenza += 1
        #result = "Ci sono risultati"
        if nessuna_corrispondenza > 0 and titolo_o_autore_corrispondenza == 0 :
            print("Nessuna corrispondenza con titoli o autori")
            #result = "Nessuna corrispondenza con titoli o autori"
        return titolo_o_autore_lista, nessuna_corrispondenza, titolo_o_autore_corrispondenza
    #######################
    
    ########################################
    #words_autore = df['Column1 (Even)'].values.ravel()
    words_autore = df.values.ravel()

    filtered_list_autore = exclude_numbers(words_autore)
    filtered_list_autore = [word.lower() for word in filtered_list_autore]    # Convert words to lowercase (optional)
    import string   # Remove punctuation (optional)
    filtered_list_autore = [word for word in filtered_list_autore if word not in string.punctuation]

    

    titolo_o_autore_lista, nessuna_corrispondenza, titolo_o_autore_corrispondenza = compare_word_to_list(word, filtered_list_autore)

    
    ## in this part we find a match between the title found in the input and the database
    Column1_lower_case = [word.lower() for word in df['Column1 (Even)']]
    Column2_lower_case = [word.lower() for word in df['Column2 (Odd)']]

    # Made a list of uniques autori e titoli
    titolo_o_autore_lista_unique = []
    for name in titolo_o_autore_lista:
        if name not in titolo_o_autore_lista_unique:
            titolo_o_autore_lista_unique.append(name)

    titolo_o_autore_lista_array = np.array(titolo_o_autore_lista_unique, dtype=str)
    
    file_path = "output.txt"
    result = []
    ##########################
    ##  Extracting from the database the autori and titoli correspondent to the word of input
    
    if nessuna_corrispondenza > 0 and titolo_o_autore_corrispondenza == 0 :
        print('\nLa ricerca NON ha dato risultati: Please try again \n')
        with open(file_path, 'w') as file:
            file.write("\nLa ricerca NON ha dato risultati: Please try again \n")
        result ='\nLa ricerca NON ha dato risultati: Please try again \n'
    else:
        print('\nLa ricerca ha dato questi risultati: \n')
        count = 0
        for i in range(0,row_count):
            for ii in range(len(titolo_o_autore_lista_unique)):
                if titolo_o_autore_lista_array[ii] == Column1_lower_case[i]:
                    print(df.iloc[i, :])
                    print('\n')
                    count += 1
                    
                    result.append(df.iloc[i, :])

        for i in range(0,row_count):
            for ii in range(len(titolo_o_autore_lista_unique)):
                if titolo_o_autore_lista_array[ii] == Column2_lower_case[i]:
                    print(df.iloc[i, :])
                    print('\n')
                    count += 1
                    result.append(df.iloc[i, :])
        
        ###### creiamo un text file where to report the results and then move them to the web, didn't find an alternative method
        with open(file_path, 'w') as file:
            file.write("Numero di libri trovati =  %s  (Autore - Titolo - Numero di copie disponibili) \n\n" % (count))
            
            numpy_array = np.array(result, dtype=str)
            print(numpy_array)

            for row in numpy_array:
                for cell in row:
                    # Split each string into words
                    words = cell.split()
                    # Write each word to the file
                    file.write(' '.join(words) + '\n')
                file.write(' '+ '\n')

            file.write('\n\nNumero di libri con titolo unico nel database = %s \n\n' % (row_count))
        #######################################################
        print ("numero di libri trovati = ", count)
        print('\nNumero di unique libri nel database = ', row_count, "\n")

    ############################
    return result


@app.route('/hello')
def input_code():
    return render_template('index.html')

@app.route('/greet', methods=["POST"])
def execute_code():
    input_frase = str(request.form['name_input'])
    result= your_python_code(input_frase)  ## the result variable is not used, because we copy all the results in a text file. it could be deleted
    with open('output.txt', 'r') as file:
        file_content = file.read()

    # Render the HTML template with the file content
    return render_template('index.html', file_content=file_content)

if __name__ == '__main__':
    app.run(debug=True)

