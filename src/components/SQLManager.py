from components.DatabaseManager import *

def fileToStatements(filePath):
    """ Read an SQL file and split it by its delimiters in single statements """
    data = open(filePath, 'r').readlines()
    stmts = []
    DELIMITER = ';'
    stmt = ''

    for lineno, line in enumerate(data):
        if not line.strip():
            continue
        if line.startswith('--'):
            continue
        if 'DELIMITER' in line:
            DELIMITER = line.split()[1]
            continue
        if (DELIMITER not in line):
            stmt += removeWhitespaces(line.replace(DELIMITER, ';'))
            continue
        if stmt:
            stmt += removeWhitespaces(line)
            stmts.append(stmt.strip())
            stmt = ''
        else:
            stmts.append(line.strip())
    return stmts