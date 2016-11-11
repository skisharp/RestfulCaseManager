import os
from RestfulCaseManager import settings


def cope_files(source_dir, target_dir):
    for file_temp in os.listdir(source_dir):
        source_file = os.path.join(source_dir,  file_temp)
        target_file = os.path.join(target_dir,  file_temp)
        # cope the files
        if os.path.isfile(source_file):
            open(target_file, "wb").write(open(source_file, "rb").read())


# get the case file dir
def get_module_file_dir(module):
    module_package_path = os.path.join(settings.BASE_DIR, 'CaseFiles')
    base_path = os.path.join(module_package_path, module)

    return base_path