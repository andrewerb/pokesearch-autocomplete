# -*- coding: utf-8 -*-
# Trie class implementation for AutoComplete
# 
__author__ = "Andrew Erb"
# Best if run in Python 3!

'''
    This project is a Node based Trie class implementation for String Autocompletion/Autosuggestion
    Nodes objects each hold a dictionary of child nodes. 
    Each key,value pair is a character to node matching that label.
    These nodes create a chain of strings. That string/word is stored in data in the last node of that word's traversal.
    Heavily influenced by Nick Stanisha's C++ Trie implementation

    Lowercase and not nested dictionary, but leverages pythonic dictionaries and data types
    * TODO:
        - Stricter type checking in methods (mostly strings)
        - regular expression to ommit whitespace
'''

''' *TODO '''
#### DB
#### API Post
#### Visualize full Trie + Print (follow dict model ?)

class Node:
    """ 
        Node class for Trie nodes.
        @Methods: ...
    """
    def __init__(self, label=None, data=None):
        """ Each node has a label, optional data value, and dictionary of child nodes."""
        self.label = label
        self.data = data # full words
        self.children = dict()

    def addChild(self, key, data=None): 
        """new key is a node-to-be added to existing node"""
        if not isinstance(key, Node) in self.children:
            self.children[key] = Node(key, data) # new Node with key as label and whatever provided data
        else:
            self.children[key].label = key # redundant label checking during setting
        
    def __getitem__(self, key):
        '''Special method. Yields a child-node of this node, at specified key.
            Syntax: this_node[a_key]
            Yields: this_node.children[key] (a Node value)'''
        return self.children[key]

    
    def __del__(self):
        """*TODO"""
        pass

class Trie: 
    '''Trie Class'''
    def __init__(self):
        self.root = Node()
        

    def __format_input(self, word=str("")):
        '''keep input case insensitive by handling all as lowercase'''
        if word is None:
            return None
        else:
            return (str(word.lower()))
    
    def __getitem__(self, key):  # FIX
        return self.root.children[key]

    '''
    def __del__(self, key):
        pass
    '''

    def add_word(self, word):
        '''Add a new word to the Trie'''
        word = self.__format_input(word) #stored in lowercase for consistency
        current_node = self.root
        word_finished = True

        for index, letter in enumerate(word): #check for letters that exist already
            if letter in current_node.children:
                current_node = current_node.children[letter]
            else:
                word_finished = False
                break
        
        if not word_finished:
            '''If word wasn't fully entered initially...'''
            for element in word[index:]:
                '''...for every new letter, create a new child node. (starting from index where the last loop left off.)'''
                current_node.addChild(element)
                current_node = current_node.children[element]
                

        current_node.data = word
        '''Complete word is stored in node data, at the final node of the chain.
            This is to avoid having to implement a stack to keep track of words.'''
    
    def has_word(self, word): ##false if 1 letter
        '''Check for truthiness of word present as an exact/full match in Trie'''
        if word == '':
            return False
        if word is None:
            raise ValueError('Trie.has_word requires a not-Null string')
        
        word = self.__format_input(word)
        
        current_node = self.root  # start check at the root node
        
        for letter in word:
            if letter in current_node.children:
                current_node = current_node.children[letter]
            else:
                return False
        else: ##reconsider this!! 
            if current_node.data is None: 
                return False
            else:
                return True
        
    def __get_prefix_node(self, prefix):
        ''' Helper method for getting prefix matches '''
        top_node = self.root
        print ("prefix in helper is  :" + prefix )
        for letter in prefix:  
            # gets node at end of prefix
            if letter in top_node.children:
                top_node = top_node[letter]
            else:
                return None  # Prefix not in trie, go no further
        else: # successful response
            return top_node
        

    def __get_prefix_words(self, search_node, max_result_list_size=None):
        word_list = list()
        
        for key, current_node in sorted( search_node.children.items() ):
            if current_node.data:
                # data is a full word string. Added to results list.
                word_list.append(current_node.data)
            if max_result_list_size and len(word_list)>=max_result_list_size:
                return word_list
            if current_node.children:
                # if current_node has are children, function recursively visits those.
                word_list.extend(self.__get_prefix_words(current_node, max_result_list_size))
                
            return word_list
        

    def get_prefix_matches(self, prefix, max_result_list_size=None):
        """ Returns a list of all words in Trie that start with requested prefix """
        prefix = self.__format_input(prefix)
        
        if prefix is None:
            raise ValueError('Requires a non-Null prefix value')

        top_node = self.__get_prefix_node(prefix) #expect node or None

        if top_node is None or not top_node.children:
            # Either no Node or no children to traverse. Result is empty list
            return []
        else:
            return (self.__get_prefix_words(top_node)) # Find list of matches; Expects list output
            

def main():
    print("Trie module running.")
    
    pkmn_trie = Trie()
    pkmn_list = ["pikachu","pikachus","pikano","pikano","squirtle","alakazam","charizard","kadabra","charmander"]
    for item in pkmn_list:
        print(item)

    for elem in pkmn_list:
        pkmn_trie.add_word(elem)
    
    print("\n\nTrying out get matches now... \n\n")
    test_query = ["pika","squ","pikachu"]
    print( str(pkmn_trie.get_prefix_matches(test_query[0])) )
    print( str(pkmn_trie.get_prefix_matches(test_query[1])) )
    print( str(pkmn_trie.get_prefix_matches(test_query[2])) )
    
    

if __name__ == '__main__':
    main()