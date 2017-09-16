from html.parser import HTMLParser
import binascii
import base64
import os
import json
import threading
import uuid
import re


class MetaParser(HTMLParser):
    common_payload = ''
    metadata = dict()
    level = 0

    coverart_path = './'
    infofile_path = './info.json'
    tag_typ = ''
    type_code = ''
    coverart_done=False

    def handle_starttag(self, tag, attrs):
        self.tag_typ = tag
        if tag == 'item':
            self.level = 1
       

    def handle_endtag(self, tag):
        if tag == 'item':
            self.level = 0
            
        if self.coverart_done:
           
            json.dump(self.metadata, open(self.infofile_path, 'w'))
            print("write files")
            self.coverart_done=False

    def handle_data(self, data):

        if self.tag_typ == 'type':
            self.type_code = binascii.a2b_hex(data)

        elif self.tag_typ == 'code':
            self.code_code = binascii.a2b_hex(data)
            if self.code_code == b'mden':
                
                print('end of metadate write info file')
                print(self.metadata)
                self.startmetadate = False

            if self.code_code == b'mdst':
                print('start of metadate')
                # clean up houskeeping
                self.startmetadate = True

                # if 'coverart' in self.metadata :
                #    os.remove(self.metadata['coverart'])

        elif self.tag_typ == 'length':
            self.length = 0

        # print (self.type_code == b'core')
        if self.tag_typ == 'data' and self.level == 1:
            self.length = len(data)

        if self.type_code == b'core' and self.tag_typ == 'data' and self.level == 1:
            self.common_payload = base64.b64decode(data.strip())

            if self.code_code == b'minm':
                self.metadata['name'] = self.common_payload.decode()

            elif self.code_code == b'asal':
                self.metadata['album'] = self.common_payload.decode()

            elif self.code_code == b'asar':
                self.metadata['interpret'] = self.common_payload.decode()

        elif self.type_code == b'ssnc' and self.tag_typ == 'data' and self.level == 1:
            if self.code_code == b'PICT':

                try:
                
                    os.remove(self.metadata['coverart'])
                except:
                    print ('cover not deleted')
                coverart = os.path.join(
                    self.coverart_path, str(uuid.uuid1()) + '.jpg')
                with open(coverart, "wb") as fh:
                    fh.write(base64.b64decode(data.strip()))
                    self.metadata['coverart'] = coverart
                    self.coverart_done=True

    def info(self):
        print('type : {0} code {1} ({2})'.format(
            self.type_code, self.code_code, self.length))
        print(self.metadata)


#parser = MyHTMLParser()


def connect(pipe='/tmp/shairport/metadata', basepath=None):
    parser = MetaParser()
    parser.coverart_path = basepath
    parser.infofile_path = os.path.join(basepath, 'info.json')

    while True:
        with open(pipe) as p:
            item = ''
            for line in p:
                item += line.strip()
                if line.strip().endswith('</item>'):
                    print(item)
                    parser.feed(item)
                    parser.info()
                    item=''


def runBackround(pipe='/tmp/shairport/metadata', basepath=None):

    metadate_parser_thread = threading.Thread(
        target=connect, kwargs={'pipe': pipe, 'basepath': basepath})
    metadate_parser_thread.start()


if __name__ == "__main__":
    connect('/tmp/shairport/metadata',
            '/home/enrico/Development/python/pymediacontrol/mediacontrol/static')
