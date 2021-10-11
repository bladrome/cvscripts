#
# find /databank/archivedata/goatvideoimagesv3 -name "*.xml" | \
#     parallel --dry-run -j 90 python xmlparse.py {} /databank/archivedata/goatvideoimagesv2  /databank/archivedata/goatvideoimagesv4
#

import os
import cv2
import argparse

from xml_to_dict import XMLtoDict




def xmlparse(xmlFile, imageoridir, imageoutdir):
    with open(xmlFile) as fobj:
        xml = fobj.read()

    parser = XMLtoDict()
    xmldict =parser.parse(xml)['annotation']
    bndbox = xmldict['object']['bndbox']
    xmin, ymin, xmax, ymax = map(lambda x: int(x), (bndbox['xmin'], bndbox['ymin'], bndbox['xmax'], bndbox['ymax']))

    print(type(xmin))

    filepath = os.path.join(xmldict['folder'], xmldict['filename'])
    img = cv2.imread(os.path.join(imageoridir, filepath))
    print(xmin, ymin, xmax, ymax, img.shape)
    # cropimg = img[xmin:xmax, ymin:ymax]
    cropimg = img[ymin:ymax, xmin:xmax]
    print(os.path.join(imageoutdir, xmldict['folder']))
    if not os.path.exists(os.path.join(imageoutdir, xmldict['folder'])):
        os.mkdir(os.path.join(imageoutdir, xmldict['folder']))
    cv2.imwrite(os.path.join(imageoutdir, filepath), cropimg)


if __name__ == "__main__":

    # xmlFile = "/databank/archivedata/goatvideoimagesv3/1/IMG_20210912_141430.xml"
    # imageoridir = "/databank/archivedata/goatvideoimagesv2"
    # imageoutdir = "/databank/archivedata/goatvideoimagesv4"
    # python xmlparse.py /databank/archivedata/goatvideoimagesv3/1/IMG_20210912_141430.xml /databank/archivedata/goatvideoimagesv2  /databank/archivedata/goatvideoimagesv4

    parser = argparse.ArgumentParser()
    parser.add_argument("xmlFile")
    parser.add_argument("inputDir")
    parser.add_argument("outputDir")
    args = parser.parse_args()
    xmlFile = args.xmlFile
    imageoridir = args.inputDir
    imageoutdir = args.outputDir
    xmlparse(xmlFile, imageoridir, imageoutdir)
