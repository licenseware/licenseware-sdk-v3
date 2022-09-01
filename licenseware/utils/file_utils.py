import os
import shutil
import subprocess

from .logger import log

accepted_archives = (
    ".zip",
    ".tar",
    ".tar.bz2",
    ".tar.gz",
    ".tgz",
    ".tar.xz",
)


def is_archive(filepath: str):  # pragma no cover
    return filepath.endswith(accepted_archives)


def list_files_from_path(dir_path: str):  # pragma no cover
    filepaths = []
    for root, dirs, filenames in os.walk(dir_path):
        for filename in filenames:
            filepaths.append(os.path.join(root, filename))

    return filepaths


def unzip(file_path: str):
    """
    Extracts: “zip”, “tar”, “gztar”, “bztar”, or “xztar”.
    Returns the path where the file was extracted
    """

    if not is_archive(file_path):  # pragma no cover
        raise ValueError(
            f"Invalid archive type, currently accepting: {accepted_archives}"
        )

    file_name = os.path.basename(file_path)
    file_dir = os.path.dirname(file_path)
    extract_path = os.path.join(file_dir, file_name + "_extracted")

    try:
        shutil.unpack_archive(file_path, extract_path)
    except:
        # RUN apt install bzip2
        shutil.rmtree(extract_path)
        os.chmod(file_path, 432)  # 432 is the int representation of the oct 660
        cmd1 = ["mkdir", "-p", extract_path]
        cmd = ["/bin/tar", "-xvf", file_path, "-C", extract_path]
        subprocess.Popen(cmd1)
        error = subprocess.Popen(cmd)
        log.warning(error)
    finally:
        if not os.path.exists(extract_path):
            os.makedirs(extract_path)

    return extract_path


def recursive_unzip(file_path: str):
    """
    Iterate over an archive and recursively extract all archives using unzip function
    """

    if is_archive(file_path):
        unziped_base = unzip(file_path)
        if unziped_base is None:
            return
    else:
        unziped_base = file_path

    archives_found = False
    for root, dirs, filenames in os.walk(unziped_base):
        for filename in filenames:

            fpath = os.path.join(root, filename)

            if not is_archive(fpath):
                continue
            if not os.path.exists(fpath):
                continue

            unzipped_path = unzip(fpath)
            if unzipped_path is None:
                continue

            os.remove(fpath)
            archives_found = True

    file_path = (
        file_path + "_extracted" if not file_path.endswith("_extracted") else file_path
    )

    if archives_found:
        recursive_unzip(file_path)

    return file_path
