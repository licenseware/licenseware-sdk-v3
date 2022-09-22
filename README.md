# Licenseware SDK v3
<img src="./coverage.svg">



# Contents

1. [Developing](#Developing)
2. [Uploaders](#Uploaders)
3. [Reports](#Reports)
4. [Report Components](#Report-Components)
5. [Datatable](#Datatable)
6. [Mongo Repository](#Mongo-Repository)
7. [History](#History)
8. [Kafka Streams](#pubsub) 
9. [Redis Get/Set](#redis) 


<a name="Developing"></a>
# Developing

- clone the repository;
- install virtualenv: `pip3 install virtualenv`;
- create virtualenv: `virtualenv ./`;
- activate virtualenv: `source ./bin/activate`;
- install dependencies: `pip3 install -r requirements.txt`;
- install dependencies: `pip3 install -r requirements-tests.txt`;
- running tests: `make run-tests`;
- install licenseware: `make install`;
- uninstall licenseware: `make uninstall`;
- build licenseware wheel: `make build`;
- install from git: `pip3 install git+https://git@github.com/licenseware/licenseware-sdk-v3.git`; 

<a name="Uploaders"></a>
# Uploaders

An `uploader` is reponsible for handling files uploaded for processing. 
Each uploader will have it's own (mostly) unique attributes and actions. 
These attributes and actions which define an uploader are needed to handle the file from the upload up to file processing handler.

- Create a new uploader

Import uploader constructors
```py
from settings import config
from licenseware import (
    NewUploader, 
    UploaderValidationParameters,
    UploaderEncryptionParameters, 
    FileTypes
)
```
- `config` - this object will contain common data for our application;
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

Creating the worker function which will handle the `event`

```py
from app.dependencies.workers import worker
from licenseware import States, log
from settings import config

from .rv_tools_data_worker import file_workflow_rvtools


@worker.task(name="rv_tools_worker", queue=config.QUEUE)
def rv_tools_worker(event: dict):

    from app.uploaders import registered_uploaders

    log.info("Starting working")
    log.debug(event)

    registered_uploaders.notify_processing_status(
        event["tenant_id"], event["uploader_id"], States.RUNNING
    )

    try:
        for filepath in event["filepaths"]:
            _event = {**{"filepath": filepath}, **event}
            file_workflow_rvtools(
                _event,
                filepath=filepath,
            )
    except:
        registered_uploaders.notify_processing_status(
            event["tenant_id"], event["uploader_id"], States.IDLE
        )

    registered_uploaders.notify_processing_status(
        event["tenant_id"], event["uploader_id"], States.IDLE
    )

    log.info("Finished working")

```

The worker function is responsibile for providing the processing information to you processing class and notify processing status to `registry-service`. 

The `event` received will be a dictionary like this:

```json
event = {
    "tenant_id": tenant_id,
    "authorization": authorization,
    "uploader_id": uploader.uploader_id,
    "filepaths": filepaths,
    "clear_data": clear_data,
    "event_id": event_id or validation_response.content.event_id,
    "app_id": self.config.APP_ID,
}
```
- `tenant_id` - the project id on which this upload was made;
- `authorization` - in some cases you may need to request data from other apps, this will help making those requests on behalf of a user;
- `uploader_id` - this `uploader_id` is unique the same as `app_id`;
- `filepaths` - a list of filepaths which will need to be processed;
- `clear_data` - bool which if is true you must delete previous processed data;
- `event_id` - uuid unique to this processing request;
- `app_id` - the unique app id which holds this uploader;


Define uploader full metadata

```py

from licenseware import FileTypes, NewUploader
from settings import config

from .encryptor import rv_tools_encryption_parameters
from .validator import rv_tools_validation_parameters
from .worker import rv_tools_worker

rv_tools_uploader = NewUploader(
    name="RVTools",
    uploader_id="rv_tools",
    description="XLSX export from RVTools after scanning your Vmware infrastructure.",
    accepted_file_types=FileTypes.GENERIC_EXCEL,
    worker=rv_tools_worker,
    validation_parameters=rv_tools_validation_parameters,
    encryption_parameters=rv_tools_encryption_parameters,
    config=config,
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


Each uploader created needs to be `registered`in the `uploaders/__init__.py` file:

```py

from licenseware import RegisteredUploaders

from app.dependencies.pubsub import producer
from app.services.defaults.registry_updater import registry_updater
from settings import config

from .rv_tools.uploader import rv_tools_uploader

uploaders = [rv_tools_uploader]


registered_uploaders = RegisteredUploaders(
    uploaders, registry_updater, producer, config
)


```

The `registered_uploaders` will be imported on app startup in the `app/api/defaults/uploader_router.py` and will be used to auto generate api routes for each uploader.

If you want more control on how the upload is handled you can inherit from `RegisteredUploaders` and modify the methods you need. Make sure to update `app/api/defaults/uploader_router.py` if method names or params are changed.


<a name="Reports"></a>
# Reports

After the `Uploader` validates the files, the files are sent to processing and processed what remains is to provide useful insights by aggregating saved data resulted after processing in small digestable chunks of data.
A report can contain one or more report components. 
Each report component has a corespondent front-end component which `knows` how to render it's data.
The same principles apply as with `Uploaders`.


- Start by importing the report contructors

```py
from settings import config
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

report_filters = (
        ReportFilter()
        .add(
            column="result",
            allowed_filters=[
                ReportFilter.FILTER.EQUALS,
                ReportFilter.FILTER.CONTAINS,
                ReportFilter.FILTER.IN_LIST,
            ],
            allowed_values=["Verify", "Used", "Licensable", "Restricted"],
        )
        .add(
            column="total_number_of_cores",
            allowed_filters=[
                ReportFilter.FILTER.EQUALS,
                ReportFilter.FILTER.GREATER_THAN,
                ReportFilter.FILTER.GREATER_OR_EQUAL_TO,
                ReportFilter.FILTER.LESS_THAN,
                ReportFilter.FILTER.LESS_OR_EQUAL_TO,
            ],
            column_type=ReportFilter.TYPE.STRING,
            allowed_values=["Verify", "Used", "Licensable", "Restricted"],
        )
        .add(
            column="total_number_of_cores_intel",
            allowed_values=["Verify", "Used", "Licensable", "Restricted"],
        )
    )

```

Variable `report_filters` will be an instance of `ReportFilter` which will make available the list of filters on `metadata` object.
For each column type if `allowed_filters` parameter is not filled the default filters for that column type will be added.
If `column_type` is not specified either, then `ReportFilter` will try to detect the type based on the other parameters.
You can take a look on the `ReportFilter` implementation to see how the defaults are applied. 
In most cases you can get away by just providing the column name and allowed_values if needed.



- Declaring the report

Using the `NewReport` class we fill the below parameters (filters can be filled later after you have defined all report components). 

```py

from app.report_components import report_components
from licenseware import NewReport
from settings import config

from .filters import report_filters

devices_overview_report = NewReport(
    name="Device Details",
    description="This report collects all the device information captured during processing.",
    report_id="device_details_report",
    filters=report_filters,
    components=report_components,
    config=config,
    connected_apps=[
        "ifmp-service",
        "odb-service",
    ],
)


devices_overview_report.attach(component_id="all_devices")


```

- `connected_apps` - here provide app_id's on which this report depends. Data will be taken from both connected_apps to create the reports.


On this instance of the new report we will `attach` all the needed report components. 
If `attach` is not used all provided `report_components` will be attached.

You can create custom filters on which report components you need to attach:

```py

for rc in report_components:
    if rc.component_id in ["some_component_id1", "some_component_id2"]:
        devices_overview_report.attach(rc.component_id)

```

Each report created needs to be `registered`in the `reports/__init__.py` file:

```py
from settings import config
from licenseware import RegisteredReports

from .device_details.report import devices_overview_report

reports = [devices_overview_report]


registered_reports = RegisteredReports(reports, config)

```

The `registered_reports` will be imported on app startup in the `app/api/defaults/*_report_router.py` and will be used to auto generate api routes for each report.

If you want more control on how the reports are handled you can inherit from `RegisteredReports` and modify the methods you need. Make sure to update `app/api/defaults/*_report_router.py` if method names or params are changed.


<a name="Report-Components"></a>
# Report Components 

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


Each report component created needs to be `registered`in the `report_components/__init__.py` file:

```py
from settings import config
from licenseware import RegisteredComponents

from .all_devices.component import all_devices_component

report_components = [all_devices_component]


registered_components = RegisteredComponents(report_components, config)

```


The `registered_components` will be imported on app startup in the `app/api/defaults/*_report_component_router.py` and will be used to auto generate api routes for each report component.

If you want more control on how the report components are handled you can inherit from `RegisteredComponents` and modify the methods you need. Make sure to update `app/api/defaults/*_report_component_router.py` if method names or params are changed.


<a name="Datatable"></a>
# Datatable

We have `uploaders` which handle files uploaded and sent to procesing, `reports` which take the data processed and show it to the user in a insightful way we also can provide a way for the user to manipulate/update the data processed using `datatable`. With Datatable we can provide `excel like` features on the web.


Ovewrite the `CrudHandler` methods if needed (in most cases you hopefully don't need to do that):

```py
from .crud_handler import CrudDeviceTable

from app.common.infrastructure_service import InfraService
from licenseware import (
    Config,
    CrudHandler,
    MongoRepository,
    insert_mongo_limit_skip_filters,
)
from settings import config


def get_data_without_foreign_key(
    tenant_id: str,
    repo: MongoRepository,
    limit: int,
    skip: int,
    config: Config,
):

    pipeline = [
        {"$match": {"tenant_id": tenant_id}},
        {
            "$lookup": {
                "from": config.MONGO_COLLECTION.DATA,
                "localField": "is_dr_with",
                "foreignField": "_id",
                "as": "dr_members",
            }
        },
        {
            "$project": {
                "_id": 1,
                "is_child_to": {
                    "$ifNull": [{"$arrayElemAt": ["$parents.name", 0]}, None]
                },
                "is_parent_to": "$children.name",
                "is_dr_with": "$dr_members.name",
                "is_part_of_cluster_with": "$cluster_members.name",
                "capped": 1,
            }
        },
    ]

    pipeline = insert_mongo_limit_skip_filters(skip, limit, pipeline)
    return repo.execute_query(pipeline)


class CrudDeviceTable(CrudHandler):
    def get(
        self,
        tenant_id: str,
        authorization: str,
        id: str,
        foreign_key: str,
        distinct_key: str,
        limit: int,
        skip: int,
        repo: MongoRepository,
    ):

        if id is not None:
            return repo.find_one(filters={"_id": id, "tenant_id": tenant_id})

        if foreign_key is None:
            return get_data_without_foreign_key(tenant_id, repo, limit, skip, config)

        if distinct_key is not None:
            return repo.distinct(distinct_key, filters={"tenant_id": tenant_id})

        return repo.find_many(filters={"tenant_id": tenant_id}, limit=limit, skip=skip)

    def put(
        self,
        tenant_id: str,
        authorization: str,
        id: str,
        new_data: dict,
        repo: MongoRepository,
    ):

        id = new_data.pop("_id", None)
        infra_service = InfraService(
            data={**new_data, **{"tenant_id": tenant_id}},
            event={
                "tenant_id": tenant_id,
                "uploader_id": "editable_controller",
                "event_id": id,
                "filepath": "N/A",
                "app_id": config.APP_ID,
            },
            collection=repo.collection,
        )
        return infra_service.replace()

    def delete(
        self,
        tenant_id: str,
        authorization: str,
        id: str,
        repo: MongoRepository,
    ):
        return repo.delete_one(filters={"_id": id, "tenant_id": tenant_id})


```

Define data table:

```py
from settings import config
from licenseware import DataTable, ColumnTypes, CrudHandler
from licenseware import ColumnTypes, DataTable
from settings import config

devices_table = (
    DataTable(
        title="All Devices",
        component_id="device_table",
        crud_handler=CrudDeviceTable, # not needed if you didn't overwrite CrudHandler class
        config=config,
    )
    .column("_id", editable=False, visible=False)
    .column("tenant_id", editable=False, visible=False)
    .column("name", required=True)
    .column("is_parent_to", distinct_key="name", foreign_key="name")
    .column("capped", type=ColumnTypes.BOOL)
    .column("device_type", values=["Virtual", "Pool",])
    .column("total_number_of_processors") # this will be type number because it has number in the field name
    .column("oracle_core_factor", type=ColumnTypes.NUMBER)
    .column("model") # default will be type string
    .column("updated_at", editable=False, type=ColumnTypes.DATE)
    .column("raw_data", editable=False, type=ColumnTypes.JSON)
)

```

Class `CrudDeviceTable` is responsible for interacting with the database and providing the data required.

Up we declare the table component metadata for `component_id="device_table"`. 
This is very similar to report attributes (ex: `BarHorizontalAttrs`).
Method `column` appends columns to table component. 
Method `column` has the following parameters, most of them with sensible defaults:
- `prop`: str - this is required, place the name of the field here;
- `name`: str = None - if not filed, value will be computed from prop;
- `values`: list = None - provide a list of values, a dropdown will appear in frontend;
- `type`: ColumnTypes = None - if values is filled type will be automatically set to enum, if distinct_key and foreign_key are filled type will be set automatically to entity, otherwise a default type string will be set. Make sure to specify type for the other types not covered automatically if needed; 
- `editable`: bool = True - by default all fields are editable (the user can change the field data). If prop is one of "tenant_id", "_id", "updated_at" editable will be set automatically to False.
- `visible`: bool = True - by default all fields are visible to the user. Same defaults apply as for editable.
- `hashable`: bool = False - by default all fields are hashable. Same defaults apply as for editable.
- `required`: bool = False - by default all fields not required. If prop is one of "tenant_id", "_id", "updated_at" editable will be set automatically to True.
- `distinct_key`:str = None - here place the name of the field from which you want a list of unique items;
- `foreign_key`:str = None  - here place the name of the foreign key field;


Each datatable component created needs to be `registered`in the `datatables/__init__.py` file:

```py
from licenseware import RegisteredDataTables
from settings import config

from .devices_table import devices_table
from .devices_table_simple import devices_table_simple

datatables = [devices_table, devices_table_simple]

registered_datatables = RegisteredDataTables(datatables, config)

```

The `registered_datatables` will be imported on app startup in the `app/api/defaults/datatables_router.py` and will be used to auto generate api routes for each report datatable.


<a name="Mongo-Repository"></a>
# Mongo Repository

The data to be useful needs to be saved somewhere that's where the `MongoRepository` class comes in handy.
It includes handling of mongo `ObjectId` field which is not json parsable + some custom handling.

First import the repo implementation:
```py

from marshmallow import Schema, fields
from settings import config
from licenseware import MongoRepository
from app.dependencies.db.mongo import get_mongo_db_connection


class EntitiesSchema(Schema):
    entities = fields.List(fields.Raw, required=True)


def entities_validator(data):
    data = EntitiesSchema(many=True if isinstance(data, list) else False).load(data)
    return data


class SomeProcessingClass:

    def __init__(self):
        # Attention! 
        # Don't keep it at the module level as a global variable!
        mongo_connection = get_mongo_db_connection(config)
        self.repo = MongoRepository(
            mongo_connection, 
            collection = config.MONGO_COLLECTION.DATA,
            data_validator = entities_validator
        )
        # Now the `repo` is ready to use!

    def some_func(self):
        
        inserted_data = repo.insert_one(
            data={"field_name": "some_data"}
        )

```

The `data_validator` (entities_validator) needs to be a function which will `raise` an error if data is not as requested.
You can use any schema package you want marshmallow, pydantic even your own custom assertion on data it just needs to raise an error if data is not as intended.

The `data_validator` validator needs to return the data provided. 

We specified the `collection` and `data_validator` function on instantiation, but we can provide other collection names or validators on the repo method parameters (not recommended).

Insert some special data:
```py

def custom_validator(data):
    assert "field_name" in data.keys()
    assert data["field_name"] in ["some_special_data"]  
    return data

# somewhere in a class method

inserted_data = self.repo.insert_one(
    data={"field_name": "some_special_data"}
    collection="SpecialCollection",
    data_validator=custom_validator
)

```

Ideally you should create one repo per collection because this way you don't need to specify collection and data_validator each time you call a repo method.

The `data_validator` can be set to `None` while figuring out what to do with the data, but you will see a warning that the data inserted/updated/replaced has no validation. So, make sure you provide a `data_validator` function once you are ready. If you really don't need a data validator you could set `data_validator="ignore"` this will bypass the data validation step (use it with care).

Note that you could always create a new repo collection based on an existing created repo.

```py

repo_data = MongoRepository(
    mongo_connection, 
    collection = config.MONGO_COLLECTION.DATA,
    data_validator = entities_validator
)

# later in the process you need another collection

repo_newcollection = MongoRepository(
    repo_data.db_connection, 
    collection = "CustomCollection",
    data_validator = "ignore"
)

```

If you need to create indexes or other extra configurations please create them on app startup (main.py file).

Checkout `licenseware/repository/mongo_repository` for more information.


<a name="History"></a>
# History

In order to have a history of the processing steps from begining to the end `licenseware.history.log` decorator can be used to decorate processing functions.

Below is an basic usage example:

```py

from settings import config
from app.dependencies.db.mongo import get_mongo_db_connection
from licenseware import MongoRepository

class InfraService:
    def __init__(self):
        self.event_id = str(uuid.uuid4())
        self.filepath = "./somefile"
        self.uploader_id = "rv_rools"
        self.app_id = "ifmp-service"
        self.tenant_id = str(uuid.uuid4())
        mongo_connection = get_mongo_db_connection(config)
        self.repo = MongoRepository(
            mongo_connection, collection=config.MONGO_COLLECTION.DATA
        )
        self.config = config

    @history.log
    def update_relationships(self):
        """some docs"""
        print("working")
        print("done")

response = InfraService().update_relationships()

```

For history to work we need some basic information (event from worker information + the config from settings) to track the processing steps:
- `event_id` 
- `filepath` 
- `uploader_id` 
- `app_id` 
- `tenant_id` 
- `repo`
- `config`

Where the `history.log` decorator cannot be used you can create an instance of `History` class and call the following functions where needed:

- `log_filename_validation` - if you are overwriting the default file names validation function;
- `log_filecontent_validation` - - if you are overwriting the default file content validation function;
- `log_success` - place it where function completed succesfully;
- `log_failure` - place it where function failed to complete, an error occured;

A basic example:

```py

import traceback
from settings import config
from app.dependencies.db.mongo import get_mongo_db_connection
from licenseware import History


class ProcessingClass:
    def __init__(self, tenant_id, authorization, event_id, uploader_id, app_id):
        mongo_connection = get_mongo_db_connection(config)

        history_repo = MongoRepository(
            mongo_connection, collection=config.MONGO_COLLECTION.HISTORY
        )
        self.history = History(
            # etc fill needed params to History class
        )


    def some_processing_func(self, filepath: str):

        try:
            # processing stuff
            self.history.log_success(
                step="some_processing_func",
                filepath="./somecsv.csv",
                on_success_save=None,
                func_source="app/some_package/some_module/some_processing_func",
            )
        except Exception as err:
            self.history.log_failure(
                step="some_processing_func",
                filepath=filepath,
                error_string=str(err),
                traceback_string=str(traceback.format_exc()),
                on_failure_save="Faled gathering data",
                func_source="app/some_package/some_module/some_processing_func",
            )

```

As you can see this method is very verbose an ugly this is what `history.log` decorator does under the hood.
I takes the required parameters and saves success and failures in encountered in a processing pipeline. 

Checkout `licenseware/repository/history` for more information.


<a name="pubsub"></a>
# Kafka Streams (Pub-Sub)

Basic usage:

On the kafka broker side define topics(channels)

```py

from licensware import Topic, TopicType
from confluent_kafka.admin import AdminClient

admin_client = AdminClient({'bootstrap.servers': 'mybroker'})

topic = Topic(admin_client)

topic.new(TopicType.USER_EVENTS)
topic.new(TopicType.APP_EVENTS)

topic.delete(TopicType.APP_EVENTS)


```

On the app side define stream producer (publisher)

```py
from licenseware import Config, Producer
from confluent_kafka import Producer as KafkaProducer
from settings import config 

def get_producer(config: Config):
    producer_client_factory = lambda cfg: KafkaProducer(
        {
            "bootstrap.servers": cfg.KAFKA_BROKER_URL,
            "security.protocol": cfg.KAFKA_SECURITY_PROTOCOL,
        }
    )
    kafka_producer = Producer(producer_client_factory, config)
    return kafka_producer

producer = get_producer(config)

data_stream = {
    "event_type": EventType.ACCOUNT_CREATED,
    "tenant_id": None,
    "etc": "data",
}

producer.publish(TopicType.USER_EVENTS, data_stream)

```
The factory function is up to you to create it with the configurations you need.
We are using a factory function for getting the confluent kafka producer to reconnect in case the connection fails.


You can also define a consumer (subscriber)

```py
from licenseware import Config, Consumer
from confluent_kafka import Consumer as KafkaConsumer
from settings import config


def get_consumer(config: Config):
    consumer_client_factory = lambda cfg: KafkaConsumer(
        {
            "bootstrap.servers": cfg.KAFKA_BROKER_URL,
            "group.id": cfg.APP_ID,
            "security.protocol": cfg.KAFKA_SECURITY_PROTOCOL,
        }
    )
    kafka_consumer = Consumer(consumer_client_factory, config)
    return kafka_consumer


consumer = get_consumer(config)

consumer.subscribe(TopicType.USER_EVENTS)


def account_created_handler(event):
    return "some processed data"


consumer.dispatch(EventType.ACCOUNT_CREATED, account_created_handler)


if __name__ == "__main__":
    consumer.listen()

```
The factory function is up to you to create it with the configurations you need.
We are using a factory function for getting the confluent kafka consumer to reconnect in case the connection fails.




<a name="redis"></a>
# Redis Get/Set

For various reasons we may need to set and get small temporary chunks of data from redis.


```py
from settings import config
from licenseware import RedisCache


rc = RedisCache(config)

# expiry in seconds - put None for no expire date
rc.set(key="apps:ifmp-service", value={"app": {"app_id": "ifmp-service"}}, expiry=10)
rc.set(key="apps:odb-service", value={"app": {"app_id": "odb-service"}}, expiry=10)

# get will return a list of matched keys results
rc.get("apps:*")
rc.get("apps:odb-service")

# get key will return the value stored on that specific key
rc.get_key("apps:odb-service")

```