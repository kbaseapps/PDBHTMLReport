# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os

from PDBHTMLReport.Utils.PDBReportUtil import PDBReportUtil
#END_HEADER


class PDBHTMLReport:
    '''
    Module Name:
    PDBHTMLReport

    Module Description:
    A KBase module: PDBHTMLReport
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = "95ab4907e56dcb18abaa0e53959a77c98814a444"

    #BEGIN_CLASS_HEADER
    '''
    PDBHTMLReport will take a metadata file from the staging area and output an html report
    '''
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.config = config
        self.config['SDK_CALLBACK_URL'] = os.environ['SDK_CALLBACK_URL']
        self.config['KB_AUTH_TOKEN'] = os.environ['KB_AUTH_TOKEN']

        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def run_PDBHTMLReport(self, ctx, params):
        """
        This function accepts PDBHTMLInput as input parameters and returns an output in a PDBHTMLReport
        :param params: instance of type "PDBHTMLReportInput" -> structure:
           parameter "pdb_infos" of list of type "PDBHInfo" (Input/Output of
           run_PDBHTMLReport structure_name: name of the protein structure
           rcsb_id: The structure id for RCSB database file_extension: the
           file extension of the structure, default to 'pdb' from_rcsb:
           indicator if the strcture is from the RCSB Database, default to 0
           is_model: indicator if the strcture is from computational
           modeling, default to 1 narrative_id: id of a KBase narrative
           genome_name: name of a KBase genome object genome_ref: name of a
           KBase genome object reference feature_id: id of a KBase feature
           object feature_type: id of a KBase feature object's type, default
           to 'gene' file_path: path to the pdb_file file of the pdb
           structure stratch_path: path on the shared folder where the
           structure file resides, default to file_path sequence_identities:
           sequence identities matched chain_ids: protein chain ids
           model_ids: model ids exact_matches: a string comma seperated '0'
           and '1' indicating an exact match not found ('0') or found ('1')
           for the structure's proteins with a given KBase genome feature
           @optional) -> structure: parameter "structure_name" of String,
           parameter "rcsb_id" of String, parameter "file_extension" of
           String, parameter "narrative_id" of String, parameter
           "genome_name" of String, parameter "genome_ref" of String,
           parameter "feature_id" of String, parameter "feature_type" of
           String, parameter "file_path" of String, parameter "scratch_path"
           of String, parameter "sequence_identities" of String, parameter
           "chain_ids" of String, parameter "model_ids" of String, parameter
           "exact_matches" of String, parameter "is_model" of type "boolean"
           (A boolean - 0 for false, 1 for true. @range (0, 1)), parameter
           "from_rcsb" of type "boolean" (A boolean - 0 for false, 1 for
           true. @range (0, 1))
        :returns: instance of type "PDBHTMLReportOutput" (report_html: a
           complete html document that can be opened by any browser doms: an
           UnspecifiedObject with DOM html segments that can be used by other
           apps) -> structure: parameter "report_html" of String, parameter
           "doms" of unspecified object
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_PDBHTMLReport
        self.config['USER_ID'] = ctx['user_id']
        self.pdb_util = PDBReportUtil(self.config)

        output = self.pdb_util.generate_html_report(params)

        #END run_PDBHTMLReport

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_PDBHTMLReport return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
