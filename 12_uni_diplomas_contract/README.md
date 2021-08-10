# Issuing university diplomas on the Algorand blockchain

Note clear_state = for deleting app, close_out = for opting-out

Repository notes:
* Make the PyTEAL contract code: `make`
* Deploy the smart contract: `python3 run_diploma.py deploy`
  *  This command will print an identifying number for APP_ID.
  *  Be sure to record this in the config.yml.
* Use the DApp:
  * Opt-in bob to the smart contract:` python3 run_diploma.py opt-in bob`
  * Issue a diploma to bob: `python3 run_diploma.py issue-diploma bob "MIT,2020,BSc,Computer Science and Engineering"`
  * Transfer registrar duties to charlie: `python3 run_diploma.py reassign-registrar charlie`
  * In order to transfer registrar duties, the current (old) registrar must still be set in the config.yml.
    * Once the duties have been transfered to charlie, update the registrar field in the config.yml to list charlie.
  * For more commands run: `python3 run_diploma.py help`

Roles:
* Registrar = admin who can issue and revoke diplomas, full control of the smart contract.
* Student = user of the DApp. Must opt-in and recieve a diploma from the registrar.

Smart contract

Deployment:
```bash
make
python3 run_diploma.py deploy
```