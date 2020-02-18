import argparse
import io
import re
import csv

from google.cloud import storage
from google.cloud import vision
from google.protobuf import json_format


# [START def_detect_document]
def detect_document(path):
    """Detects document features in an image."""
    client = vision.ImageAnnotatorClient()

    # [START migration_document_text_detection]
    with io.open(paths, 'rb') as image_file:
        content = image_file.read()
        filename = image_file.name.split('/')[2]
        product_title = filename.split('.')[0]
        print(product_title)

    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)
    blockcount = 0
    BLOCK = 'BLOCK'

    my_dict = {'Name': product_title}
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            #print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
            #print('Block Number:',blockcount)
            #print('Block confidence: {}'.format(block.confidence))
            blockcount += 1

            for paragraph in block.paragraphs:
                #print('\nParagraph confidence: {}\n'.format(
                    #paragraph.confidence))

                endstring = ""
                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    endstring = endstring + word_text + ' '
                #print(endstring)
            #print('\n')
            while(blockcount):
                my_dict[BLOCK+ str(blockcount)] = endstring
                break
        #print(my_dict)
    print(count)
    if(count==1):
        with open('/Users/Ayush/Desktop/VisionAPI/ss2text/Delllaptops102.csv', 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([k for k in my_dict])
            writer.writerow([v for v in my_dict.values()])
    else:
        with open('/Users/Ayush/Desktop/VisionAPI/ss2text/Delllaptops102.csv', 'a') as csv_file:
            writer = csv.writer(csv_file)
            #writer.writerow([k for k in my_dict])
            writer.writerow([v for v in my_dict.values()])

        """for key, value in my_dict.items():
            writer.writerow([key])
            writer.writerow([value])"""

    # [END migration_document_text_detection]
# [END def_detect_document]


def run_local(args):  
    if args.command == 'document':
        detect_document(paths)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')

    count = 0

    with open('/Users/Ayush/Desktop/VisionAPI/ss2text/dell_path_102.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            count += 1
            paths = (', '.join(row))

            # 1.1 Vision features
            document_parser = subparsers.add_parser(
                'document', help=detect_document.__doc__)
                
            args = parser.parse_args()

            run_local(args)  
