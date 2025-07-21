import os
from PIL import Image
import pillow_heif
import io
import pydantic

sourcePath = "Path"
# print (os.listdir(sourcePath))

def getListOfHeicFiles(sourcePath):
    # Only selecting the main directory where file extension is "heic". Does not recursively check sub-directories.
    listOfFiles = [f for f in os.listdir(sourcePath) if os.path.isfile(os.path.join(sourcePath,f)) and f.rsplit(".",1)[-1].lower() == "heic"]
    # print (listOfFiles)
    print (len(listOfFiles))
    return listOfFiles

def convertHeicToJPG(heicFileFullPath, fileName, targetFilePath="/", targetFileName="Test", compressionPrecentage=0, expectedFileSize='moderate'):
    with open(heicFileFullPath, "rb") as heicFile:
        heicFileBytes = heicFile.read()

    print (type(heicFileBytes))
    print (len(heicFileBytes))

    heif_file = pillow_heif.read_heif(heicFileBytes)

    fileNamePrefix = targetFileName

    print (heif_file.mode)
    print (heif_file.size)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
    )
    width, height = image.size
    # print (width, height)
    # Adjust Image size by reducing width and corresponding height
    if compressionPrecentage is None or compressionPrecentage == 0:
        TARGET_WIDTH = width
    else:
        TARGET_WIDTH = int(width * compressionPrecentage)
    coefficient = width / TARGET_WIDTH
    new_height = int (height / coefficient)
    if targetFilePath == "/":
        new_file = fileNamePrefix + ".jpg"
    else:
        new_file = targetFilePath + "/" + fileNamePrefix + ".jpg"
    # print (new_file)
    optimalSizeImage = image.resize((int(TARGET_WIDTH),int(new_height)),Image.LANCZOS)
    # print (type(optimalSizeImage))
    imgByteArr = io.BytesIO()
    if (expectedFileSize).lower() == 'low':
        quality = 20
    elif expectedFileSize.lower() == 'moderate':
        quality = 50
    else:
        quality = 95
    optimalSizeImage.save(imgByteArr, format("jpeg"),quality=quality)
    imagedata = imgByteArr.getvalue()                                            

    # Write imagedata to file
    with open (new_file, "wb") as f:
        f.write(imagedata)
    f.close()
    return True

def wrapperHeicToJPG(folderOrImage, sourcePath, targetFolder, compressionPercentage, imageQuality ):
    if folderOrImage == 'Folder':
        listOfFiles = getListOfHeicFiles(sourcePath=sourcePath)
        for file in listOfFiles:
            heicFileFullPath = sourcePath + "/" + file
            norm_heicFileFullPath = heicFileFullPath.replace("\\","/")
            filePath = norm_heicFileFullPath.rsplit("/", 1)[0]
            fileName = norm_heicFileFullPath.rsplit("/", 1)[-1]
            if targetFolder is None or targetFolder.strip() == "":
                targetFolder = filePath
            else:
                targetFolder = targetFolder
            fileNameWithoutExt = fileName.rsplit(".", 1)[0]
            print ("File Path: ", filePath)
            print ("File Name: ", fileName)
            print ("norm_heicFileFullPath: ", norm_heicFileFullPath)

            convertHeicToJPG(heicFileFullPath = norm_heicFileFullPath, fileName = fileName, targetFilePath = targetFolder, targetFileName = fileNameWithoutExt, compressionPrecentage=compressionPercentage, expectedFileSize=imageQuality)

    else:
        norm_heicFileFullPath = sourcePath.replace("\\","/")
        filePath = norm_heicFileFullPath.rsplit("/", 1)[0]
        fileName = norm_heicFileFullPath.rsplit("/", 1)[-1]
        if fileName.rsplit(".",1)[-1].lower() != "heic":
            print ("This file does not have heic extension")
            raise Exception("This file does not have heic extension. Please double check the parameters provided in the form.")
        if targetFolder is None or targetFolder.strip() == "":
            targetFolder = filePath
        else:
            targetFolder = targetFolder
        fileNameWithoutExt = fileName.rsplit(".", 1)[0]
        print ("File Path: ", filePath)
        print ("File Name: ", fileName)
        print ("norm_heicFileFullPath: ", norm_heicFileFullPath)

        convertHeicToJPG(heicFileFullPath = norm_heicFileFullPath, fileName = fileName, targetFilePath = targetFolder, targetFileName = fileNameWithoutExt, compressionPrecentage=compressionPercentage, expectedFileSize=imageQuality)
    return "Success"



# heicFileFullPath = "Path/20250607_125528.heic"

# userInput = input("Please provide full image path:\n")
# heicFileFullPath = userInput.strip()

# norm_heicFileFullPath = heicFileFullPath.replace("\\","/")
# filePath = norm_heicFileFullPath.rsplit("/", 1)[0]
# fileName = norm_heicFileFullPath.rsplit("/", 1)[-1]
# fileNameWithoutExt = fileName.rsplit(".", 1)[0]
# print ("filePath: ", filePath)

# convertHeicToJPG(heicFileFullPath = heicFileFullPath, fileName = fileName, targetFilePath = filePath, targetFileName = fileNameWithoutExt, compressionPrecentage=0, expectedFileSize='moderate')

# # Open the image
# img = Image.open("test123.jpeg")

# # Get dimensions
# width, height = img.size
# print(f"Image size: {width} x {height}")