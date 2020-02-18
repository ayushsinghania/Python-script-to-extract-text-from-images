import argparse
import io
import re
import csv

from google.cloud import storage
from google.cloud import vision
from google.protobuf import json_format

# [START def_detect_labels]
def detect_labels(path):
    """Detects labels in the file."""
    client = vision.ImageAnnotatorClient()

    # [START migration_label_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    for label in labels:
        print('Label text: {} (score: {})'.format(label.description, label.score))

    # [END migration_label_detection]
# [END def_detect_labels]


# [START def_detect_labels_uri]
def detect_labels_uri(uri):
    """Detects labels in the file located in Google Cloud Storage or on the
    Web."""
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    for label in labels:
        print(label.description)
# [END def_detect_labels_uri]

# [START def_detect_document]
def detect_document(path):
    """Detects document features in an image."""
    client = vision.ImageAnnotatorClient()

    # [START migration_document_text_detection]
    with io.open(path, 'rb') as image_file:
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
    with open('/Users/Ayush/Desktop/VisionAPI/ss2text/%s.csv' % product_title, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([k for k in my_dict])
        writer.writerow([v for v in my_dict.values()])

        """for key, value in my_dict.items():
            writer.writerow([key])
            writer.writerow([value])"""

    # [END migration_document_text_detection]
# [END def_detect_document]


# [START def_detect_document_uri]
def detect_document_uri(uri):
    """Detects document features in the file located in Google Cloud
    Storage."""
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.document_text_detection(image=image)

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:
                print('Paragraph confidence: {}'.format(
                    paragraph.confidence))

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    print('Word text: {} (confidence: {})'.format(
                        word_text, word.confidence))

                    """for symbol in word.symbols:
                        print('\tSymbol: {} (confidence: {})'.format(
                            symbol.text, symbol.confidence))"""
# [END def_detect_document_uri]

def run_local(args):
    if args.command == 'labels':
        detect_labels(args.path)   
    elif args.command == 'document':
        detect_document(args.path)

def run_uri(args):
    if args.command == 'labels-uri':
        detect_labels_uri(args.uri)    
    elif args.command == 'document-uri':
        detect_document_uri(args.uri)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')

    detect_labels_parser = subparsers.add_parser(
        'labels', help=detect_labels.__doc__)
    detect_labels_parser.add_argument('path')

    labels_file_parser = subparsers.add_parser(
        'labels-uri', help=detect_labels_uri.__doc__)
    labels_file_parser.add_argument('uri')

    # 1.1 Vision features
    document_parser = subparsers.add_parser(
        'document', help=detect_document.__doc__)
    document_parser.add_argument('path')

    document_uri_parser = subparsers.add_parser(
        'document-uri', help=detect_document_uri.__doc__)
    document_uri_parser.add_argument('uri')

    args = parser.parse_args()

    if 'uri' in args.command:
        run_uri(args)
    else:
        run_local(args)
