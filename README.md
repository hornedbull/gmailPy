__     __    _             _   ____  _           _     
\ \   / /_ _| |_ ___  __ _| | / ___|| |__   __ _| |__  
 \ \ / / _` | __/ __|/ _` | | \___ \| '_ \ / _` | '_ \ 
  \ V / (_| | |_\__ \ (_| | |  ___) | | | | (_| | | | |
   \_/ \__,_|\__|___/\__,_|_| |____/|_| |_|\__,_|_| |_|

ECE - C433 Mini - Project 2
gmailPy - A terminal gmail client
Tested on Python 2.7.3

Installation:

imapclient package is required to run this program and is not a part of the standard python library
install using 'sudo pip install imapclient'

Run:

Please use 'python gmailPy.py -h' for any help

Features:

1. Create a new folder:
    'python gmailPy.py -n FOLDERNAME' creates a new folder in the account. This is achieved using create_folder method in IMAPClient.
2. Delete a folder:
    'python gmailPy.py -d FOLDERNAME' deletes the folder provided as an argument. This is achieved using delete_folder method in IMAPClient.
3. Rename a folder:
    'python gmailPy.py -n OLDFOLDERNAME NEWFOLDERNAME' renames the folder. This is achieved using rename_folder method in IMAPClient.
4. Merge two folders:
    'python gmailPy.py -m MERGEDFOLDERNAME FOLDER1NAME FOLDER2NAME' creates a new folder with MERGEDFOLDERNAME and adds the messages from FOLDER1NAME and FOLDER2NAME to it. This is achieved using copy method in IMAPClient which uses IMAP flags to move messages. No local copy is stored on the machine and thus it is scalable with very little runtime. Finally, FOLDER1NAME and FOLDER2NAME are deleted after the merge operation is complete.
5. Search for big mail:
    'python gmailPy.py -b FOLDERNAME'. First searches for all the not deleted mail in FOLDERNAME and then fetches the sizes for all the message ids returned during the search operation. All the sizes are received in one request with a return time < 10 ms. Thus, it is scalable for folders with a lot of messages. Once sizes are returned, the method sorts the message ids by descending order of their sizes. The method now iterates through the list of sorted message ids and prompts the user with necessary information about the big message(From, To, Subject & Size) and asks whether to delete the message or not. Note that this is the only time the entire message is fetched from the server. The method keeps iterating through the list until the user exits by entering 0 or using ctrl + c. Multiple messages are not fetched at a time in entirity to save space and also that it usually only the biggest few that need to be deleted.
6. Search for big mail with search criteria:
    'python gmailPy.py -s FOLDERNAME COMMAND CRITERIA'. This method is very similar to big mail with the same time complexity and space complexity. The only change is the first step of the process. Instead of searching for all the non - deleted messages as the big mail did, this method searches for a particular criteria based on COMMAND(TO, FROM, SUBJECT) and CRITERIA. For example, 'python gmailPy.py -s INBOX FROM xyz@gmail.com'. This will search for all the mails that match the search criteria
    in this case all the mails from xyz@gmail.com. Then use those message ids to fetch the message sizes. Then follow the same trend as in big mail to sort and promt the user.
