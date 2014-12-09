from labScript import *
from apicPython import createFilter
from apicPython import createContract


class Lab3BuildingPolicyFiltersAndContracts(LabScript):
    """
    Create Filters and Contracts
    """
    def __init__(self):
        self.description = 'Create Filters and Contracts'
        self.tenant_required = True
        self.filters = []
        self.contracts = []
        super(Lab3BuildingPolicyFiltersAndContracts, self).__init__()

    def run_yaml_mode(self):
        super(Lab3BuildingPolicyFiltersAndContracts, self).run_yaml_mode()
        self.filters = self.args['filters']
        self.contracts = self.args['contracts']

    def wizard_mode_input_args(self):
        filters = add_mos('Add a Filter', createFilter.input_key_args, createFilter.input_optional_args)
        contracts = add_mos('Add a Contract', createContract.input_key_args, createContract.input_optional_args)
        for filter in filters:
            self.filters.append({'name': filter['key_args'], 'optional_args': filter['opt_args']})
        for contract in contracts:
            self.contracts.append({'name': contract['key_args'], 'optional_args': contract['opt_args']})

    def main_function(self):
        fv_tenant = self.check_if_tenant_exist()
        for filter in self.filters:
            vz_filter = createFilter.create_filter(fv_tenant, filter['name'])
            if return_valid_optional_args(filter):
                for entry in return_valid_optional_args(filter):
                    createFilter.create_filter_entry(vz_filter, filter['name'], optional_args=entry)

        for contract in self.contracts:
            vz_ct=createContract.create_contract(fv_tenant, contract['name'], optional_args=return_valid_optional_args(contract))
            if is_valid_key(contract, 'optional_args') and is_valid_key(contract['optional_args'], 'subjects'):
                for subject in contract['optional_args']['subjects']:
                    subject['subject'] = subject['name']
                    vz_subj = createContract.create_contract_subject(vz_ct, contract['name'], optional_args=subject)
                    if is_valid_key(subject, 'filters'):
                        for filter in subject['filters']:
                            createContract.add_filter_to_subject(vz_subj, filter)

if __name__ == '__main__':
    mo = Lab3BuildingPolicyFiltersAndContracts()