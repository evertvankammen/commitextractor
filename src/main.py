from src import utils, sanitychecker, db_postgresql, hashing, commitextractor
import uuid

# initialiseer logging
instance_uuid = str(uuid.uuid4())
utils.open_logfile(instance_uuid)
utils.log('Starting application commitextractor with procesid ' + instance_uuid)


#####################################
#         define functions          #
#####################################

def start_processing():
    # start_processing()
    # while there projects to analyze,
    # extract data from repositories
    try:
        # connect to database
        db_postgresql.open_connection()
        # commitextractor.test_werking()
        # projectname = db_postgresql.get_next_project('')
        # while projectname:
        projectname = '/git/java/nifi'
        commitextractor.extract_repository(projectname)
        # projectname = db_postgresql.get_next_project(projectname)

        #
    finally:
        utils.log('Cleaning up')


def start_with_checks():
    # start_with_checks()
    # check if the environment is in proper order
    # abort gracefully if it is not
    # if all is well start processing
    try:

        # cache seed value
        hashing.set_seed()
        # check if environment is configured properly
        sane = sanitychecker.check_dependencies()
        if not sane:
            utils.log('Er zijn fouten geconstateerd tijdens de initialisatie. Het programma wordt afgebroken.')
            raise Exception('Er zijn fouten geconstateerd tijdens de initialisatie. Het programma wordt afgebroken.')

        start_processing()

    finally:
        utils.log('Stopping application commitextractor')
        utils.close_logfile()


#####################################
#         start of code             #
#####################################
start_with_checks()