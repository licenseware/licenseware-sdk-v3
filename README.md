# Licenseware SDK v3
<img src="./coverage.svg">

# Developing

- clone the repository;
- install virtualenv: `pip3 install virtualenv`;
- create virtualenv: `virtualenv ./`;
- activate virtualenv: `source ./bin/activate`;
- install dependencies: `pip3 install -r requirements.txt`;
- running tests: `make run-tests`;
- install lestest wheel: `make install`;
- uninstall lestest: `make uninstall`;
- build lestest wheel: `make build`;


# Uploaders

An `uploader` is reponsible for handling files uploaded for processing. 
Each uploader will have it's own (mostly) unique attributes and actions. 
These attributes and actions which define an uploader are needed to handle the file from the upload up to file processing handler.

## How to create a new uploader

Import configuration
```py
from config import config
```
The `config` object will contain common data for our application.
Data like:
- the app id;
- url to register uploader;
etc  


Import uploader constructors
```py
from licenseware.uploader import (
    NewUploader, 
    UploaderValidationParameters,
    UploaderEncryptionParameters, 
)
```
- `NewUploader` - this object will `hold` all the information needed (metadata) for describing file(s) which will be uploaded for processing;
- `UploaderValidationParameters` - this object will contain metadata needed to validate file(s);
- `UploaderEncryptionParameters` - this object will contain metadata needed to encrypt sensitive data from file(s);

This list can grow depending on the requirements.

Define uploader encryption parameters
```py
rv_tools_encryption_parameters = UploaderEncryptionParameters(
    filepaths=["DeviceX", "encrypt_this(.*)_untilhere"],
    filecontent=["MachineName=(.*?)"],
    columns=["Device", "Host"]
)
```

Data provided on `UploaderEncryptionParameters` will be used in data anonymization app for encrypting sensitive data locally before sending the date for processing.

- `filepaths` - this will encrypt all files and folders which match the given parameters;
- `filecontent` - this will encrypt all text like content that matched (`.txt`, `.xml`) in the same way `filepaths` does;
- `columns` - this will encrypt all columns from the `.xlsx`, `.xls` or `.csv` given;

This is how the encryption will take place for `filepaths` and `filecontent`:
- Given "DeviceX" will encrypt in filepath anywhere it finds "DeviceX" like: `/path/to/DeviceX` to `/path/to/slkjl9e`;  
- Given "Device-(.+?)" will encrypt in filepath anywhere it finds regex match like: `/path/to/Device-SecretName` to `/path/to/Device-dasdia3i`;  

This is how the encryption will take place for `columns`:
- Given the list of columns will encrypt all values;
- Parameters can be given just as we did for `filepaths` and `filecontent` it can be either exact match `SpecificDeviceX` or regex match `SpecificDevice(.+?)`. The regex match will encrypt what it found between paranthesis. 

If no encryption is needed don't provide any parameters this would be enough:
```py
rv_tools_encryption_parameters = UploaderEncryptionParameters()
``` 
If you need to encrypt only the columns:
```py
rv_tools_encryption_parameters = UploaderEncryptionParameters(
    columns=["Device", "Host"]
)
``` 
In a similar way this can be done for `filepaths` and `filecontent`.


Define uploader validation parameters
```py

rv_tools_validation_parameters = UploaderValidationParameters(
    required_input_type="excel",
    filename_contains=["rv", "tools"],
    filename_endswith=[".xls", ".xlsx"],
    required_sheets=["sheet1", "sheet2"],
    required_columns=["col1", "col2"],
    min_rows_number=1,
    header_starts_at=0,
    text_contains_all=None,
    text_contains_any=None,
    ignore_filenames=None,
    buffer=15000,
    filename_valid_message="File is valid",
    filename_ignored_message="File is ignored",
    regex_escape=True,
    ignored_by_uup=False
)

```
These are all needed validation parameters, these may seem like a lot, but you'll only use one or two parameters per uploader.

- `required_input_type` - this describes the type of file uploaded. Put the file extension like `.xlsx`, `.xlsx` (or `excel`), `.csv`, `.xml` etc;
- `filename_contains` - at least one of the items in the list must be on the filename; 
- `filename_endswith` - at least one of the items in the list must end with `filename.endswith((etc,))`; 
- `required_sheets` - you can put here the required sheets/tabs the excel file needs to have. You can also provide alternative sheets to find like:
`required_sheets=[["sheet1", "sheet2"], ["tab1", "tab2"]]` - this way if at least one of the nested list of sheets has a match validation will succeed;
- `required_columns` - this will look for all columns in all the excel sheets. You can also provide alternative columns just like we did for `required_sheets`;
- `min_rows_number` - the minimum number of rows the excel or csv must have;
- `header_starts_at` - some times header doesn't start from the top, here you can put the index where the header starts;
- `text_contains_all` - this is used for text like files (anything you can open with notepad and understand the text), will check if all items are in the text;
- `text_contains_any` - similar to `text_contains_all`, but will check if at least one item is found in text;


TODO - continue docs

ignore_filenames=None
buffer=15000
filename_valid_message="File is valid"
filename_ignored_message="File is ignored"
regex_escape=True
ignored_by_uup=False









```py






rv_tools_validation_parameters = UploaderValidationParameters(
    required_input_type="excel",
    filename_contains=["rv", "tools"],
    filename_endswith=[".xls", ".xlsx"]
    required_sheets=["sheet1", "sheet2"]
    required_columns=["col1", "col2"]
    min_rows_number=1,
    header_starts_at=0,
    text_contains_all=None
    text_contains_any=None
    ignore_filenames=None
    buffer=15000
    filename_valid_message="File is valid"
    filename_ignored_message="File is ignored"
    regex_escape=True
    ignored_by_uup=False
)

rv_tools_uploader = NewUploader(
    name="RVTools",
    description="XLSX export from RVTools after scanning your Vmware infrastructure.",
    uploader_id="rv_tools",
    accepted_file_types=[".xls", ".xlsx"],
    validation_parameters=rv_tools_validation_parameters,
    encryption_parameters=rv_tools_encryption_parameters,
    filenames_validation_handler=None,
    filecontents_validation_handler=None,
    flags=None,
    status=None,
    icon=None,
    config=config
)




```