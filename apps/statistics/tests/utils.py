from django.core.files.uploadedfile import SimpleUploadedFile


def file_upload_csv(file_path: str):
    data = open(file_path, "rb")
    data = SimpleUploadedFile(content=data.read(), name=data.name, content_type="multipart/form-data")

    return data
