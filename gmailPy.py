# Vatsal Shah
# ECE-C433 Mini-Project 2
# gmailPy - A terminal gmail client
# Tested on Python 2.7.3

# imapclient is not a part of the standard python library
# install using sudo pip install imapclient
import getpass
from imapclient import IMAPClient
import operator
import email
import optparse
import sys


class gmailPy(object):
    def __init__(self):
        self.IMAP_SERVER = 'imap.gmail.com'
        self.ssl = True
        self.myIMAPc = None
        self.response = None
        self.folders = []

    def login(self, username, password):
        self.myIMAPc = IMAPClient(self.IMAP_SERVER, ssl=self.ssl)
        self.myIMAPc.login(username, password)

    # Returns a list of all the folders for a particular account
    def get_folders(self):
        self.response = self.myIMAPc.list_folders()
        for item in self.response:
            self.folders.append(item[2].strip('u'))
        return self.folders

    # Returns the total number of messages in a folder
    def get_mail_count(self, folder='Inbox'):
        self.response = self.myIMAPc.select_folder(folder, True)
        return self.response['EXISTS']

    # Method to delete messages based on their size
    def delete_bigmail(self, folder='Inbox'):
        self.myIMAPc.select_folder(folder, False)
        # Gets all the message ids of the messages which are not deleted in the folder
        messages = self.myIMAPc.search(['NOT DELETED'])
        print "%d messages that aren't deleted" % len(messages)
        if len(messages) > 0:
            print "You can exit by entering 0 or pressing CTRL+C \n"
        else: print "There are no messages in the folder"
        # Gets the message sizes for all the message ids returned in previous step
        # Note: Just sends one request for all message ids with a return time < 10 ms
        self.response = self.myIMAPc.fetch(messages, ['RFC822.SIZE'])
        # Sorts the dictionary returned by fetch by size in descending order
        sorted_response = sorted(self.response.iteritems(), key=operator.itemgetter(1), reverse=True)
        count = 1
        try:
            for item in sorted_response:
                # Gets the biggest message including headers, body, etc.
                big_message = self.myIMAPc.fetch(item[0], ['RFC822'])
                for msgid, data in big_message.iteritems():
                    msg_string = data['RFC822']
                    # Parses the message string using email library
                    msg = email.message_from_string(msg_string)
                    val = dict(self.response[msgid])['RFC822.SIZE']
                    print 'ID %d: From: %s Date: %s' % (msgid, msg['From'], msg['date'])
                    print 'To: %s' % (msg['To'])
                    print 'Subject: %s' % (msg['Subject'])
                    print 'Size: %d bytes \n' % (val)
                    user_del = raw_input("Do you want to delete this message?(Y/N): ")
                    if user_del == 'Y':
                        self.delete_message(msgid)
                        if count == len(sorted_response):
                            print "There are no more messages"
                        else:
                            print "\nMoving on to the next biggest message >>> \n"
                    elif user_del == '0':
                        print "Program exiting"
                        sys.exit()
                    else:
                        if count == len(sorted_response):
                            print "There are no more messages"
                        else:
                            print "\nMoving on to the next biggest message >>> \n"
                    count += 1
        except KeyboardInterrupt:
            print "Program exiting"
            sys.exit()

    # Method to delete messages based on their size with a search criteria
    def delete_bigmail_search(self, folder='Inbox', command='', criteria=''):
        self.myIMAPc.select_folder(folder, False)
        # Gets all the message ids from the server based on the search criteria
        messages = self.myIMAPc.search('%s "%s"' % (command, criteria))
        print "%d messages that match --> %s: %s" % (len(messages), command, criteria)
        if len(messages) > 0:
            print "You can exit by entering 0 or pressing CTRL+C \n"
        else: print "There are no messages in that matched your search criteria"
        # Gets the message sizes for all the message ids returned in previous step
        # Note: Just sends one request for all message ids with a return time < 10 ms
        self.response = self.myIMAPc.fetch(messages, ['RFC822.SIZE'])
        # Sorts the messages in decending order of their sizes
        sorted_response = sorted(self.response.iteritems(), key=operator.itemgetter(1), reverse=True)
        count = 1
        try:
            for item in sorted_response:
                # Gets the entire content for the biggest message identified
                big_message = self.myIMAPc.fetch(item[0], ['RFC822'])
                for msgid, data in big_message.iteritems():
                    msg_string = data['RFC822']
                    msg = email.message_from_string(msg_string)
                    val = dict(self.response[msgid])['RFC822.SIZE']
                    print 'ID %d: From: %s Date: %s' % (msgid, msg['From'], msg['date'])
                    print 'To: %s' % (msg['To'])
                    print 'Subject: %s' % (msg['Subject'])
                    print 'Size: %d bytes \n' % (val)
                    user_del = raw_input("Do you want to delete this message?(Y/N): ")
                    if user_del == 'Y':
                        self.delete_message(msgid)
                        if count == len(sorted_response):
                            print "There are no more messages"
                        else:
                            print "\nMoving on to the next biggest message >>> \n"
                    elif user_del == '0':
                        print "Program exiting"
                        sys.exit()
                    else:
                        if count == len(sorted_response):
                            print "There are no more messages"
                        else:
                            print "\nMoving on to the next biggest message >>> \n"
                    count += 1

        except KeyboardInterrupt:
            print "Program exiting"
            sys.exit()

    # Deletes a message in the current folder based on msg id
    def delete_message(self, id):
        try:
            self.myIMAPc.delete_messages([id])
            self.myIMAPc.expunge()
            print "Message deleted"
        except IMAPClient.Error as err:
            print "Message deletion failed"
            print err

    # Renames a folder
    def rename_folder(self, oldfolder, newfolder):
        try:
            self.myIMAPc.rename_folder(oldfolder, newfolder)
            print "Folder %s renamed to %s" % (oldfolder, newfolder)
        except IMAPClient.Error as err:
            print "Folder renaming failed"
            print err

    # Creates a new folder
    def create_folder(self, folder):
        try:
            self.myIMAPc.create_folder(folder)
            print "New folder %s created" % folder
        except IMAPClient.Error as err:
            print "Folder creation failed"
            print err

    # Deletes a folder
    def delete_folder(self, folder):
        try:
            self.myIMAPc.delete_folder(folder)
            print "Folder %s deleted" % folder
        except IMAPClient.Error as err:
            print "Folder deletion failed"
            print err

    # Creates a new folder and copies the content from the two folders that need to be merged
    # Then deletes the old folders
    def merge_folders(self, merged_folder, folder_1, folder_2):
        try:
            self.create_folder(merged_folder)
            # Selects the folder with read/write permission
            self.myIMAPc.select_folder(folder_1, True)
            messages = self.myIMAPc.search(['NOT DELETED'])
            print "Moving %d messages from %s to %s" % (len(messages), folder_1, merged_folder)
            self.myIMAPc.copy(messages, merged_folder)
            self.myIMAPc.select_folder(folder_2, True)
            messages = self.myIMAPc.search(['NOT DELETED'])
            print "Moving %d messages from %s to %s" % (len(messages), folder_2, merged_folder)
            self.myIMAPc.copy(messages, merged_folder)
            print "Deleting %s and %s..." % (folder_1, folder_2)
            self.delete_folder(folder_1)
            self.delete_folder(folder_2)
            print "Merge folder operation succeeded"
        except IMAPClient.Error as err:
            print "Merge operation failed"
            print err

    def logout(self):
        self.myIMAPc.logout()


def main():
    # Using parser library for handling command line arguments
    usage = "usage: python gmailPy.py [options]"
    prog_desc = """gmailPy is a scalable command line gmail client capable of adding, deleting, renaming and merging folders. It also provides interface for the user to delete big messages based on size and search criteria."""
    parser = optparse.OptionParser(usage=usage, description=prog_desc)
    parser.add_option(
        '-l', '--list', help="List folder statistics. This doesn't need any arguments. Usage: python gmailPy.py -l", dest='lf',
        default=False, action='store_true')
    parser.add_option(
        '-b', '--big', help='Delete big messages. Please enter folder name as an argument. For example: python gmailPy.py -b INBOX',
        dest='big_folder_name', action='store')
    parser.add_option(
        '-s', '--bigsearch', help='Delete big messages based on search criteria. This takes 3 arguments folder_name, command and criteria. For example: python gmailPy.py -s INBOX FROM xyz@gmail.com',
        dest='bigsearch_folder_name', action='store', nargs=3)
    parser.add_option(
        '-n', '--new', help='Create new folder. Please enter folder name as an argument. For example: python gmailPy.py -n Test_folder',
        dest='new_folder_name', action='store')
    parser.add_option(
        '-d', '--del', help='Delete a folder. Please enter folder name as an argument. For example: python gmailPy.py -d Test_folder',
        dest='del_folder_name', action='store')
    parser.add_option(
        '-r', '--rename', help='Rename a folder. Please enter old_folder_name and new_folder_name as two arguments. For example: python gmailPy.py -r OLDFOLDERNAME NEWFOLDERNAME',
        dest='rename_folder_name', action='store', nargs=2)
    parser.add_option(
        '-m', '--merge', help='Merge two folders. This takes 3 arguments merged_folder_name , folder_1_name , folder_2_name. For example: python gmailPy.py -m Test_folder_2 Test_folder_0 Test_folder_1',
        dest='merge_folder_name', action='store', nargs=3)
    (opts, args) = parser.parse_args()
    try:
        print "***** Welcome to gmailPy!!! A command line GMAIL Client *****"
        print "Please enter your username and password >>>>>>"
        username = raw_input("Username: ")
        password = getpass.getpass()
        ## Can be set for testing and debugging
        # username = 'username'
        # password = 'password'
        client_session = gmailPy()
        client_session.login(username, password)

        if opts.lf:
            client_folders = client_session.get_folders()
            print "########## Your folder Statistics ##########"
            for item in client_folders:
                try:
                    print item, ':', client_session.get_mail_count(item), 'messages'
                except:
                    pass
            print "############################################"

        if opts.big_folder_name != None:
            print "Let's enter your %s folder and delete big mail" % opts.big_folder_name
            client_session.delete_bigmail(opts.big_folder_name)

        available_commands = ['TO', 'FROM', 'SUBJECT']
        if opts.bigsearch_folder_name != None:
            if opts.bigsearch_folder_name[1] in available_commands:
                print "Let's enter your %s folder and delete big mail with %s: %s" % (opts.bigsearch_folder_name[0], opts.bigsearch_folder_name[1], opts.bigsearch_folder_name[2])
                client_session.delete_bigmail_search(
                    opts.bigsearch_folder_name[0], opts.bigsearch_folder_name[1], opts.bigsearch_folder_name[2])
            else:
                print "Invalid Command Entry. Please enter one of the follwing commands: ", available_commands

        if opts.new_folder_name != None:
            print "Creating a new folder with name %s ..." % opts.new_folder_name
            client_session.create_folder(opts.new_folder_name)

        if opts.del_folder_name != None:
            print "Deleting %s folder..." % opts.del_folder_name
            client_session.delete_folder(opts.del_folder_name)

        if opts.rename_folder_name != None:
            print "Renaming folder %s to %s..." % (opts.rename_folder_name[0], opts.rename_folder_name[1])
            client_session.rename_folder(opts.rename_folder_name[0], opts.rename_folder_name[1])

        if opts.merge_folder_name != None:
            print "Merging folders %s and %s to %s..." % (opts.merge_folder_name[1], opts.merge_folder_name[2], opts.merge_folder_name[0])
            client_session.merge_folders(opts.merge_folder_name[0], opts.merge_folder_name[1], opts.merge_folder_name[2])

        client_session.logout()

    except IMAPClient.Error as err:
        print "Something awful happened"
        print err

    except KeyboardInterrupt:
        print "gmailPy force shutdown"
        client_session.logout()

if __name__ == '__main__':
    main()
