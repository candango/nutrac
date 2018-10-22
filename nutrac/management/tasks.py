from firenado.management import ManagementTask
from firenado.util import file as _file
from firenado.util.sqlalchemy_util import Session, run_script
import logging
import os
from six import moves
from sqlalchemy import create_engine

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

        conn_string = "%s://%s:%s@%s:%s/%s" % (
            "postgresql+psycopg2",
            namespace.user,
            namespace.password,
            namespace.host,
            namespace.port,
            namespace.database
        )

        engine = create_engine(conn_string)

        engine.connect()

        Session.configure(bind=engine)
        session = Session()

        db_script_path = os.path.realpath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "scripts",
                "pgsql",
                "public.sql"
            )
        )

        def fix_command(sql_command):
            return sql_command.replace("<NUTRAC_USER>", namespace.user)

        run_script(db_script_path, session, handle_command=fix_command)


        logger.info("Creating the NuTrac database.")
