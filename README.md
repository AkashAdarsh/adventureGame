## Akash Adarsh (a8@stevens.edu)

### https://github.com/AkashAdarsh/adventureGame/

1. Time spent: Spent about 7 hours on the design, map and coding part of the project. 

2.  Testing:


    *Manually tested the code for bugs, also used doctests. For matching with transcripts i used diff checker.

    *3 must keys, exit might be khaali but should be there
    
    *Small data set with 4-5 rooms items in few rooms checked drop, get items and then tested it with bigger data set
    
    *Tested exits if empty that it goes no where.


3. Unresolved Bugs 

    *If we type only direction as abbreviation it works perfectly, but if we use it along with a verb it will not function. Can be noted as future improvement.
    
    *Exits have to be in dictionary data structure, lists data structures would not be handled.
    
    *Exits will break if not in lower case, key won't match with what has been defined.

4. Resolved Bugs

    *Earlier I had hardcoded the verbs but later used a constants.py so we can maintain a better account of verbs and add more improvements easily in future if needed (more of an improvement than a bug)
     
    *The conditional processing of verbs in adventure.py was added in Line 65
    
    *Wrote a more efficient way of calling processes dynamically
    
    *Made an improvement by usuing getters and setters
    
    
5. The three implemented extentions are:


      -Drop
      
      -Directions as abbreviation 
      
      -Help


