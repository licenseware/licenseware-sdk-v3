# Licenseware SDK v3
<img src="./coverage.svg">

# Developing

- clone the repository;
- install virtualenv: `pip3 install virtualenv`;
- create virtualenv: `virtualenv ./`;
- activate virtualenv: `source ./bin/activate`;
- install dependencies: `pip3 install -r requirements.txt`;
- running tests: `make run-tests`;
- install licenseware: `make install`;
- uninstall licenseware: `make uninstall`;
- build licenseware wheel: `make build`;


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
from licenseware import (
    NewUploader, 
    UploaderValidationParameters,
    UploaderEncryptionParameters, 
    FileTypes
)
```
- `NewUploader` - this object will `hold` all the information needed (metadata) for describing file(s) which will be uploaded for processing;
- `UploaderValidationParameters` - this object will contain metadata needed to validate file(s);
- `UploaderEncryptionParameters` - this object will contain metadata needed to encrypt sensitive data from file(s);
- `FileTypes` - this contains all the file types we can process (.xml, .csv, .xlsx etc);

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
    filename_endswith=FileTypes.GENERIC_EXCEL # or just [".xls", ".xlsx"],
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
- `filename_endswith` - at least one of the items in the list must end with `filename.endswith((".xlsx", etc,))`; 
- `required_sheets` - you can put here the required sheets/tabs the excel file needs to have. You can also provide alternative sheets to find like:
`required_sheets=[["sheet1", "sheet2"], ["tab1", "tab2"]]` - this way if at least one of the nested list of sheets has a match validation will succeed;
- `required_columns` - this will look for all columns in all the excel sheets. You can also provide alternative columns just like we did for `required_sheets`;
- `min_rows_number` - the minimum number of rows the excel or csv must have;
- `header_starts_at` - some times header doesn't start from the top, here you can put the index where the header starts;
- `text_contains_all` - this is used for text like files (anything you can open with notepad and understand the text), will check if all items are in the text;
- `text_contains_any` - similar to `text_contains_all`, but will check if at least one item is found in text;
- `ignore_filenames` - here you can put a list of filenames that should not be validated. These files will have status `skipped` in the validation response;
- `buffer` - this sets the ammount of characters that will be loaded in memory for validation (default: 15000). Doing this we avoid loading the whole file in memory which can cause memory overflow; 
- `filename_valid_message` - you can change the message of a file which passed validation (default: "File is valid");
- `filename_ignored_message` - you can change the message of a file which is in `ignore_filenames` field (default: "File is ignored");
- `regex_escape` - the search is done mostly with regex which means that sometimes the text we search can contain regex queries and this may cause an incorect search. To avoid this `regex_escape` is default `True`, but you can change this to `False` if you have a special case;
- `ignored_by_uup` - universal uploader app by default takes all the uploader metadata (uploader details, validation parameters, encryption parameters etc) and checks each file if it fits one specific uploader's metadata. Set `ignored_by_uup` to `False` if you want the uploader created to be ignored by universal uploader app.

Each field is `optional` so we can reduce the above uploader's validation parameters to this:

```py
rv_tools_validation_parameters = UploaderValidationParameters(
    filename_contains=["rv", "tools"],
    filename_endswith=FileTypes.GENERIC_EXCEL,
    required_sheets=["sheet1", "sheet2"],
    required_columns=["col1", "col2"]
)
```


Define uploader full metadata

```py

rv_tools_uploader = NewUploader(
    name="RVTools",
    description="XLSX export from RVTools after scanning your Vmware infrastructure.",
    uploader_id="rv_tools",
    accepted_file_types=FileTypes.GENERIC_EXCEL,
    validation_parameters=rv_tools_validation_parameters,
    encryption_parameters=rv_tools_encryption_parameters,
    filenames_validation_handler=None,
    filecontents_validation_handler=None,
    flags=None,
    icon=None,
    config=config
)

```
In the `NewUploader` object we gather all information about this uploader


- `name` - the name of the uploader (will be displayed by frontend);
- `description` - uploader description (will be displayed by frontend);
- `uploader_id` - this id must be `unique`;
- `accepted_file_types` - the files extentions accepted  (will be displayed by frontend);
- `validation_parameters` - here we pass the instance of `UploaderValidationParameters` class;
- `encryption_parameters` - here we pass the instance of `UploaderEncryptionParameters` class;
- `filenames_validation_handler` - by default the validation is handled by `uploader.defaults.default_filenames_validation_handler` function. If you need to treat the filename validation in a different way you can always pass another function. The `filenames_validation_handler` function will receive the a list of strings as a first parameter and an instance of `UploaderValidationParameters` class and must return an instace of `uiresponses.FileValidationResponse`;
- `filecontents_validation_handler` - by default the validation is handled by `uploader.defaults.default_filecontents_validation_handler` function. If you need to overwrite this functionality you can pass your custom `filecontents_validation_handler` function which will have the same signature as `default_filenames_validation_handler`;
- Obs: for setting the state of the validation you need to use the States `from licenseware States`;
- `flags`- here you can set a list of flags for this uploader. Flags will be imported from `constants` package (`from licenseware import Flags`);
- `icon` - the icon of this uploader which will be displayed in frontend;
- `config` - the configuration class instance will will need to make available the following information:
    * `config.APP_ID` - each service must have an unique ID;
    * `config.REGISTER_UPLOADER_URL` - the url where this uploader will be registered (discovery/registry service);
    * `config.get_machine_token()` - a function which will return the service's authentification token. This token is available after the services authentificates that's way we need a dynamic way of retreiving it;


We can remove the fields we don't fill and reduce the above to this:

```py

rv_tools_uploader = NewUploader(
    name="RVTools",
    description="XLSX export from RVTools after scanning your Vmware infrastructure.",
    uploader_id="rv_tools",
    accepted_file_types=FileTypes.GENERIC_EXCEL,
    validation_parameters=rv_tools_validation_parameters,
    encryption_parameters=rv_tools_encryption_parameters,
    config=config
)

```

This `rv_tools_uploader` instance will make available the following needed methods:
- `validate_filenames` - method which will be used to validate file names received from frontend in the filename validation step;
- `validate_filecontents` - method which will be used to validate file contents received from frontend in the upload files step;
- `metadata` - property which contains all the needed information to register a new uploader to discovery/registry-service;
- `register` - method which will send uploader's metadata to discovery/registry-service;




# Reports

After the `Uploader` validates the files, the files are sent to processing and processed what remains is to provide useful insights by aggregating saved data resulted after processing in small digestable chunks of data.
A report can contain one or more report components. 
Each report component has a corespondent front-end component which `knows` how to render it's data.
The same principles apply as with `Uploaders`.


- Start by importing the report contructors

```py
from config import config
from licenseware import (
    NewReport, 
    NewReportComponent,
    ReportFilter,
    StyleAttrs,
    SummaryAttrs,
    BarHorizontalAttrs,
    Icons
)
```

- Declare a new report

Below we contruct report filters. This step can be done after you have defined all report components.

```py

FMW_FILTERS = (
        ReportFilter()
        .add(
            column="result",
            allowed_filters=[
                ReportFilter.FILTER.EQUALS, 
                ReportFilter.FILTER.CONTAINS, 
                ReportFilter.FILTER.IN_LIST
            ],
            # column_type=ReportFilter.TYPE.STRING, # string type is the default
            allowed_values=["Verify", "Used", "Licensable", "Restricted"],
            # visible_name="Result" # Optional
        )
        .add(
            column="total_number_of_cores",
            allowed_filters=[
                ReportFilter.FILTER.EQUALS, 
                ReportFilter.FILTER.GREATER_THAN, 
                ReportFilter.FILTER.GREATER_OR_EQUAL_TO,
                ReportFilter.FILTER.LESS_THAN,
                ReportFilter.FILTER.LESS_OR_EQUAL_TO
            ],
            column_type=ReportFilter.TYPE.STRING,
            allowed_values=["Verify", "Used", "Licensable", "Restricted"],
        )
    )

```

FMW_FILTERS will be an instance of `ReportFilter` which will make available the list of filters on `metadata` object.


- Declaring the report

Using the `NewReport` class we fill the below parameters (filters can be filled later after you have defined all report components). 

```py

fmw_deployment_report = NewReport(
    name="Oracle Fusion Middleware Deployment",
    report_id="fmw_deployment_report",
    description="Provides overview of Oracle Fusion Middleware deployed components and product bundles.", 
    filters=FMW_FILTERS,
    config=config
)

```
On this instance of the new report we will `attach` all the needed report components. 

This report instance provides the following objects for use:
- `attach` - method which will be used to attach instances of `NewReportComponent`;
- `register` - method which will be used to make a post request with this report data;
- `metadata` - property which contains the json payload for registry service;


- Declaring a new report component

A report can contain one or more report components. Here we declare a `summary` report component type.


- Declaring report component attributes

```py

summary = (
    SummaryAttrs()
    .attr(
        value_key="missing_parent_details", 
        value_description="Missing parent details",
        icon=Icons.FEATURES
    )
    .attr(value_key="unknown_types")
)

```
This way we inform front-end that it needs to use the Summary UI component and it needs to fill the component data as described in `SummaryAttrs`.


- Declaring report component style attributes

```py
styles = (
    StyleAttrs()
    .width_one_third
    .set("height", "full")
)
```
Here we specify additional information to front-end about report component looks.


Next, we need to create a function which based on the parameters received will return component data from database. 

```py

def get_fmw_summary_component_data(*args, **kwargs):
    return "data from database"

```
    
- Declaring the report component


```py
fmw_summary_component = NewReportComponent(
    title="Summary", 
    component_id="fmw_summary", 
    attributes=summary,
    style_attributes=styles,
    get_component_data_handler=get_fmw_summary_component_data,
    config=config
)
```

Now that we have declared report component attributes, style attributes and the `get_component_data_handler` function we are ready to attach it to the report created up.


- Attaching a report component to a report
```py 

fmw_deployment_report.attach(fmw_summary_component)

```

# Datatable

We have `uploaders` which handle files uploaded and sent to procesing, `reports` which take the data processed and show it to the user in a insightful way we also can provide a way for the user to manipulate/update the data processed using `datatable`. With Datatable we can provide `excel like` features on the web.


```py

from licenseware import DataTable, ColumnTypes, CrudHandler


class CrudDeviceTable(CrudHandler): 

    # you can provide some init values if you want

    def get(self, params):
        return params

    def post(self, payload):
        return payload

    def put(self, payload):
        return payload

    def delete(self, payload):
        return payload



devices = DataTable(
    title="Devices", 
    component_id="device_table",
    crud_handler=CrudDeviceTable, # class or instance which inherits from CrudHandler abstract class
    compound_indexes = [["tenant_id", "name"], ["tenant_id", "name", "device_type"]],
    simple_indexes = [
        "_id",
        "tenant_id",
        "name",
        "is_parent_to",
        "cpu_model",
    ]
)

devices.column("_id", editable=False, visible=False)
devices.column("tenant_id", editable=False, visible=False)
devices.column("name", required=True)
devices.column("is_parent_to", distinct_key="name", foreign_key="name")
devices.column("capped", required=True, type=ColumnTypes.BOOL)
devices.column(
    "device_type", 
    required=True, 
    values=["Virtual", "Pool", "Domain", "Physical", "Cluster", "Unknown"]
)
devices.column(
    "operating_system_type", 
    values=["Solaris", "ESX", "Linux", "AIX", "HP-UX", "Windows", "Other"]
)
devices.column("total_number_of_processors", type=ColumnTypes.NUMBER)
devices.column("updated_at", editable=False, type=ColumnTypes.DATE)
devices.column("raw_data", editable=False, type=ColumnTypes.JSON)

```

Class `CrudDeviceTable` is responsible for interacting with the database and providing the data required.
Since the way data is structured can vary from case to case it's up to you to provide the logic. 

Up we declare the table component metadata for `component_id="device_table"`. 
This is very similar to report attributes (ex: `BarHorizontalAttrs`).
Method `column` appends columns to table component. 
Method `column` has the following parameters, most of them with sensible defaults:
- prop: str - this is required, place the name of the field here;
- name: str = None - if not filed, value will be computed from prop;
- values: list = None - provide a list of values, a dropdown will appear in frontend;
- type: ColumnTypes = None - if values is filled type will be automatically set to enum, if distinct_key and foreign_key are filled type will be set automatically to entity, otherwise a default type string will be set. Make sure to specify type for the other types not covered automatically if needed; 
- editable: bool = True - by default all fields are editable (the user can change the field data). If prop is one of "tenant_id", "_id", "updated_at" editable will be set automatically to False.
- visible: bool = True - by default all fields are visible to the user. Same defaults apply as for editable.
- hashable: bool = False - by default all fields are hashable. Same defaults apply as for editable.
- required: bool = False - by default all fields not required. If prop is one of "tenant_id", "_id", "updated_at" editable will be set automatically to True.
- distinct_key:str = None - here place the name of the field from which you want a list of unique items;
- foreign_key:str = None  - here place the name of the foreign key field;

