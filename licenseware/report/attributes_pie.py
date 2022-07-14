from dataclasses import dataclass
from licenseware.utils.alter_string import get_altered_strings



@dataclass
class PieAttrs:
    label_key: str
    value_key: str
    label_description: str = None
    value_description: str = None

    def __post_init__(self):

        if self.label_description is None:
            altstr = get_altered_strings(self.label_key)
            self.label_description = altstr.title

        if self.value_description is None:
            altstr = get_altered_strings(self.value_key)
            self.value_description = altstr.title


    def dict(self):
        return {
            "series": [
                {
                    "label_key": self.label_key,
                    "label_description": self.label_description, 
                },
                {
                    "value_key": self.value_key,
                    "value_description": self.value_description,
                },
            ]
        }



"""
PIE SAMPLE

{
    "series": [
        {"label_description": "WebLogic Edition", "label_key": "product_name"},
        {
            "value_description": "Number of Devices",
            "value_key": "number_of_devices",
        },
    ]
}
"""
