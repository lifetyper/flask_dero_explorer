# coding=utf-8
import logging
import json
from jsonrpcclient.clients.http_client import HTTPClient
from jsonrpcclient.exceptions import ReceivedNon2xxResponseError
from jsonrpcclient.request import Request
import requests
from datetime import datetime


def get_info():
    client = HTTPClient("http://127.0.0.1:20206/json_rpc")
    network_data = dict()
    try:
        response = client.send(Request("get_info")).data.result
        print(response)
        network_data['difficulty'] = response['difficulty']
        network_data['height'] = response['height']
        network_data['topo_height'] = response['topoheight']
        network_data['block_time'] = response['averageblocktime50']
        network_data['total_supply'] = response['total_supply']
        network_data['dynamic_fee_per_kb'] = response['dynamic_fee_per_kb'] / 1000000000000
        network_data['hash_rate'] = "{0:.3f}".format(float(network_data['difficulty']) / (12 * 1000000))
        return network_data
    except ReceivedNon2xxResponseError as e:
        logging.warning(e)


def load_tx_info(tx_hash):
    tx_data = dict()
    address = "http://127.0.0.1:20206/gettransactions"
    params = {'txs_hashes': [tx_hash]}
    try:
        response = json.loads(requests.post(url=address, json=params).content.decode())
        if response['status'] == "TX NOT FOUND":
            return False, None
        tx_data['size'] = float('{0:.3f}'.format(len(response['txs_as_hex'][0]) / 2048))
        # FIXME Fee calc error
        # tx_data['fee'] = float('{0:.3f}'.format((int(tx_data['size']) + 1) * fee_per_kb))
        tx_data['fee'] = '*'
        tx_data['reward'] = response['txs'][0]['reward']
        if not tx_data['reward']:
            tx_data['ring_count'] = len(response['txs'][0]['ring'][0])
        else:
            tx_data['ring_count'] = 0
        tx_data['valid_block'] = response['txs'][0]['valid_block']
        tx_data['block_height'] = response['txs'][0]['block_height']
        return True, tx_data
    except ReceivedNon2xxResponseError as e:
        logging.warning(e)
        return False, None


def load_block_info(height_hash):
    block_data = dict()
    client = HTTPClient("http://127.0.0.1:20206/json_rpc")
    height_hash = str(height_hash)
    try:
        if len(height_hash) == 64:
            response = client.send(Request("getblock", hash=height_hash)).data.result
        else:
            height_hash = int(height_hash)
            response = client.send(Request("getblock", height=height_hash)).data.result
    except ReceivedNon2xxResponseError as e:
        logging.warning(e)
        return False, None
    block_data['block_hash'] = response['block_header']['hash']
    block_data['block_difficulty'] = response['block_header']['difficulty']
    block_data['timestamp'] = response['block_header']['timestamp']
    block_data['time'] = datetime.utcfromtimestamp(block_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
    block_data['height'] = response['block_header']['height']
    block_data['topo_height'] = response['block_header']['topoheight']
    block_data['depth'] = response['block_header']['depth']
    block_data['tips'] = response['block_header']['tips']
    json_data = json.loads(response['json'])
    block_data['miner_tx'] = json_data['miner_tx']
    block_data['miner_reward'] = response['block_header']['reward'] / 1000000000000
    block_data['tx_hashes'] = json_data['tx_hashes']
    block_data['size'] = 0
    block_data['tx_size_list'] = list()
    if block_data['tx_hashes']:
        block_data['tx_count'] = len(block_data['tx_hashes'])
        for tx in block_data['tx_hashes']:
            _, tx_data = load_tx_info(tx)
            block_data['size'] += tx_data['size']
            block_data['tx_size_list'].append(tx_data['size'])
        block_data['size'] = "{0:.3f}".format(block_data['size'])
        block_data['hash_size_list'] = zip(block_data['tx_hashes'], block_data['tx_size_list'])
    else:
        block_data['tx_count'] = 0

    return True, block_data


miner_tx = '381fc10ad97cdfa1dac9fcad52cb3a56b0c538e2e48ee8312bba130ffd848f7b'
normal_tx = '7af20789a735acbb53fb7289becbd89eec915ff2a466b049c251372c3b919643'

block_hash = '7a71fe371ebabf814abd173c27c586d7723054fdc91df373082d0028f6616201'
fake_hash = '3a71fe371ebabf814abd173c27c586d7723054fdc91df373082d0028f6616201'
block_height = 784128

# print(load_tx_info(normal_tx))
# print(load_block_info(block_height))
