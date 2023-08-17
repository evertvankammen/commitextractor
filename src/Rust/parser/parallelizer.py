import logging
import multiprocessing as mp
import os
import uuid
from datetime import datetime

from src.Rust.parser import rustParser
from src.utils import configurator


# rust_parser starts in a new process.
# Therefore, it needs a new logging file.
def _start_rust_parser(nummer=0):
    process_identifier = str(uuid.uuid4())
    dt = datetime.now()
    filename = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                             '../../../../../../../..', 'log',
                                             'processor.' + dt.strftime(
                                                 '%y%m%d-%H%M%S') + '.' + process_identifier + '.log'))
    logging.basicConfig(filename=filename,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.INFO, encoding='utf-8')
    logging.info(f'start process {str(nummer)}  with id: {process_identifier}')
    rustParser.parse_fulltext(process_identifier)


# start_processen is the entry point for parallelizer
# it starts a configurable number of processes
def start_rust_parser_processen():
    number_of_processes = configurator.get_number_of_processes("diff_analyzer")
    logging.info(f"Number of (virtual) processors on this machine: {str(mp.cpu_count())}")
    logging.info(f'Starting {str(number_of_processes)} processes')
    mp.Pool()
    pool = mp.Pool(number_of_processes)
    pool.map(_start_rust_parser, range(number_of_processes))
    pool.close()
