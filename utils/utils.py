from drf_extra_fields.fields import Base64FileField
import magic


class Base64File(Base64FileField):
    """
    encodes Files as base 64 and checks mime
    """

    ALLOWED_TYPES = ["pdf", "jpg", "jpeg", "png"]

    def get_file_extension(self, filename, decoded_file):
        mime_type = magic.from_buffer(decoded_file, mime=True)

        return mime_type.split("/")[-1]
