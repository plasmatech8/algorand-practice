import time

from _01_create_asset import create_asset
from _02_change_manager import change_manager
from _03_opt_in import opt_in
from util import print_accounts_list

print('============= 00 - Show account list')
print_accounts_list()
input('Continue?\n')

print('============= 01 - Create Asset named LATINUM')
asset_id = create_asset()
input('Continue?\n')

print('============= 02 - Change manager from acc2 to acc1')
change_manager(asset_id)
input('Continue?\n')

print('============= 03 - Opt-in acc3 for LATINUM')
opt_in(asset_id)
input('Finished!\n')