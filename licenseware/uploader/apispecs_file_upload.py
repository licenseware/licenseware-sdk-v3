from licenseware.apispec import ApiSpec


specs = ApiSpec(
    title="File Upload", 
    description="Validate filenames, upload files and check quota or status"
)




filename_validation_specs = (
    specs
    .route("/uploads/{uploader_id}/validation")
    

)

