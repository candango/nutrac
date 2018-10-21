from firenado.management import ManagementTask
from firenado.util import file as _file
import logging
import os
from sqlalchemy import text

logger = logging.getLogger(__name__)


class NutacCreateDatabaseTask(ManagementTask):
    """ Create the database
    """
    def run(self, namespace):
        print(namespace)

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
        print(public_script_path)
        logger.info("Creating the NuTrac database.")

