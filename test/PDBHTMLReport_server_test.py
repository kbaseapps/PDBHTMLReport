# -*- coding: utf-8 -*-
import os
import unittest
import time
from configparser import ConfigParser

from PDBHTMLReport.PDBHTMLReportImpl import PDBHTMLReport
from PDBHTMLReport.PDBHTMLReportServer import MethodContext
from PDBHTMLReport.authclient import KBaseAuth as _KBaseAuth
from installed_clients.DataFileUtilClient import DataFileUtil
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
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = PDBHTMLReport(cls.cfg)
        suffix = int(time.time() * 1000)
        cls.wsName = "test_PDBHTMLReport_" + str(suffix)
        cls.ws_id = cls.wsClient.create_workspace({'workspace': cls.wsName})[0]
        cls.scratch = cls.cfg['scratch']
        cls.dfu = DataFileUtil(cls.callback_url)
        # cls.prepare_structures_object()

    # save the proteinstructures object and return a ref for test the apps in this module
    @classmethod
    def prepare_structures_object(cls):
        """Saving (by dfu) a well-defined KBaseStructure.ProteinStructures
           using appdev objects
        """

        cls.pdb_infos = [{
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
            'structure_name': 'MLuteus_AlphaFold_133',
            'file_extension': '.pdb',
            'narrative_id': 63679,
            'genome_name': 'MLuteus_ATCC_49442',
            'feature_id': 'MLuteus_masurca_RAST.CDS.133',
            'is_model': 1,
            'from_rcsb': 0,
            'file_path': os.path.join('/kb/module/test/data', 'MLuteus_AlphaFold_133.pdb'),
            'genome_ref': '63679/38/1',  # for appdev
            # 'genome_ref': '107138/2/1',  # for prod
            'feature_type': 'gene',
            'sequence_identities': '99.99%',
            'chain_ids': 'Model 1.Chain B',
            'model_ids': '0',
            'exact_matches': '1',
            'scratch_path': os.path.join('/kb/module/test/data', 'MLuteus_AlphaFold_133.pdb')
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
        }, {
            'structure_name': 'MLuteus_AlphaFold_3664',
            'file_extension': '.pdb',
            'narrative_id': 63679,
            'genome_name': 'MLuteus_ATCC_49442',
            'feature_id': 'MLuteus_masurca_RAST.CDS.3664',
            'is_model': 1,
            'from_rcsb': 0,
            'file_path': os.path.join('/kb/module/test/data', 'MLuteus_AlphaFold_3664.pdb'),
            'genome_ref': '63679/38/1',  # for appdev
            # 'genome_ref': '107138/2/1',  # for prod
            'feature_type': 'gene',
            'sequence_identities': '99.99%',
            'chain_ids': 'Model 1.Chain B',
            'model_ids': '0',
            'exact_matches': '1',
            'scratch_path': os.path.join('/kb/module/test/data', 'MLuteus_AlphaFold_3664.pdb')
        }]
        obj_to_save = {
            'protein_structures': [
              {'name': 'ksga from bacillus subtilis 168', 'num_chains': 2, 'num_residues': 567, 'num_atoms': 4583,
               'compound': {'misc': '', 'molecule': 'ribosomal rna small subunit methyltransferase a', 'chain': 'a, b',
                            'synonym': "16s rrna (adenine(1518)-n(6)/adenine(1519)-n(6))-dimethyltransferase,16s rrna dimethyladenosine transferase,16s rrna dimethylase,s-adenosylmethionine-6-n',n'-adenosyl(rrna) dimethyltransferase ",
                            'ec_number': '2.1.1.182', 'ec': '2.1.1.182', 'engineered': 'yes'},
               'source': {'misc': '', 'organism_scientific': 'bacillus subtilis (strain 168)', 'organism_taxid': '224308', 'strain': '168', 'gene': 'rsma, ksga, bsu00420', 'expression_system': 'escherichia coli', 'expression_system_taxid': '562'},
               'proteins': [
                  {'id': '6ifs.pdb', 'model_id': 0, 'chain_id': 'A', 'sequence': 'KDIATPIRTKEILKKYGFSFKKSLGQNFLIDTNILNRIVDHAEVTEKTGVIEIGPGIGALTEQLAKRAKKVVAFEIDQRLLPILKDTLSPYENVTVIHQDVLKADVKSVIEEQFQDCDEIMVVANLPYYVTTPIIMKLLEEHLPLKGIVVMLQKEVAERMAADPSSKEYGSLSIAVQFYTEAKTVMIVPKTVFVPQPNVDSAVIRLILRDGPAVDVENESFFFQLIKASFAQRRKTLLNNLVNNLPEGKAQKSTIEQVLEETNIDGKRRGESLSIEEFAALSNGLYKALF', 'md5': 'f0eb43b0bf610adb501695053cecc5a6', 'seq_identity': 0.679487, 'exact_match': 0, 'genome_ref': '57196/6/1', 'feature_id': 'JCVISYN3_0004', 'feature_type': 'gene'},
                  {'id': '6ifs.pdb', 'model_id': 0, 'chain_id': 'B', 'sequence': 'ATPIRTKEILKKYNFLIDTNILNRIVDHAEVTEKTGVIEIGPGIGALTEQLAKRAKKVVAFEIDQRLLPILKDTLSPYENVTVIHQDVLKADVKSVIEEQFQDCDEIMVVANLPYYVTTPIIMKLLEEHLPLKGIVVMLQKEVAERMAADPSSKEYGSLSIAVQFYTEAKTVMIVPKTVFVPQPNVDSAVIRLILRDGPAVDVENESFFFQLIKASFAQRRKTLLNNLVNNLPEGKAQKSTIEQVLEETNIDGKRRGESLSIEEFAALSNGLYKALF', 'md5': 'a6c3a37bcc8c3be55fce6bfdae74e3be', 'seq_identity': 0.677419, 'exact_match': 0, 'genome_ref': '57196/6/1', 'feature_id': 'JCVISYN3_0004', 'feature_type': 'gene'}
                ],
                'pdb_handle': 'KBH_182761', 'user_data': '', 'is_model': 1
              },
              {'name': 'ksga from bacillus subtilis in complex with sam', 'num_chains': 1, 'num_residues': 292, 'num_atoms': 2508, 'compound': {'misc': '', 'molecule': 'ribosomal rna small subunit methyltransferase a', 'chain': 'a', 'synonym': "16s rrna (adenine(1518)-n(6)/adenine(1519)-n(6))-dimethyltransferase,16s rrna dimethyladenosine transferase,16s rrna dimethylase,s-adenosylmethionine-6-n',n'-adenosyl(rrna) dimethyltransferase ", 'ec_number': '2.1.1.182', 'ec': '2.1.1.182', 'engineered': 'yes'}, 'source': {'misc': '', 'organism_scientific': 'bacillus subtilis (strain 168)', 'organism_taxid': '224308', 'strain': '168', 'gene': 'rsma, ksga, bsu00420', 'expression_system': 'escherichia coli', 'expression_system_taxid': '562'},
               'proteins': [{'id': '6ift.pdb', 'model_id': 0, 'chain_id': 'A', 'sequence': 'MNKDIATPIRTKEILKKYGFSFKKSLGQNFLIDTNILNRIVDHAEVTEKTGVIEIGPGIGALTEQLAKRAKKVVAFEIDQRLLPILKDTLSPYENVTVIHQDVLKADVKSVIEEQFQDCDEIMVVANLPYYVTTPIIMKLLEEHLPLKGIVVMLQKEVAERMAADPSSKEYGSLSIAVQFYTEAKTVMIVPKTVFVPQPNVDSAVIRLILRDGPAVDVENESFFFQLIKASFAQRRKTLLNNLVNNLPEGKAQKSTIEQVLEETNIDGKRRGESLSIEEFAALSNGLYKALF', 'md5': '076fc7704e83dab1565ae973a11c435d', 'seq_identity': 0.679487, 'exact_match': 0, 'genome_ref': '57196/6/1', 'feature_id': 'JCVISYN3_0004', 'feature_type': 'gene'}],
               'pdb_handle': 'KBH_182762', 'user_data': '', 'is_model': 1
              },
              {'name': 'c-terminal truncated ksga from bacillus subtilis 168', 'num_chains': 2, 'num_residues': 410, 'num_atoms': 3068,'compound': {'misc': '', 'molecule': 'ribosomal rna small subunit methyltransferase a', 'chain': 'a, b', 'fragment': 'c-terminal truncated', 'synonym': "16s rrna (adenine(1518)-n(6)/adenine(1519)-n(6))-dimethyltransferase,16s rrna dimethyladenosine transferase,16s rrna dimethylase,s-adenosylmethionine-6-n',n'-adenosyl(rrna) dimethyltransferase ", 'ec_number': '2.1.1.182', 'ec': '2.1.1.182', 'engineered': 'yes'}, 'source': {'misc': '', 'organism_scientific': 'bacillus subtilis (strain 168)', 'organism_taxid': '224308', 'strain': '168', 'gene': 'rsma, ksga, bsu00420', 'expression_system': 'escherichia coli', 'expression_system_taxid': '562'},
               'proteins': [{'id': '6ifv.pdb', 'model_id': 0, 'chain_id': 'A', 'sequence': 'KDIATPIRTKEILKKYGFSFQNFLIDTNILNRIVDHAEVTEKTGVIEIGPGIGALTEQLAKRAKKVVAFEIDQRLLPILKDTLSPYENVTVIHQDVLKADVKSVIEEQFQDCDEIMVVANLPYYVTTPIIMKLLEEHLPLKGIVVMLQKEVAERMAADPSSKEYGSLSIAVQFYTEAKTVMIVPKTVFVPQPNVDSAVIRLILR', 'md5': '08a6b2ba57f21c334db58633867a40e9', 'seq_identity': 0.694915, 'exact_match': 0, 'genome_ref': '57196/6/1', 'feature_id': 'JCVISYN3_0004', 'feature_type': 'gene'},
                            {'id': '6ifv.pdb', 'model_id': 0, 'chain_id': 'B', 'sequence': 'DIATPIRTKEILKKYGFSFKKSQNFLIDTNILNRIVDHAEVTEKTGVIEIGPGIGALTEQLAKRAKKVVAFEIDQRLLPILKDTLSPYENVTVIHQDVLKADVKSVIEEQFQDCDEIMVVANLPYYVTTPIIMKLLEEHLPLKGIVVMLQKEVAERMAADPSSKEYGSLSIAVQFYTEAKTVMIVPKTVFVPQPNVDSAVIRLILR', 'md5': 'e614ffbf074ae76a9c3fd447adf9e447', 'seq_identity': 0.694915, 'exact_match': 0, 'genome_ref': '57196/6/1', 'feature_id': 'JCVISYN3_0004', 'feature_type': 'gene'}],
               'pdb_handle': 'KBH_182763', 'user_data': '', 'is_model': 1
              },
              {'name': 'crystal structure of chimeric construct of ksga with loop 1 from erm', 'num_chains': 2, 'num_residues': 486, 'num_atoms': 3794, 'compound': {'misc': '', 'molecule': 'ribosomal rna small subunit methyltransferase a', 'chain': 'a, b', 'synonym': "16s rrna (adenine(1518)-n(6)/adenine(1519)-n(6))-dimethyltransferase,16s rrna dimethyladenosine transferase,16s rrna dimethylase,s-adenosylmethionine-6-n',n'-adenosyl(rrna) dimethyltransferase ", 'ec_number': '2.1.1.182', 'ec': '2.1.1.182', 'engineered': 'yes'}, 'source': {'misc': '', 'organism_scientific': 'bacillus subtilis (strain 168)', 'organism_taxid': '224308', 'strain': '168', 'gene': 'rsma, ksga, bsu00420', 'expression_system': 'escherichia coli', 'expression_system_taxid': '562'},
               'proteins': [{'id': '6ifw.pdb', 'model_id': 0, 'chain_id': 'A', 'sequence': 'NFLIDTNILNRIVDHAEVTEKTGVIEIGPGIGALTEQLAKRAKKVVAFEIDQRLLPILKDTLSPYENVTVIHQDVLKADVKSVIEEQFQDCDEIMVVANLPYYVTTPIIMKLLEEHLPLKGIVVMLQKEVAERMAADPSSKEYGSLSIAVQFYTEAKTVMIVPKTVFVPQPNVDSAVIRLILRDGPAVDVENESFFFQLIKASFAQRRKTLLNNLVNNLPEGKAQKSTIEQVLEETNIDGKRRGESLSIEEFAALSNGLYKALF', 'md5': '662e3cf38381c833487b97de1ad4a5f2', 'seq_identity': 0.671053, 'exact_match': 0, 'genome_ref': '57196/6/1', 'feature_id': 'JCVISYN3_0004', 'feature_type': 'gene'},
                            {'id': '6ifw.pdb', 'model_id': 0, 'chain_id': 'B', 'sequence': 'QNFLIDTNILNRIVDHAEVTEKTGVIEIGPGIGALTEQLAKRAKKVVAFEIDQRLLPILKDTLSPYENVTVIHQDVLKADVKSVIEEQFQDCDEIMVVANLPYYVTTPIIMKLLEEHLPLKGIVVMLQKEVAERMAADPSSKEYGSLSIAVQFYTEAKTVMIVPKTVFVPQPNVDSAVIRLILRDGPAVDVENESFFFQLIKASFNNLVNNLSIEEFAALSN', 'md5': 'c7f304f9a4fb589e19b516ea1bf3a36c', 'seq_identity': 0.671756, 'exact_match': 0, 'genome_ref': '57196/6/1', 'feature_id': 'JCVISYN3_0004', 'feature_type': 'gene'}],
               'pdb_handle': 'KBH_182764', 'user_data': '', 'is_model': 1
              }
            ],
            'total_structures': 4,
            'pdb_infos': cls.pdb_infos,
            'description': 'Created 4 structures test_structures'
        }

        cls.structs_ref = ""
        try:
            info = cls.dfu.save_objects({
                'id': cls.ws_id,
                'objects': [
                    {'type': 'KBaseStructure.ProteinStructures',
                     'name': 'structures_test',
                     'data': obj_to_save}]
            })[0]
        except (RuntimeError, TypeError, KeyError, ValueError) as e:
            err_msg = f'DFU.save_objects errored with message: {e.message} and data: {e.data}'
            print(err_msg)
            raise ValueError(err_msg)
        else:
            cls.structs_ref = f"{info[6]}/{info[0]}/{info[4]}"
        print(f'structure saved with ref={cls.structs_ref}')

    @classmethod
    def tearDownClass(cls):
        pass

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def _get_PDBInfos_1(self):
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
        ret_pdb_infos = self.serviceImpl.get_PDBInfos(
            self.ctx, {'protein_structures_ref': self.structs_ref})
        self.assertEqual(ret_pdb_infos[0], self.pdb_infos)

    def test_get_PDBInfos_2(self):
        # Using CI objects
        expected_pdbinfos1 = [{
            'chain_ids': 'Model 1.Chain A,Model 1.Chain B',
            'exact_matches': '0,0',
            'feature_id': 'JCVISYN3_0004',
            'feature_type': 'gene',
            'file_extension': 'pdb',
            'file_path': '6ifs.pdb',
            'from_rcsb': 0,
            'genome_name': 'Synthetic_bacterium_JCVI_Syn3_genome',
            'genome_ref': '62713/17/1',
            'is_model': 1,
            'model_ids': '0,0',
            'narrative_id': 62713,
            'scratch_path': '/kb/module/work/tmp/3385594d-365a-4b07-9ae8-7b252ae5a73a/6ifs.pdb',
            'sequence_identities': '67.95%,67.74%',
            'structure_name': '6ifs'
          }, {
            'chain_ids': 'Model 1.Chain A',
            'exact_matches': '0',
            'feature_id': 'JCVISYN3_0004',
            'feature_type': 'gene',
            'file_extension': 'pdb',
            'from_rcsb': 0,
            'file_path': '6ift.pdb',
            'genome_name': 'Synthetic_bacterium_JCVI_Syn3_genome',
            'genome_ref': '62713/17/1',
            'is_model': 1,
            'model_ids': '0',
            'narrative_id': 62713,
            'scratch_path': '/kb/module/work/tmp/09d936a7-1efc-4bd0-9929-151e6d437c39/6ift.pdb',
            'sequence_identities': '67.95%',
            'structure_name': '6ift'
          }, {
            'chain_ids': 'Model 1.Chain A,Model 1.Chain B',
            'exact_matches': '0,0',
            'feature_id': 'JCVISYN3_0004',
            'feature_type': 'gene',
            'file_extension': 'pdb',
            'from_rcsb': 0,
            'file_path': '6ifw.pdb',
            'genome_name': 'Synthetic_bacterium_JCVI_Syn3_genome',
            'genome_ref': '62713/17/1',
            'is_model': 1,
            'model_ids': '0,0',
            'narrative_id': 62713,
            'scratch_path': '/kb/module/work/tmp/1f25a4de-8b73-4550-8d56-c777d54e04ca/6ifw.pdb',
            'sequence_identities': '67.11%,67.18%',
            'structure_name': '6ifw'
          }]

        ret_pdb_infos1 = self.serviceImpl.get_PDBInfos(
            self.ctx, {'protein_structures_ref': '67759/37/1'})
        self.assertEqual(ret_pdb_infos1[0], expected_pdbinfos1)

        expected_pdbinfos2 = [{
            'chain_ids': 'Model 1.Chain A,Model 1.Chain B',
            'exact_matches': '0,0', 'feature_id': 'JCVISYN3_0004',
            'feature_type': 'gene', 'file_extension': 'pdb',
            'file_name': '6ifs.pdb', 'from_rcsb': 0,
            'genome_name': 'Synthetic_bacterium_JCVI_Syn3_genome',
            'genome_ref': '62713/17/1', 'is_model': 1, 'model_ids': '0,0',
            'narrative_id': 62713,
            'scratch_path': '/kb/module/work/tmp/2e158ead-2809-4f4d-9f91-d0929f885272/6ifs.pdb',
            'sequence_identities': '67.95%,67.74%', 'structure_name': '6ifs'
          }, {
            'chain_ids': 'Model 1.Chain A', 'exact_matches': '0', 'feature_id': 'JCVISYN3_0004',
            'feature_type': 'gene', 'file_extension': 'pdb', 'file_name': '6ift.pdb', 'from_rcsb': 0,
            'genome_name': 'Synthetic_bacterium_JCVI_Syn3_genome', 'genome_ref': '62713/17/1',
            'is_model': 1, 'model_ids': '0', 'narrative_id': 62713,
            'scratch_path': '/kb/module/work/tmp/e9bb0caf-8499-4630-874c-e9f357c2586d/6ift.pdb',
            'sequence_identities': '67.95%', 'structure_name': '6ift'
          }, {'chain_ids': 'Model 1.Chain A,Model 1.Chain B', 'exact_matches': '0,0',
              'feature_id': 'JCVISYN3_0004', 'feature_type': 'gene', 'file_extension': 'pdb',
              'file_name': '6ifw.pdb', 'from_rcsb': 0,
              'genome_name': 'Synthetic_bacterium_JCVI_Syn3_genome', 'genome_ref': '62713/17/1',
              'is_model': 1, 'model_ids': '0,0', 'narrative_id': 62713,
              'scratch_path': '/kb/module/work/tmp/8f94c7eb-4fe8-414d-9c39-57e5c8f99417/6ifw.pdb',
              'sequence_identities': '67.11%,67.18%', 'structure_name': '6ifw'
          }]

        ret_pdb_infos2 = self.serviceImpl.get_PDBInfos(
            self.ctx, {'protein_structures_ref': '67759/38/1'})
        self.assertEqual(ret_pdb_infos2[0], expected_pdbinfos2)

    def run_PDBHTMLReport(self):
        ret = self.serviceImpl.run_PDBHTMLReport(
            self.ctx, {'protein_structures_ref': self.structs_ref})
        self.assertTrue(ret[0]['report_html'])
        #print(ret[0]['report_html'])
