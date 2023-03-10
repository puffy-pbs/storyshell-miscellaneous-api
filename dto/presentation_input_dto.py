from fastapi import UploadFile

from helpers.constants import DEFAULT_PRESENTATION_WIDTH, DEFAULT_PRESENTATION_HEIGHT


class PresentationInputDto:
    """
        PresentationInputDto`s main purpose is to validate and provide an easy-to-use wrapper of the values listed below

        Attributes:
            presentation_file (UploadFile): The file that we should obtain the thumbnails from
            width (int): The desired width of the thumbnail
            height (int): The desired height of the thumbnail

        Raises:
            ValueError
        """
    presentation_file: UploadFile
    width: int
    height: int

    def __init__(self, file, width=None, height=None):
        if not isinstance(file.__class__, UploadFile.__class__):
            raise ValueError("File is not correct")
        self.presentation_file = file

        if width is not None and not isinstance(width, int):
            raise ValueError("Width is not correct")

        self.width = DEFAULT_PRESENTATION_WIDTH
        if width is not None:
            self.width = width

        if height is not None and not isinstance(height, int):
            raise ValueError("Height is not correct")

        self.height = DEFAULT_PRESENTATION_HEIGHT
        if height is not None:
            self.height = height
