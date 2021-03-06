from mifiel import Base
import mimetypes
from os.path import basename
import requests

class Document(Base):
  def __init__(self, client):
    Base.__init__(self, client, 'documents')

  @staticmethod
  def find(client, doc_id):
    doc = Document(client)
    doc.process_request('get', url=doc.url(doc_id))
    return doc

  @staticmethod
  def create(client, signatories, file=None, dhash=None, callback_url=None):
    if not file and not dhash:
      raise ValueError('Either file or hash must be provided')
    if file and dhash:
      raise ValueError('Only one of file or hash must be provided')

    sig_numbers = {}

    for index, item in enumerate(signatories):
      for key, val in item.items():
        sig_numbers.update(
          {'signatories[' + str(index) + '][' + str(key) + ']': val}
        )

    data = sig_numbers

    if callback_url:
      data['callback_url'] = callback_url
    if file:
      mimetype = mimetypes.guess_type(file)[0]
      _file = open(file, 'rb')
      file = {'file': (basename(_file.name), _file, mimetype)}
    if dhash:
      data['original_hash'] = dhash

    doc = Document(client)
    doc.process_request('post', data=data, files=file)
    return doc

  def save_file(self, path):
    url_ = self.url('{}/file').format(self.id)
    response = requests.get(url_, auth=self.client.auth)
    with open(path, 'w') as file_:
      file_.write(response.text)

  def save_file_signed(self, path):
    url_ = self.url('{}/file_signed').format(self.id)
    response = requests.get(url_, auth=self.client.auth)
    with open(path, 'w') as file_:
      file_.write(response.text)

  def save_xml(self, path):
    url_ = self.url('{}/xml').format(self.id)
    response = requests.get(url_, auth=self.client.auth)
    with open(path, 'w') as file_:
      file_.write(response.text)
