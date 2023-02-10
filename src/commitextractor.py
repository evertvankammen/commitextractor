from datetime import datetime
from pydriller import Repository
from src import db_postgresql, utils
from src.db_postgresql import get_connection

# pip install package pydriller
# pip install package mysql-connector-python
def test_werking():
    # global reponaam, commit_teller, start, connectie, val, projectId
    reponaam = 'https://github.com/chrisadoorn/OUwebclient'
    start = datetime.now()
    utils.log(str(start))
    new_id = 0
    val = (reponaam, 'Java', new_id)
    projectId = db_postgresql.insert_project(val)
    utils.log("project " + reponaam + " inserted with id: " + str(projectId))


# reponaam = 'https://github.com/ishepard/pydriller'
# reponaam = '/git/android/ou-mini-bieb'
# reponaam = '/git/java/nifi'
# test_werking()



# exit(7)
#
# fullRepository = Repository(reponaam)
# commit_teller = 0
# for commit in fullRepository.traverse_commits():
#     commit_teller = commit_teller + 1
#
#     commitcursor = connectie.cursor()
#     commit_datetime = commit.committer_date
#     commitMySqlFormat = commit_datetime.strftime("%Y-%m-%d %H:%M:%S")
#     commit_remark = commit.msg[:200]  # limit the comment
#     sql = "INSERT INTO tests.commit(datum, hashvalue, username, emailadress, remark, idproject) VALUES (%s, %s, %s, %s, %s, %s);"
#     val_commit = (commitMySqlFormat, commit.hash, commit.author.name, commit.author.email, commit_remark, projectId)
#     commitcursor.execute(sql, val_commit)
#     commitId = commitcursor.lastrowid
#     print('commit: ' + str(commit_teller))
#
#     for file in commit.modified_files:
#         print(file.filename, ' has changed')
#         if not (file.filename.endswith('.zip') or file.filename.endswith('.eot') or file.filename.endswith(
#                 '.woff') or file.filename.endswith('interface.saveScore.loadScore.txt')):
#             # sla op in database
#             filecursor = connectie.cursor()
#
#             sql = "INSERT INTO tests.bestandswijziging (tekstvooraf, tekstachteraf, verschil, locatie, idcommit) VALUES (%s, %s, %s, %s, %s)"
#             val = (file.content_before, file.content, file.diff, file.new_path, commitId)
#             filecursor.execute(sql, val)
#             rowId = filecursor.lastrowid
#             connectie.commit()
#
# #          print(filecursor.rowcount, "record inserted with id: " + str(rowId))
#
# print("aantal commits : " + str(commit_teller))
#
# eind = datetime.now()
# print(eind)
# duur = eind - start
# print(duur)
def extract_repository(projectname):
    start = datetime.now()
    utils.log('start verwerking ' + projectname + str(start))
    connectie = db_postgresql.get_conn()

    new_id = 0
    val = (projectname, 'Java', new_id)
    project_id = db_postgresql.insert_project(val)
    utils.log("project " + projectname + " inserted with id: " + str(project_id))

    full_repository = Repository(projectname)
    commit_teller = 0
    for commit in full_repository.traverse_commits():
        commit_teller = commit_teller + 1

        commitcursor = connectie.cursor()
        commit_datetime = commit.committer_date
        commitMySqlFormat = commit_datetime.strftime("%Y-%m-%d")
        commit_remark = commit.msg  # limit the comment commit.msg[:200]
        sql = "INSERT INTO test.commit(commitdatumtijd, hashvalue, username, emailaddress, remark, idproject) VALUES (%s, %s, %s, %s, %s, %s);"
        val_commit = (commitMySqlFormat, commit.hash, commit.author.name, commit.author.email, commit_remark, project_id)
        commitcursor.execute(sql, val_commit)
        commitId = commitcursor.lastrowid
        print('commit: ' + str(commit_teller))

        for file in commit.modified_files:
            # print(file.filename, ' has changed')
            #if not (file.filename.endswith('.zip') or file.filename.endswith('.eot') or file.filename.endswith(
            #       '.woff') or file.filename.endswith('interface.saveScore.loadScore.txt')):
            if file.filename.endswith('.java') or (file.filename == 'pom.xml' and file.new_path == '' and file.old_path == '') :
                # sla op in database
                filecursor = connectie.cursor()

                #sql = "INSERT INTO test.bestandswijziging (tekstvooraf, tekstachteraf, difftext, filename, locatie, idcommit) VALUES (%s, %s, %s, %s, %s, %s)"
                #val = (file.content_before, file.content, file.diff, file.filename, file.new_path, commitId)
                sql = "INSERT INTO test.bestandswijziging ( tekstachteraf, difftext, filename, locatie, idcommit) VALUES (%s, %s, %s, %s, %s)"
                val = (file.content, file.diff, file.filename, file.new_path, commitId)

                filecursor.execute(sql, val)
                rowId = filecursor.lastrowid
                connectie.commit()

    #          print(filecursor.rowcount, "record inserted with id: " + str(rowId))

    print("aantal commits : " + str(commit_teller))

    eind = datetime.now()
    utils.log('einde verwerking ' + projectname + str(eind))
    print(eind)
    duur = eind - start
    utils.log('verwerking ' + projectname + ' duurde ' + str(duur))
    print(duur)
