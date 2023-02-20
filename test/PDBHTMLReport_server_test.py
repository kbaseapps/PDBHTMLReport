# -*- coding: utf-8 -*-
import os
import time
import unittest
from configparser import ConfigParser

from PDBHTMLReport.PDBHTMLReportImpl import PDBHTMLReport
from PDBHTMLReport.PDBHTMLReportServer import MethodContext
from PDBHTMLReport.authclient import KBaseAuth as _KBaseAuth

from installed_clients.WorkspaceClient import Workspace


class PDBHTMLReportTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('PDBHTMLReport'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'PDBHTMLReport',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = PDBHTMLReport(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        cls.wsName = "test_ContigFilter_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_your_method(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
        pdb_infos = [{
            'structure_name': '6TUK',
            'file_extension': '.pdb',
            'narrative_id': 63679,
            'genome_name': 'MLuteus_ATCC_49442',
            'feature_id': 'MLuteus_masurca_RAST.CDS.133',
            'is_model': 1,
            'from_rcsb': 1,
            'file_path': os.path.join('/kb/module/test/data', '6TUK.pdb.gz'),
            'genome_ref': '63679/38/1',  # for appdev
            # 'genome_ref': '107138/2/1',  # for prod
            'feature_type': 'gene',
            'sequence_identities': '68.93%',
            'chain_ids': 'Model 1.Chain B',
            'model_ids': '0',
            'exact_matches': '0',
            'scratch_path': os.path.join('/kb/module/test/data', '6TUK.pdb.gz')
        }, {
            'structure_name': 'MLuteus_AlphaFold_3483',
            'file_extension': '.pdb',
            'narrative_id': 63679,
            'genome_name': 'MLuteus_ATCC_49442',
            'feature_id': 'MLuteus_masurca_RAST.CDS.3483',
            'is_model': 1,
            'from_rcsb': 0,
            'file_path': os.path.join('/kb/module/test/data', 'MLuteus_AlphaFold_3483.pdb'),
            'genome_ref': '63679/38/1',  # for appdev
            # 'genome_ref': '107138/2/1',  # for prod
            'feature_type': 'gene',
            'sequence_identities': '99.99%',
            'chain_ids': 'Model 1.Chain B',
            'model_ids': '0',
            'exact_matches': '1',
            'scratch_path': os.path.join('/kb/module/test/data', 'MLuteus_AlphaFold_3483.pdb')
        }]
        ret = self.serviceImpl.run_PDBHTMLReport(self.ctx, pdb_infos)
        self.assertTrue(ret[0]['report_html'])
        self.assertTrue(ret[0]['doms'])
        print(ret[0]['report_html'])
