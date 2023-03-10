import os
import random
import shutil

import aiofiles
from fastapi import UploadFile


def generate_save_filename(filename: str) -> str:
    """
    Generate random filename
    Args:
        filename (str): The filename of the file on the fs

    Returns:
        str: The filename
    """
    filename, extension = os.path.splitext(filename)
    rnd = random.randint(100, 100000)
    return "uploads/" + filename + str(rnd) + extension


async def save_uploaded_file(output_filename: str, file: UploadFile) -> None:
    """
    Save uploaded file
    Args:
        output_filename (str): Desired filename
        file (UploadFile): The file itself
    """
    async with aiofiles.open(output_filename, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)


def generate_thumbnails(filename: str, width: int, height: int) -> str:
    """
    Generate thumbnails from presentation file
    Args:
        filename (str): Source filename
        width (int): Desired width of the converted images
        height (int): Desired height of the converted images
    """

    # Thumbnails destination folder
    thumbnails_folder = "thumbnail_{rnd}_{rnd2}".format(rnd=random.randint(100, 100000), rnd2=random.randint(1, 50000))
    os.mkdir(thumbnails_folder)
    if not os.path.exists(thumbnails_folder):
        raise OSError("Error in creating the converted images directory!")

    # Convert ppt to pdf
    convert_ppt_to_pdf(filename)

    # Generate the pdf filename
    pdf_filename, extension = os.path.splitext(filename)
    pdf_filename += ".pdf"

    # Convert the pdf to images
    convert_pdf_to_images(pdf_filename, width, height, thumbnails_folder)
    if not os.listdir(thumbnails_folder):
        raise OSError("Converted images directory is empty!")

    # Create zip file from the generated thumbnails
    zip_file = shutil.make_archive("zip/{dir}".format(dir=thumbnails_folder), "zip", thumbnails_folder)

    # Cleanup time
    cleanup_after_thumbnail_generation(thumbnails_folder, filename, pdf_filename)

    return zip_file


def convert_ppt_to_pdf(filename: str) -> int:
    """
    Convert presentation file to a pdf using soffice
    Args:
        filename (str): Source filename
    Returns:
        int - The result of the conversion
    """
    return os.system(
        "soffice --convert-to pdf {source} "  # convert to pdf
        "--outdir uploads "  # destination folder
        "--headless "  # like invisible but no user interaction at all
        "--invisible "  # no startup screen, no default document and no UI
        "--accept='pipe,name=soffice-pipe-uuid;urp;StarOffice.ServiceManager' "
        "-env:UserInstallation=file:///tmp/soffice{process_id} "  # make the process run in parallel
        "disown"  # destroy after execution
        .format(source=filename, process_id=random.randint(1, 10000))
    )


def convert_pdf_to_images(filename: str, width: int, height: int, folder: str) -> int:
    """
    Convert pdf file to images (each page is different image) using imagemagick
    Args:
        filename (str): Source filename
        width (int): Desired width of the converted images
        height (int): Desired height of the converted images
        folder (str): Output folder
    Returns:
        int - The result of the conversion
    """
    return os.system(
        "convert {filename} "  # convert each page of a pdf to an individual image
        "-quality 50 "  # quality of image
        "-resize {width}x{height} "  # resizing
        "{folder}/%d.jpg"  # output
        .format(filename=filename, width=width, height=height, folder=folder)
    )


def cleanup_after_thumbnail_generation(thumbnails_folder: str, upload_filename: str, pdf_filename: str) -> None:
    """
    Cleanup after we generate the thumbnails
    Args:
        thumbnails_folder (str): The folder used to generate the thumbnails
        upload_filename (str): The uploaded file
        pdf_filename (str): The generated pdf file (after the conversion from presentation to pdf)
    Returns:
        None
    """
    shutil.rmtree(thumbnails_folder, True)
    os.remove(upload_filename)
    os.remove(pdf_filename)
