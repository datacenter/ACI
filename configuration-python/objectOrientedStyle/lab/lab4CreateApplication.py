from labScript import *
import createApplication
import createApplicationEpg
import connectEpgContract
from cobra.model.fv import Ap, AEPg, RsBd


class Lab4CreateApplication(LabScript):
    """
    Create Application
    """
    def __init__(self):
        self.description = 'Create Application'
        self.tenant_required = True
        self.application_optional_args = None
        self.epgs = []
        self.applied_contracts = []
        super(Lab4CreateApplication, self).__init__()

    def run_yaml_mode(self):
        super(Lab4CreateApplication, self).run_yaml_mode()
        self.application = self.args['application']['name']
        self.application_optional_args = self.args['application']['optional_args']
        self.epgs = self.args['epgs']
        self.applied_contracts = self.args['applied_contracts']

    def wizard_mode_input_args(self):
        application = add_mos('Create a Application', self.input_application_name, opt_args_function= createApplication.input_optional_args, do_first=True, once=True)
        epgs = add_mos('Add a Application EPG', createApplicationEpg.input_key_args, createApplicationEpg.input_optional_args)
        applied_contracts = add_mos('Add a Applied Contract to EPG', connectEpgContract.input_key_args)
        self.application_optional_args = application['opt_args']
        for epgs in epgs:
            self.epgs.append({'name': epgs['key_args'], 'optional_args': epgs['opt_args']})
        for contract in applied_contracts:
            self.applied_contracts.append({'epg': contract['key_args'][0],
                                           'name': contract['key_args'][1],
                                           'type': contract['key_args'][2]})

    def main_function(self):
        fv_tenant = self.check_if_tenant_exist()
        fv_ap = createApplication.create_application(fv_tenant, self.application, optional_args=self.application_optional_args)
        for epg in self.epgs:
            createApplicationEpg.create_application_epg(fv_ap, epg['name'], optional_args=epg['optional_args'])
        self.commit_change(changed_object=fv_tenant)
        for contract in self.applied_contracts:
            print '-------', contract
            fv_aepg = self.check_if_mo_exist('uni/tn-' + self.tenant + '/ap-' + self.application + '/epg-', contract['epg'], AEPg, description='Application EPG')
            connectEpgContract.connect_epg_contract(fv_aepg, contract['name'], contract['type'])
            self.commit_change(changed_object=fv_aepg)


if __name__ == '__main__':
    mo = Lab4CreateApplication()