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
            createFilter.create_filter(fv_tenant, filter['name'], optional_args=filter['optional_args'])
        for contract in self.contracts:
            createContract.create_contract(fv_tenant, contract['name'], optional_args=contract['optional_args'])

if __name__ == '__main__':
    mo = Lab3BuildingPolicyFiltersAndContracts()