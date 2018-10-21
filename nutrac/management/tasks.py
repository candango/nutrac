from firenado.management import ManagementTask
from firenado.util import file as _file, sqlalchemy_util
import logging
import os
from six import moves

logger = logging.getLogger(__name__)


class NutacCreateDatabaseTask(ManagementTask):

    def add_arguments(self, parser):
        parser.add_argument("-d", "--database", default="nutrac")
        parser.add_argument("-H", "--host", default="localhost")
        parser.add_argument("-p", "--password")
        parser.add_argument("-P", "--port", default=5432, type=int)
        parser.add_argument("-u", "--user", default="nutrac")

    def run(self, namespace):
        """ Create the database
        """
        password = None
        if namespace.password is None:
            password = moves.input("Inform the database password:")
        else:
            password = namespace.password
        print(namespace)
        exit(2)

        db_script_path = os.path.realpath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "scripts",
                "pgsql",
                "public.sql"
            )
        )
        public_script_path = _file.read(db_script_path).replace(
            "<INTRAC_USER>", "intracuser")
        sqlalchemy_util.run_script(public_script_path)

        logger.info("Creating the NuTrac database.")
