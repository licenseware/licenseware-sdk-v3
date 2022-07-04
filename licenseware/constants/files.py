from dataclasses import dataclass



@dataclass
class files:
    EXCEL: str = ".xls"
    CSV: str = ".csv"
    TXT: str = ".txt"
    XML: str = ".xml"
    GENERIC_EXCEL: str = "generic_excel"
    GENERIC_CSV: str = "generic_csv"
    GENERIC_TEXT: str = "generic_text"
    GENERIC_XML: str = "generic_xml"
    ZIP: str = ".zip"
    TAR: str = ".tar"
    TAR_BZ2: str = ".tar.bz2"
    TAR_GZ: str = ".tar.gz"
    TGZ: str = ".tgz" 
    GENERIC_ARCHIVE : str = "generic_archive"
     