# coding=utf-8
from flask import render_template, redirect

from . import main
from .forms import SearchForm
from .rpc_call import *


def search_redirect(form):
    network_data = get_info()
    if form.validate_on_submit():
        search_data = str(form.search_content.data).strip()
        if len(search_data) != 64:
            # could be a block height
            try:
                block_height = int(search_data)
            except:
                return False, None
            if 0 <= block_height <= network_data['topo_height']:
                return True, '/block/{}'.format(block_height)
        else:
            input_hash = str(search_data)
            tx_valid, tx_data = load_tx_info(search_data)
            if tx_valid:
                return True, '/tx/{}'.format(input_hash)
            block_valid, block_data = load_block_info(input_hash)
            if block_valid:
                return True, '/block/{}'.format(input_hash)
    return False, None


@main.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    jump, url = search_redirect(form)
    if jump:
        return redirect(url)
    network_data = get_info()
    block_list = list()
    for i in range(network_data['topo_height'] - 10, network_data['topo_height']):
        _, block_data = load_block_info(i)
        block_list.append(block_data)
    block_list = reversed(block_list)
    return render_template('index.html', network_data=network_data, block_list=block_list, form=form)


@main.route('/block/<block_hash_height>', methods=['GET', 'POST'])
def block(block_hash_height):
    form = SearchForm()
    network_data = get_info()
    valid_block, block_info = load_block_info(block_hash_height)
    if valid_block:
        pre_block = block_info['topo_height'] - 1
        next_block = block_info['topo_height'] + 1
        return render_template('block.html', network_data=network_data, pre_block=pre_block, next_block=next_block,
                               block_info=block_info, form=form)
    else:
        return redirect('/')


@main.route('/tx/<tx_hash>', methods=['GET', 'POST'])
def tx(tx_hash):
    form = SearchForm()
    network_data = get_info()
    valid_tx, tx_info = load_tx_info(tx_hash)
    if valid_tx:
        _, block_data = load_block_info(tx_info['block_height'])
        if tx_info['reward'] > 0:
            mature_require = 60
        else:
            mature_require = 10
        unlocked_height = tx_info['block_height'] + mature_require
        percent = min(100, int((block_data['depth'] / mature_require) * 100))
        return render_template('tx.html', network_data=network_data, block_data=block_data,
                               unlocked_height=unlocked_height, tx_info=tx_info, percent=percent,
                               tx_hash=tx_hash, form=form)
    else:
        return redirect('/')
