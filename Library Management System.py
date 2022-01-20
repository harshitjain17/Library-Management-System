'''

Project: Final Project
Collaborators: Rohan Gupta, Harshit Jain, Pranav Bhave, Vansh Koul

'''
import os
os.chdir('C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python39\\FILE HANDLING FILES')


def ReadBooklist():
    """
    Reading the data from the file Booklist and arranging it in a list
    .
    :var file: used to open and hold the file named Booklist.txt
    :var readFile: string containing the data in individual line of Booklist.txt
    :var bookList: list containing all the data in the file Booklist.txt, in formatted manner.
    .
    :return: booklist
    """
    file = open("booklist-2.txt", "r")

    readFile = file.readline().rstrip()

    bookList = []

    while readFile:
        bookList.append(readFile.split("#"))
        readFile = file.readline().rstrip()

    for i in range(len(bookList)):
        bookList[i][1] = int(bookList[i][1])
        if bookList[i][2] == "TRUE":
            bookList[i][2] = True
        else:
            bookList[i][2] = False

    file.close()

    return bookList


def ReadLibraryLog():
    """
    Reading and storing the data from the file librarylog.txt
    .
    :var file: used to open and hold the file named librarylog.txt
    :var readFile: string containing the data in individual line of librarylog.txt
    :var borrowNotation: list of records dealing with books that are borrowed
    :var returnNotation: list of records dealing with books being returned
    :var bookAddition: list of records dealing with new books added to library
    :var finePayNotation: list of records dealing with payment of fine
    .
    :return: borrowNotation, returnNotation, bookAddition, finePayNotation
    """
    file = open("librarylog-3.txt", "r")

    readFile = file.readline().rstrip()

    borrowNotation, returnNotation, bookAddition, finePayNotation = [], [], [], []

    while readFile:
        if readFile[0] == "B":
            borrowNotation.append(readFile[2:len(readFile)].split("#"))
        elif readFile[0] == "R":
            returnNotation.append(readFile[2:len(readFile)].split("#"))
        elif readFile[0] == "A":
            bookAddition.append(readFile[2:len(readFile)].split("#"))
        else:
            finePayNotation.append(readFile[2:len(readFile)].split("#"))

        readFile = file.readline().rstrip()

    file.close()

    for i in range(len(borrowNotation)):
        borrowNotation[i][0] = int(borrowNotation[i][0])
        borrowNotation[i][3] = int(borrowNotation[i][3])
    for i in range(len(returnNotation)):
        returnNotation[i][0] = int(returnNotation[i][0])
    for i in range(len(bookAddition)):
        bookAddition[i][0] = int(bookAddition[i][0])
    for i in range(len(finePayNotation)):
        finePayNotation[i][0] = int(finePayNotation[i][0])
        finePayNotation[i][2] = int(finePayNotation[i][2])

    return borrowNotation, returnNotation, bookAddition, finePayNotation


def canBorrowBook(studentName, currentDay, bookName, borrowingPeriod):
    """
    Calculating whether the given student can borrow the specified book on the perticular day or not
    .
    :var numberOfBooksBorrowed: Integer that reflects the number of books the given student has currently borrowed
    :var bookAvailable: Integer that reflects the number of copies of the given book available
    :var studentRecord: All the data about the books students has currently borrowed but not returned yet
    .
    :param studentName:
    :param currentDay:
    :param bookName:
    .
    :return: A boolean value for whether or not the student can borrow a book
    """
    studentRecord = []

    # Calculating the books that student has ever borrowed
    for i in borrowNotation:
        if i[1] == studentName and i[0] <= currentDay:
            studentRecord.append(i)

    numberOfBooksBorrowed = len(studentRecord)

    # Filtering the books student has borrowed by removing the books that have been returned
    for i in returnNotation:
        if i[1] == studentName:
            for j in range(len(studentRecord)):
                if i[2] == studentRecord[j][2] and i[0] + studentRecord[j][0] <= currentDay:
                    numberOfBooksBorrowed -= 1
                    studentRecord.pop(j)

    # Checking for the number of copies of the book available in the library
    bookAvailable = 0
    for i in bookList:
        if i[0] == bookName:
            bookAvailable += i[1]
    for i in borrowNotation:
        if i[2] == bookName and i[0] < currentDay:
            bookAvailable -= 1
    for i in returnNotation:
        if i[2] == bookName and i[0] < currentDay:
            bookAvailable += 1
    for i in bookAddition:
        if i[1] == bookName and i[0] < currentDay:
            bookAvailable += 1

    # Checking if there is any pending fine on the student
    FineOnStudent = fineCalculator(studentName, currentDay)

    # Checking if book is restricted, so that later it can be checked that for how long can it be borrowed
    for k in bookList:
        if k[0] == bookName:
            if not k[2]:
                restriction = False
            else:
                restriction = True

    if FineOnStudent <= 0 and numberOfBooksBorrowed < 3 and bookAvailable > 0:
        if restriction and borrowingPeriod < 7:
            return True
        elif not restriction and borrowingPeriod < 28:
            return True
        else:
            return False
    else:
        return False


def fineCalculator(studentName, currentDay):
    StudentBorrow = []
    StudentReturn = []

    for borrowRecord in borrowNotation:
        if borrowRecord[1] == studentName:
            StudentBorrow.append(borrowRecord)
    for returnRecord in returnNotation:
        if returnRecord[1] == studentName:
            StudentReturn.append(returnRecord)

    TotalFine = 0

    for bookRecord in StudentBorrow:

        bookName = bookRecord[2]
        borrowDay = bookRecord[0]

        # Checking if the book is restricted
        for book in bookList:
            if book[0] == bookName:
                restriction = book[2]
        for book in bookAddition:
            if book[1] == bookName:
                restriction == False

        Fine = 0

        for i in StudentReturn:
            if i[2] == bookName:
                returnDay = i[0]
                StudentReturn.remove(i)
                break
        else:
            returnDay = currentDay

        # Vars to work with borrowDay, returnDay

        if returnDay - borrowDay > bookRecord[3]:
            if restriction:
                Fine += (returnDay - (borrowDay + bookRecord[3])) * 5
            else:
                Fine += returnDay - (borrowDay + bookRecord[3])

        TotalFine += Fine

    for finePay in finePayNotation:
        if finePay[1] == studentName:
            TotalFine -= finePay[2]

    return TotalFine


# Return the list of all books along with the number of hours they were borrowed for
def bookBorrrowHours(currentDay):
    """
    :var listOfAllBooks: list that contain the names of all books along with the number of hours they were borrowed for
    :var localReturnList: a copy of the returnNotation declared so that data can be deleted from it
    .
    :param currentDay: the day for which these records are to be checked
    .
    :return: listOfAllBooks
    """
    listOfAllBooks = []

    # Assembling a record of all books that are in the library
    for book in bookList:
        listOfAllBooks.append([book[0], 0])

    # To the ListOfAllBooks adding those books that are added to the library later under the A#<date>#<book name>
    # notation
    for book in bookAddition:
        isPresent = False
        for i in listOfAllBooks:
            if i[0] == book[1]:
                isPresent = True
        if not isPresent:
            listOfAllBooks.append([book[1], 0])

    # Calculating that which book was borrowed for how long
    localReturnList = returnNotation[:]
    for i in range(0, len(listOfAllBooks)):
        for book in borrowNotation:
            if book[2] == listOfAllBooks[i][0]:
                for bookReturn in range(0, len(localReturnList)):
                    if localReturnList[bookReturn][2] == book[2]:
                        listOfAllBooks[i][1] += localReturnList[bookReturn][0] - book[0]
                        localReturnList.pop(bookReturn)
                        break
                else:
                    listOfAllBooks[i][1] += currentDay - book[0]

    return listOfAllBooks


# Checking which is the most popular book in the library
def checkBookPopularity(currentDay):
    """
    :var bookHourList: nested list that contains the records of which book was borrowed for how many hours
    :var popularBook: list containing the name of most popular book along with number of hours it was borrowed for
    .
    :param currentDay: The day on which the function should test for the desired result
    .
    :return: popularBook
    """

    bookHourList = bookBorrrowHours(currentDay)

    # Finalizing which book is most popular
    popularBook = ["", 0]
    for i in bookHourList:
        if popularBook[1] < i[1]:
            popularBook = i

    return popularBook


# Checking for how many hours each individual book has existed in the library
def TotalHoursBookExist(currentDay):
    """
    :var AllBooks = list that contains the record of all books along with how many hours have they been in the library
    .
    :param currentDay: The day on which the function should test for the desired result
    .
    :return: AllBooks
    """

    AllBooks = []

    # Adding the books that have existed from start
    for book in bookList:
        # name of book, totalDaysOfExistence
        AllBooks.append([book[0], (currentDay - 1) * book[1]])  # Altered this line to fix the number of days

    # Adding the books that were added later
    for book in bookAddition:
        for addedBook in range(len(AllBooks)):
            if AllBooks[addedBook][0] == book[1] and book[0] < currentDay:
                AllBooks[addedBook][1] += currentDay - book[0]
                break
        else:
            AllBooks.append([book[1], currentDay - book[0]])

    return AllBooks


# Assembles the borrow hours and existence hours to calculate the borrow ratio of each book
def BookBorrowHourRatio(currentDay):
    bookBorrowHour = bookBorrrowHours(currentDay)
    bookExistHour = TotalHoursBookExist(currentDay)

    AllBooks = []

    for book in range(len(bookBorrowHour)):
        AllBooks.append([bookBorrowHour[book][0], 100 * (bookBorrowHour[book][1] / bookExistHour[book][1])])

    return AllBooks


# Returns the name and borrow ratio of book that has the highest borrow ratio
def HighestBorrowRatio(currentDay):
    borrowRatio = BookBorrowHourRatio(currentDay)

    highestBorrowBook = ["", 0]
    for book in borrowRatio:
        if book[1] >= highestBorrowBook[1]:
            highestBorrowBook = book

    return highestBorrowBook


def sortedBorrowRatio(currentDay):
    borrowRatio = BookBorrowHourRatio(currentDay)

    length = len(borrowRatio)
    for i in range(0, length):
        for book in range(0, length - i - 1):
            if borrowRatio[book][1] < borrowRatio[book + 1][1]:
                currentBook = borrowRatio[book]
                borrowRatio[book] = borrowRatio[book + 1]
                borrowRatio[book + 1] = currentBook

    return borrowRatio


bookList, borrowNotation, returnNotation, bookAddition, finePayNotation = "", "", "", "", ""


def main():
    global bookList, borrowNotation, returnNotation, bookAddition, finePayNotation
    bookList = ReadBooklist()
    borrowNotation, returnNotation, bookAddition, finePayNotation = ReadLibraryLog()

    print("Question 1: Can a student borrow a book on a particular day for a certain number of days?")
    print("Question 2: What are the most borrowed / popular books in the library?")
    print("Question 3: Which books has the highest borrow ratio?")
    print("Question 4: Produce a sorted lists of most borrowed books / books with highest usage ratio.")
    print("Question 5: What are the pending fines at the end of the log / at a specific day in the log?\n")

    questionNum = int(input("Please input the number of question you need answered: "))

    if questionNum == 1:
        student = input("Please enter the name of the student: ")
        Day = int(input("Please enter the day on which you want to check: "))
        book = input("Please enter the Book the student wants to borrow: ")
        period = int(input("Please enter the number of days for which the book is to be borrowed: "))

        if canBorrowBook(student, Day, book, period):
            print("\nYou are good to borrow that book")
        else:
            print("\nYou can not borrow that book")

    elif questionNum == 2:
        Day = int(input("Please enter the day on which you want to check: "))
        print("The most popular book on day", Day, "was", checkBookPopularity(Day)[0])

    elif questionNum == 3:
        Day = int(input("Please enter the day on which you want to check: "))
        print("The book with highest borrow ratio is`", HighestBorrowRatio(Day)[0], "`with a borrow ratio of",
              HighestBorrowRatio(Day)[1])

    elif questionNum == 4:
        Day = int(input("Please enter the day on which you want to check: "))
        funkReturn = sortedBorrowRatio(Day)

        for i in funkReturn:
            print(i[0], "  -->  ", i[1])

    elif questionNum == 5:
        print("\nWould you like to check for end of the log or a given day?")
        student = input("Please enter the name of the student: ")
        endOrCurrent = input("e: end of log / c: specific day: ")

        if endOrCurrent == "c":
            Day = int(input("Please enter the day on which you want to check: "))
            print("The Total Pending Fine on day", Day, "is:", fineCalculator(student, Day))
        else:
            file = open("librarylog.txt", "r")
            readFile = file.readline().rstrip()

            Day = int(readFile.split("#")[1])
            while readFile:
                Day = int(readFile.split("#")[1])
                readFile = file.readline().rstrip()

            print("The Total Pending Fine at the end of the log is:", fineCalculator(student, Day))


    else:
        print("\nWe apologies but there are no such function")


main()
