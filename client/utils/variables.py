import os

# parent directory
parentDirname = os.path.dirname(os.path.dirname(__file__))

# Local storage variable
storage_filename = "local_storage.data"
storage_file_path = f"{parentDirname}/storage/{storage_filename}"


nb_random_questions = 10