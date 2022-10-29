import patoolib

def extract(archive_name):

    patoolib.extract_archive(archive_name, outdir="files")